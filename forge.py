#!/usr/bin/env python3
"""
forge.py — Local AI coding agent
Powered by Ollama. Works with any model, tiny to large.
"""

import os
import sys
import json
import re
import subprocess
import difflib
import shutil
import time
import threading
import itertools
import ast
import random
from pathlib import Path

VERSION = "0.6.0"
CODENAME = "forge"

# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------
try:
    import requests
except ImportError:
    print("Missing 'requests'. Run: pip install requests")
    sys.exit(1)

try:
    from rich.console import Console, Group
    from rich.syntax import Syntax
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.table import Table
    from rich.text import Text
    from rich.live import Live
    from rich.spinner import Spinner
    from rich import box as rich_box
    # Force Unicode for Windows
    import sys
    if sys.platform == "win32":
        import os
        os.environ["PYTHONIOENCODING"] = "utf-8"
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
except Exception:
    HAS_RICH = False

def supports_unicode() -> bool:
    """Check if terminal supports Unicode properly."""
    try:
        import sys
        # Try to encode a test character
        "⠋⣾🌟⟳".encode(sys.stdout.encoding or "utf-8")
        return True
    except (AttributeError, UnicodeEncodeError, LookupError):
        return False

SUPPORTS_UNICODE = supports_unicode()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OLLAMA_CANDIDATES = [
    os.getenv("OLLAMA_HOST", "").strip(),
    "http://localhost:11434",
    "http://127.0.0.1:11434",
    "http://0.0.0.0:11434",
]

WORKDIR = os.path.abspath(os.getenv("WORKDIR", "."))
MAX_TOOL_OUTPUT = int(os.getenv("MAX_TOOL_OUTPUT", "2000"))
EXEC_MODE = "ask"  # "auto", "ask", "manual"
SAFE_TOOLS = {"read", "list", "search", "ask_choice"}  # Always auto, never confirm

console = Console() if HAS_RICH else None


# ---------------------------------------------------------------------------
# Animation & startup
# ---------------------------------------------------------------------------

FORGE_LOGO = r"""
  ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
  █████╗  ██║   ██║██████╔╝██║  ███╗█████╗  
  ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  
  ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
  ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
"""

TAGLINE = "local AI coding agent"

# ---------------------------------------------------------------------------
# UI Helpers & Visuals
# ---------------------------------------------------------------------------

ACTIVITY_WORDS = [
    "Synthesizing thoughts", "Polishing code", "Consulting the binary gods",
    "Rerouting power to logic", "Analyzing patterns", "Waking up neural nets",
    "Optimizing context", "Thinking really hard", "Brewing coffee for the AI",
    "Aligning sub-tokens", "Scanning repository", "Parsing intentions"
]

FLOWER_SPINNER = ["◐", "◓", "◑", "◒", "◌", "◍"]

def animate_startup():
    """Startup animation — logo appears smoothly."""
    if not HAS_RICH:
        print(FORGE_LOGO)
        print(f"  {TAGLINE}  v{VERSION}")
        print()
        return

    logo_text = Text(FORGE_LOGO, style="bold #FFA000")

    console.clear()
    console.print()
    with Live(Panel(logo_text, box=rich_box.ROUNDED, padding=(0, 2), border_style="#FFA000"),
              console=console, refresh_per_second=10) as live:
        time.sleep(0.5)
        live.update(Panel(Group(logo_text, Text(f"\n{TAGLINE}  v{VERSION}", justify="center", style="dim")),
                          box=rich_box.ROUNDED, padding=(0, 2), border_style="#FFA000"))
        time.sleep(0.5)
    console.print()


def spinner_task(label: str, func, *args, **kwargs):
    """Runs func(*args, **kwargs) in the background, showing a spinner. Returns result."""
    if not HAS_RICH:
        print(f"{label}...", end=" ", flush=True)
        result = func(*args, **kwargs)
        print("OK")
        return result

    result_container = [None]
    done = threading.Event()

    def worker():
        result_container[0] = func(*args, **kwargs)
        done.set()

    t = threading.Thread(target=worker, daemon=True)
    t.start()

    try:
        # Use Rich's built-in Spinner with auto-fallback
        with Live(
            Spinner("dots", text=f" {label}", style="dim"),
            console=console, refresh_per_second=12
        ) as live:
            done.wait()
    except Exception:
        # Fallback for Windows without Unicode support
        if not done.is_set():
            print(f"  {label}...", end=" ", flush=True)
        done.wait()
        print("OK", flush=True)

    return result_container[0]


def animate_connecting(url: str):
    """Connecting to Ollama animation."""
    if not HAS_RICH:
        print(f"Connecting to Ollama at {url}...")
        return

    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(8):
        for f in frames[:3]:
            console.print(f"  [dim]{f}[/dim] [dim]connecting to ollama...[/dim]", end="\r")
            time.sleep(0.06)
    console.print(" " * 50, end="\r")


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def p_ok(msg):
    if HAS_RICH: console.print(f"  [green]✓[/green] {msg}")
    else: print(f"  ✓ {msg}")

def p_err(msg):
    if HAS_RICH: console.print(f"  [bold red]✗[/bold red] {msg}")
    else: print(f"  ✗ {msg}")

def p_warn(msg):
    if HAS_RICH: console.print(f"  [yellow]![/yellow] {msg}")
    else: print(f"  ! {msg}")

def p_info(msg):
    if HAS_RICH: console.print(f"  [dim]{msg}[/dim]")
    else: print(f"  {msg}")

def p_tool(name, args_str, status="run"):
    """Print tool execution. status: 'run', 'ok', 'err'"""
    icon = {"run": "●" if SUPPORTS_UNICODE else "~", "ok": "✓", "err": "✗"}.get(status, "?")
    colors = {"run": "[#FFA000]", "ok": "[green]", "err": "[bold red]"}.get(status, "")
    color_end = {"run": "[/#FFA000]", "ok": "[/green]", "err": "[/bold red]"}.get(status, "")

    if HAS_RICH:
        console.print(f"  {colors}{icon}{color_end} [cyan]{name}[/cyan][dim]({args_str})[/dim]")
    else:
        print(f"  {icon} {name}({args_str})")

def p_tool_result(msg):
    if HAS_RICH: console.print(f"  [dim]  {msg}[/dim]")
    else: print(f"    {msg}")

def p_separator():
    if HAS_RICH: console.print("[dim]" + "─" * 60 + "[/dim]")
    else: print("─" * 60)

def truncate(text: str, n: int = MAX_TOOL_OUTPUT) -> str:
    if len(text) <= n:
        return text
    h = n // 2
    return text[:h] + f"\n  ...[{len(text)-n} chars hidden]...\n" + text[-h:]


# ---------------------------------------------------------------------------
# Ollama — detection and API
# ---------------------------------------------------------------------------

def detect_ollama() -> str:
    """Detect Ollama API. If not running, attempt to start it (Windows/Linux)."""
    for candidate in OLLAMA_CANDIDATES:
        if not candidate:
            continue
        base = candidate.rstrip("/")
        if not base.startswith("http"):
            base = "http://" + base
        try:
            r = requests.get(f"{base}/api/tags", timeout=1)
            if r.status_code == 200:
                return base
        except Exception:
            pass

    # Not found — try to start it
    p_info("Ollama not responding. Attempting to start 'ollama serve'...")
    try:
        if sys.platform == "win32":
            # Use CREATE_NO_WINDOW (0x08000000) for Windows
            subprocess.Popen(["ollama", "serve"], creationflags=0x08000000,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Poll for 10 seconds
        for _ in range(10):
            time.sleep(1)
            try:
                r = requests.get("http://localhost:11434/api/tags", timeout=1)
                if r.status_code == 200:
                    return "http://localhost:11434"
            except Exception:
                pass
    except Exception as e:
        p_warn(f"Could not start Ollama: {e}")

    return ""


def parse_param_size(param_str: str) -> float:
    """Parse parameter size string like '494.03M' or '3.1B' to billions."""
    if not param_str:
        return 7.0
    param_str = param_str.strip().upper()
    try:
        if "B" in param_str:
            return float(param_str.replace("B", ""))
        elif "M" in param_str:
            return float(param_str.replace("M", "")) / 1000.0
        elif "K" in param_str:
            return float(param_str.replace("K", "")) / 1000000.0
    except ValueError:
        pass
    return 7.0


def get_models(base_url: str) -> list:
    """Get models from Ollama with auto-detected parameters."""
    try:
        r = requests.get(f"{base_url}/api/tags", timeout=5)
        r.raise_for_status()
        models = r.json().get("models", [])

        # Enrich with API details
        enriched = []
        for m in models:
            details = m.get("details", {})
            param_size_str = details.get("parameter_size", "7B")
            params_b = parse_param_size(param_size_str)

            enriched.append({
                "name": m["name"],
                "size_bytes": m.get("size", 0),
                "params_b": params_b,
                "quant": details.get("quantization_level", "?"),
                "family": details.get("family", "unknown"),
                "context_length": details.get("context_length", 0),
                "size_mb": m.get("size", 0) // (1024 * 1024),
            })

        enriched.sort(key=lambda m: m["size_bytes"])
        return enriched
    except Exception:
        return []


def model_profile(model: dict) -> dict:
    """Get profile from model dict (from get_models) or fallback to name string."""
    # Support both old string format and new dict format
    if isinstance(model, str):
        name = model.lower()
        m = re.search(r'(\d+(?:\.\d+)?)b', name)
        params_b = float(m.group(1)) if m else 7.0
        context_len = 0 # unknown
    else:
        params_b = model.get("params_b", 7.0)
        context_len = model.get("context_length", 0)

    if params_b <= 1.0:
        p = {"max_context": 4,  "max_tool_output": 800,  "num_predict": 512,  "temperature": 0.05, "label": "tiny"}
    elif params_b <= 3.0:
        p = {"max_context": 6,  "max_tool_output": 1200, "num_predict": 768,  "temperature": 0.1,  "label": "small"}
    elif params_b <= 8.0:
        p = {"max_context": 10, "max_tool_output": 2000, "num_predict": 1536, "temperature": 0.1,  "label": "medium"}
    elif params_b <= 20.0:
        p = {"max_context": 14, "max_tool_output": 3000, "num_predict": 2048, "temperature": 0.15, "label": "large"}
    else:
        p = {"max_context": 20, "max_tool_output": 5000, "num_predict": 4096, "temperature": 0.2,  "label": "xlarge"}
    
    # If API provided real context length, we can use it (heuristic: 1 msg ~ 1000 tokens)
    # But for now we keep max_context as message count for stability with tiny models
    if context_len > 0:
        p["context_length"] = context_len
    else:
        # Fallback heuristic context length in tokens
        p["context_length"] = p["max_context"] * 1000

    return p


# ---------------------------------------------------------------------------
# Model selection — interactive menu
# ---------------------------------------------------------------------------

def choose_model(models: list, preselect: str = "") -> str:
    """Choose model from list. Models can be dicts (from get_models) or strings (legacy)."""
    # Handle legacy string format
    if models and isinstance(models[0], str):
        # Old format: just names
        if preselect and preselect in models:
            return preselect
        if not models:
            p_warn("No models found. Enter name manually:")
            return input("  Model: ").strip() or "qwen2.5:0.5b"
        if HAS_RICH:
            console.print()
            console.print("  [bold]Available models[/bold]")
            console.print()
            t = Table(box=None, show_header=False, padding=(0, 2))
            t.add_column("num", style="dim", width=4)
            t.add_column("name", style="cyan")
            for i, m in enumerate(models, 1):
                t.add_row(f"{i}.", m)
            console.print(t)
            console.print()
            raw = Prompt.ask("[dim]Select model number or name[/dim]", default="1").strip()
        else:
            print("\n  Available models:")
            for i, m in enumerate(models, 1):
                print(f"    {i}. {m}")
            raw = input("  Select (Enter = 1): ").strip() or "1"
        if raw.isdigit():
            idx = int(raw) - 1
            return models[idx] if 0 <= idx < len(models) else models[0]
        elif raw in models:
            return raw
        else:
            matches = [m for m in models if raw.lower() in m.lower()]
            return matches[0] if matches else models[0]

    # New format: list of dicts from get_models()
    if preselect:
        match = next((m for m in models if m["name"] == preselect), None)
        if match:
            return match["name"]

    if not models:
        p_warn("No models found. Enter name manually:")
        return input("  Model: ").strip() or "qwen2.5:0.5b"

    if HAS_RICH:
        console.print()
        console.print("  [bold]Available models[/bold]")
        console.print()

        t = Table(box=None, show_header=False, padding=(0, 2))
        t.add_column("num", style="dim", width=4)
        t.add_column("name", style="cyan", width=20)
        t.add_column("params", style="dim", justify="right", width=8)
        t.add_column("quant", style="dim", width=10)
        t.add_column("size", style="dim", justify="right", width=8)
        t.add_column("family", style="dim")

        for i, m in enumerate(models, 1):
            prof = model_profile(m)
            size_str = f"{m['size_mb']}MB" if m['size_mb'] < 1024 else f"{m['size_mb']//1024}GB"
            params_str = f"{m['params_b']:.1f}B"
            t.add_row(
                f"{i}.",
                m["name"],
                params_str,
                m["quant"],
                size_str,
                f"[dim]{m['family']}[/dim]"
            )

        console.print(t)
        console.print()
        raw = Prompt.ask(
            "  [dim]Select model number or name[/dim]",
            default="1"
        ).strip()
    else:
        print("\n  Available models:")
        for i, m in enumerate(models, 1):
            print(f"    {i}. {m['name']} ({m['params_b']:.1f}B, {m['quant']}, {m['family']})")
        raw = input("  Select (Enter = 1): ").strip() or "1"

    if raw.isdigit():
        idx = int(raw) - 1
        return models[idx]["name"] if 0 <= idx < len(models) else models[0]["name"]
    else:
        matches = [m for m in models if raw.lower() in m["name"].lower()]
        return matches[0]["name"] if matches else models[0]["name"]


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

def build_system_prompt(workdir: str, tiny: bool = False) -> str:
    tools_desc = """- read(path, [start_line], [end_line]): Read file with line numbers
- write(path, content): Write/overwrite entire file
- patch(path, old_text, new_text): Replace first occurrence of old_text (safe)
- list([path], [pattern]): List files recursively
- search(pattern, [path], [file_glob]): Search text (grep)
- shell(cmd, [timeout]): Run shell command
- delete(path): Delete file/dir
- rename(src, dst): Rename/move
- mkdir(path): Create directory
- ask_choice(question, options): Ask user to pick an option (Decision point)"""

    common_rules = """1. Read before edit.
2. patch for small changes.
3. One tool per message.
4. If task is clear, ACT IMMEDIATELY.
5. If unclear or multiple options exist, use ask_choice to let the user decide.
6. Write complete code.
7. Match style. No TODOs."""

    if tiny:
        return f"""You are Forge (tiny). Workdir: {workdir}
TOOLS: {{"tool":"name","args":{{...}}}}
{tools_desc}
RULES: {common_rules}"""

    return f"""You are Forge, an expert local AI coding agent.
Working directory: {workdir}

## Core Workflow
1. Analyze -> 2. Plan -> 3. Act (Analyze the task, state your plan, then use tools).

## Tools
Output JSON on its own line:
{{"tool":"<name>","args":{{<params>}}}}

{tools_desc}

## Rules
{common_rules}"""


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

def tool_read(path: str, start_line: int = 1, end_line: int = 0) -> str:
    p = Path(WORKDIR) / path if not Path(path).is_absolute() else Path(path)
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        total = len(lines)
        sl, el = max(1, int(start_line)), int(end_line)
        chunk = lines[sl-1:el] if el > 0 else lines[sl-1:]
        numbered = [f"{sl+i:5}│ {l}" for i, l in enumerate(chunk)]
        return f"[{path}  {total} lines]\n" + truncate("\n".join(numbered))
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return f"Read error: {e}"


def tool_write(path: str, content: str) -> str:
    p = Path(WORKDIR) / path if not Path(path).is_absolute() else Path(path)
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Written: {path}  ({len(content.splitlines())} lines)"
    except Exception as e:
        return f"Write error: {e}"


def tool_patch(path: str, old_text: str, new_text: str) -> str:
    p = Path(WORKDIR) / path if not Path(path).is_absolute() else Path(path)
    try:
        original = p.read_text(encoding="utf-8")
        if old_text not in original:
            return f"Error: text not found in {path}\nTip: use /read {path} to verify exact content"
        updated = original.replace(old_text, new_text, 1)
        p.write_text(updated, encoding="utf-8")
        diff_lines = list(difflib.unified_diff(
            original.splitlines(keepends=True),
            updated.splitlines(keepends=True),
            fromfile=f"a/{path}", tofile=f"b/{path}", n=3
        ))
        diff = "".join(diff_lines[:60])
        return f"Patched: {path}\n{diff}"
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return f"Patch error: {e}"


def tool_list(path: str = ".", pattern: str = "*") -> str:
    base = Path(WORKDIR) / path if not Path(path).is_absolute() else Path(path)
    SKIP = {".git","__pycache__","node_modules",".venv","venv",".next","dist","build","target"}
    try:
        results = []
        for f in sorted(base.rglob(pattern)):
            if any(s in f.parts for s in SKIP):
                continue
            rel = f.relative_to(base)
            results.append(f"{'[D]' if f.is_dir() else '[F]'} {rel}")
        if not results:
            return "(empty)"
        extra = len(results) - 100
        out = results[:100]
        if extra > 0:
            out.append(f"  ... and {extra} more")
        return "\n".join(out)
    except Exception as e:
        return f"List error: {e}"


def tool_search(pattern: str, path: str = ".", file_glob: str = "*") -> str:
    base = Path(WORKDIR) / path if not Path(path).is_absolute() else Path(path)
    SKIP = {".git","__pycache__","node_modules",".venv","venv"}
    results = []
    try:
        for f in sorted(base.rglob(file_glob)):
            if any(s in f.parts for s in SKIP) or not f.is_file():
                continue
            try:
                for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                    if pattern.lower() in line.lower():
                        results.append(f"{f.relative_to(base)}:{i}: {line.strip()}")
            except Exception:
                pass
        return truncate("\n".join(results)) if results else f"No matches for: '{pattern}'"
    except Exception as e:
        return f"Search error: {e}"


def tool_shell(cmd: str, timeout: int = 30) -> str:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           timeout=int(timeout), cwd=WORKDIR)
        out, err = r.stdout.strip(), r.stderr.strip()
        parts = ([out] if out else []) + ([f"[stderr]\n{err}"] if err else [])
        return truncate("\n".join(parts) or "(no output)") + f"\n[exit: {r.returncode}]"
    except subprocess.TimeoutExpired:
        return f"Timeout after {timeout}s"
    except Exception as e:
        return f"Shell error: {e}"


def tool_delete(path: str) -> str:
    p = Path(WORKDIR) / path if not Path(path).is_absolute() else Path(path)
    try:
        if p.is_file():
            p.unlink(); return f"Deleted file: {path}"
        elif p.is_dir():
            shutil.rmtree(p); return f"Deleted dir: {path}"
        return f"Not found: {path}"
    except Exception as e:
        return f"Delete error: {e}"


def tool_rename(src: str, dst: str) -> str:
    s = Path(WORKDIR) / src if not Path(src).is_absolute() else Path(src)
    d = Path(WORKDIR) / dst if not Path(dst).is_absolute() else Path(dst)
    try:
        d.parent.mkdir(parents=True, exist_ok=True)
        s.rename(d); return f"Renamed: {src} → {dst}"
    except Exception as e:
        return f"Rename error: {e}"


def tool_mkdir(path: str) -> str:
    p = Path(WORKDIR) / path if not Path(path).is_absolute() else Path(path)
    try:
        os.makedirs(p, exist_ok=True)
        return f"Directory created: {path}"
    except Exception as e:
        return f"Mkdir error: {e}"


def tool_ask_choice(question: str, options: list) -> str:
    """Model asks user to pick from multiple options."""
    if not HAS_RICH:
        print(f"\n  [?] {question}")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        ans = input(f"  Select [1-{len(options)}]: ").strip()
        try:
            idx = int(ans) - 1
            return f"User selected option: {options[idx]}"
        except:
            return f"User provided custom response: {ans}"

    console.print(f"\n  [yellow]?[/yellow] [bold]{question}[/bold]")
    for i, opt in enumerate(options, 1):
        console.print(f"  [cyan]{i}.[/cyan]    {opt}")
    console.print(f"  [cyan]{len(options)+1}.[/cyan]    Enter custom instruction...")

    try:
        raw = Prompt.ask(
            f"  [dim]Select option [1-{len(options)+1}][/dim]",
            default="1"
        ).strip()
    except (KeyboardInterrupt, EOFError):
        return "[User cancelled the selection]"

    if raw.isdigit():
        idx = int(raw) - 1
        if 0 <= idx < len(options):
            return f"User selected option: {options[idx]}"
        elif idx == len(options):
            custom = input("  Custom instruction: ").strip()
            return f"User chose a custom path: {custom}"
    
    return f"User provided raw response: {raw}"


TOOLS = {
    "read":       (tool_read,       "Read file with line numbers",    "path [start_line] [end_line]"),
    "write":      (tool_write,      "Write/overwrite file",           "path content"),
    "patch":      (tool_patch,      "Replace text in file (safe)",    "path old_text new_text"),
    "list":       (tool_list,       "List files recursively",         "[path] [pattern]"),
    "search":     (tool_search,     "Grep text in files",             "pattern [path] [file_glob]"),
    "shell":      (tool_shell,      "Run shell command",              "cmd [timeout]"),
    "delete":     (tool_delete,     "Delete file or directory",       "path"),
    "rename":     (tool_rename,     "Rename or move file",            "src dst"),
    "mkdir":      (tool_mkdir,      "Safely create directory",        "path"),
    "ask_choice": (tool_ask_choice, "Ask user to pick an option",     "question options"),
}


def run_tool(name: str, args: dict) -> str:
    if name not in TOOLS:
        return f"Unknown tool: '{name}'. Available: {', '.join(TOOLS)}"
    func, _, _ = TOOLS[name]
    try:
        return func(**args)
    except TypeError as e:
        return f"Bad args for '{name}': {e}"
    except Exception as e:
        return f"Tool error: {e}"


# ---------------------------------------------------------------------------
# Ollama stream chat
# ---------------------------------------------------------------------------

def llm_generate(messages: list, model: str, base_url: str, profile: dict) -> str:
    """Non-streaming chat for utility tasks like summarization."""
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 512,
        }
    }
    try:
        resp = requests.post(f"{base_url}/api/chat", json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json().get("message", {}).get("content", "").strip()
    except Exception as e:
        return f"Error: {e}"


def stream_chat(messages: list, model: str, base_url: str, profile: dict) -> tuple:
    """Stream chat from Ollama with Flower animation, activity words and precise stats."""
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": profile["temperature"],
            "num_predict": profile["num_predict"],
        }
    }
    try:
        resp = requests.post(f"{base_url}/api/chat", json=payload, stream=True, timeout=180)
        resp.raise_for_status()
    except Exception as e:
        p_err(f"Connection error: {e}")
        return "", {"prompt_tokens": 0, "completion_tokens": 0, "tokens_per_sec": 0, "elapsed": 0}

    full_text = []
    prompt_tokens = 0
    completion_tokens = 0
    start_time = time.time()

    if not HAS_RICH:
        print(f"\n  [{model}]: ", end="", flush=True)
        for line in resp.iter_lines():
            if not line: continue
            try:
                chunk = json.loads(line)
                token = chunk.get("message", {}).get("content", "")
                if token:
                    print(token, end="", flush=True)
                    full_text.append(token)
                if chunk.get("done"):
                    prompt_tokens = chunk.get("prompt_eval_count", 0)
                    completion_tokens = chunk.get("eval_count", 0)
                    break
            except: pass
        print()
        elapsed = time.time() - start_time
        tps = completion_tokens / elapsed if elapsed > 0 else 0
        return "".join(full_text), {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "tokens_per_sec": tps, "elapsed": elapsed}

    # -- RICH CLAUDE-CODE STYLE UI --
    response_display = Text("")
    activity_word = random.choice(ACTIVITY_WORDS)
    spinner_idx = 0

    def make_layout(status_text: str, footer_text: str, is_done=False) -> Group:
        # Header: Icon + Activity/Time
        color = "green" if is_done else "#FFA000"
        header = Text.assemble(
            (f"  {FLOWER_SPINNER[spinner_idx] if not is_done else '✓'} ", color),
            (f"{model} ", "cyan"),
            (f"| {status_text} ", "dim")
        )

        # Tool call hiding logic
        cleaned_response = Text("")
        raw_lines = response_display.plain.splitlines()
        for i, line in enumerate(raw_lines):
            if '"tool":' in line or '"args":' in line:
                continue
            cleaned_response.append(line + ("\n" if i < len(raw_lines)-1 else ""))

        # Footer: Tokens & speed
        footer = Text(f"  {footer_text}", style="dim italic") if footer_text else Text("")

        return Group(header, cleaned_response, footer)

    # Render loop using Live
    with Live(make_layout(activity_word, ""), console=console, refresh_per_second=12) as live:
        try:
            for line in resp.iter_lines():
                if not line: continue
                try:
                    chunk = json.loads(line)
                    token = chunk.get("message", {}).get("content", "")
                    if token:
                        response_display.append(token)
                        full_text.append(token)

                        # Heuristic for live updates
                        completion_tokens += 1

                        now = time.time()
                        elapsed = now - start_time
                        tps = completion_tokens / elapsed if elapsed > 0 else 0

                        # Update spinner and activity word
                        spinner_idx = (spinner_idx + 1) % len(FLOWER_SPINNER)
                        if spinner_idx == 0 and random.random() < 0.1:
                            activity_word = random.choice(ACTIVITY_WORDS)

                        live.update(make_layout(f"{elapsed:.1f}s", f"{completion_tokens} ↓ · {tps:.1f} t/s"))

                    if chunk.get("done"):
                        prompt_tokens = chunk.get("prompt_eval_count", 0)
                        completion_tokens = chunk.get("eval_count", 0)
                        break
                except json.JSONDecodeError: pass
        except (KeyboardInterrupt, Exception) as e:
            if isinstance(e, KeyboardInterrupt):
                p_warn("Stream interrupted by user.")
            else:
                p_err(f"Stream error: {e}")

    elapsed = time.time() - start_time
    tokens_per_sec = completion_tokens / elapsed if elapsed > 0 else 0

    # Final cleanup (replace live status with precise final summary)
    console.print(f"  [dim]{prompt_tokens} ↑ · {completion_tokens} ↓ · {tokens_per_sec:.1f} t/s[/dim]\n")

    return "".join(full_text), {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "tokens_per_sec": tokens_per_sec,
        "elapsed": elapsed
    }


def extract_tool_calls(text: str) -> list:
    """Extract tool calls from model output using multiple strategies."""
    calls = []

    # Strategy 1: Standard JSON object {"tool":"name","args":{...}}
    # Use a more lenient regex that allows nested objects
    for match in re.finditer(r'\{[^{}]*"tool"\s*:', text, re.DOTALL):
        start = match.start()
        # Find matching closing brace
        depth = 0
        for i in range(start, len(text)):
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    try:
                        obj = json.loads(text[start:i+1])
                        if "tool" in obj and "args" in obj:
                            calls.append(obj)
                    except json.JSONDecodeError:
                        pass
                    break

    if calls:
        return calls

    # Strategy 2: JSON inside markdown code block ```json {...}```
    for match in re.finditer(r'```(?:json)?\s*(\{[^`]+\})\s*```', text, re.DOTALL):
        try:
            obj = json.loads(match.group(1))
            if "tool" in obj:
                obj.setdefault("args", {})
                calls.append(obj)
        except Exception:
            pass

    if calls:
        return calls

    # Strategy 3: Function-call syntax like read("path") or shell("ls -la")
    for match in re.finditer(rf'(\w+)\(([^)]*)\)', text):
        func_name = match.group(1)
        if func_name in TOOLS:
            args_str = match.group(2).strip()
            try:
                # Parse as Python literals
                if args_str:
                    parsed = ast.literal_eval(f"({args_str})")
                    if not isinstance(parsed, tuple):
                        parsed = (parsed,)
                else:
                    parsed = ()

                # Extract param names from param_str like "path [start_line] [end_line]"
                _, _, param_str = TOOLS[func_name]
                param_names = [p.strip("[]") for p in param_str.split()]

                args_dict = {}
                for i, val in enumerate(parsed):
                    if i < len(param_names):
                        args_dict[param_names[i]] = val

                calls.append({"tool": func_name, "args": args_dict})
            except (SyntaxError, ValueError, KeyError):
                pass

    return calls


# ---------------------------------------------------------------------------
# Context — sliding window
# ---------------------------------------------------------------------------

class ContextWindow:
    def __init__(self, system: str, max_msgs: int = 10, max_tokens: int = 4000):
        self.system = system
        self.max_msgs = max_msgs
        self.max_tokens = max_tokens
        self.messages: list = []
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0

    def set_max(self, msgs: int, tokens: int = 4000):
        self.max_msgs = msgs
        self.max_tokens = tokens

    def estimate_tokens(self, text: str) -> int:
        # Crude estimation: 4 chars = 1 token
        return len(text) // 4

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self.trim()

    def trim(self):
        # 1. Trim by message count
        if len(self.messages) > self.max_msgs:
            head = min(2, len(self.messages))
            self.messages = self.messages[:head] + self.messages[-(self.max_msgs - head):]

        # 2. Trim by token count (heuristic)
        # Always keep system prompt and last few messages if possible
        while len(self.messages) > 2:
            total = self.estimate_tokens(self.system)
            for m in self.messages:
                total += self.estimate_tokens(m["content"])
            
            if total > self.max_tokens * 0.9: # leave some buffer
                # Remove oldest message (after the head/first 2 which we usually want to keep for context)
                # But here we just remove index 2 (third message) to keep the flow
                if len(self.messages) > 3:
                    self.messages.pop(2)
                else:
                    break
            else:
                break

    def add_tokens(self, prompt: int, completion: int):
        self.total_prompt_tokens += prompt
        self.total_completion_tokens += completion
        # Save to persistent storage
        try:
            stats_dir = os.path.join(os.path.expanduser("~"), "Documents", "FORGE_agent_memory")
            os.makedirs(stats_dir, exist_ok=True)
            stats_path = os.path.join(stats_dir, "usage_stats.json")
            
            data = {"total_in": 0, "total_out": 0, "sessions": 0}
            if os.path.exists(stats_path):
                try:
                    with open(stats_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except: pass
            
            data["total_in"] += prompt
            data["total_out"] += completion
            # We don't increment sessions here, only once per startup if desired
            
            with open(stats_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except: pass

    def clear(self):
        self.messages = []
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0

    def build(self) -> list:
        return [{"role": "system", "content": self.system}] + self.messages

    def stats(self) -> str:
        chars = sum(len(m["content"]) for m in self.messages)
        tokens = chars // 4
        return f"{len(self.messages)} msgs, ~{tokens:,} tokens"

    def token_stats(self) -> str:
        total = self.total_prompt_tokens + self.total_completion_tokens
        return f"Session: {self.total_prompt_tokens:,} in  {self.total_completion_tokens:,} out  {total:,} total"


# ---------------------------------------------------------------------------
# Agentic loop
# ---------------------------------------------------------------------------

def should_confirm(tool_name: str) -> bool:
    """Check if tool execution needs user confirmation based on EXEC_MODE."""
    global EXEC_MODE
    if EXEC_MODE == "auto":
        return False
    if EXEC_MODE == "manual":
        return True
    # "ask" mode — safe tools don't need confirmation
    return tool_name not in SAFE_TOOLS


def ask_confirm(tool_name: str, args: dict) -> bool:
    """Ask user to confirm tool execution. Defaults to Yes (Enter)."""
    tool_func, _, _ = TOOLS.get(tool_name, (None, None, None))
    if not tool_func:
        return False

    # Format args for display
    if tool_name == "shell":
        cmd = args.get("cmd", "?")
        display = f"{tool_name}: {cmd}"
    else:
        display = f"{tool_name}({', '.join(f'{k}={v!r}' for k, v in args.items())})"

    if not HAS_RICH:
        print(f"\n  → {display}")
        ans = input(f"  Execute [Y/n]: ").strip().lower()
        return ans in ("", "y", "yes")

    try:
        print()
        ans = Prompt.ask(
            f"  [yellow]?[/yellow] {tool_name.upper()}: [cyan]{display[len(tool_name)+1:]}[/cyan] [dim][Y/n][/dim]",
            default="y"
        ).strip().lower()
        return ans in ("", "y", "yes")
    except (KeyboardInterrupt, EOFError):
        return False
    except:
        print(f"  → {display}")
        ans = input(f"  Execute [Y/n]: ").strip().lower()
        return ans in ("", "y", "yes")


def agentic_loop(user_input: str, ctx: ContextWindow,
                 model: str, base_url: str, profile: dict):
    ctx.add("user", user_input)

    for _ in range(10):
        response, stats = stream_chat(ctx.build(), model, base_url, profile)
        ctx.add_tokens(stats["prompt_tokens"], stats["completion_tokens"])

        if not response:
            break

        calls = extract_tool_calls(response)
        if not calls:
            ctx.add("assistant", response)
            break

        ctx.add("assistant", response)
        tool_results = []

        console.print(f"\n  [bold #FFA000]●[/bold #FFA000] [dim]Executing plan...[/dim]") if HAS_RICH else None

        for call in calls:
            name = call["tool"]
            args = call.get("args", {})
            args_preview = json.dumps(args, ensure_ascii=False)
            if len(args_preview) > 70:
                args_preview = args_preview[:67] + "..."
            p_tool(name, args_preview, status="run")

            # Check if confirmation needed
            confirmed = True
            if should_confirm(name):
                confirmed = ask_confirm(name, args)
            
            if not confirmed:
                result = f"[{name} execution cancelled by user]"
                p_tool(name, args_preview, status="err")
            else:
                result = run_tool(name, args)
                p_tool(name, args_preview, status="ok")

            # Compact result display
            res_str = str(result).strip()
            if len(res_str.splitlines()) > 5:
                for line in res_str.splitlines()[:5]:
                    p_tool_result(line)
                p_tool_result(f"... and {len(res_str.splitlines())-5} more lines")
            else:
                p_tool_result(truncate(res_str, 100))

            tool_results.append(f"[{name} result]\n{result}")

        ctx.add("user", "\n\n".join(tool_results))
    else:
        p_warn("Agent loop limit reached.")


# ---------------------------------------------------------------------------
# Slash commands
# ---------------------------------------------------------------------------

HELP = """
  Commands
  ──────────────────────────────────────────────────
  /help              Show this help
  /model             Interactive model picker
  /model <name>      Switch to named model
  /models            List available models
  /cd <dir>          Change working directory
  /compact           Summarize conversation to save context
  /clear             Clear conversation history
  /ctx               Show context stats (messages)
  /tokens            Show session token totals
  /usage             Show persistent usage dashboard
  /profile           Show current model profile
  /mode              Show current execution mode
  /auto              Switch to auto mode (execute all without asking)
  /ask               Switch to ask mode (confirm destructive ops)
  /manual            Switch to manual mode (confirm all)
  /tools             List available tools
  /read <file>       Read file directly (no AI)
  /shell <cmd>       Run shell command directly
  /exit              Quit
  ──────────────────────────────────────────────────
  AI tools: read write patch list search shell delete rename mkdir
"""

def show_status_bar(model: str, profile: dict, workdir: str, ctx: ContextWindow):
    """Displays permanent dashboard-style status bar."""
    global EXEC_MODE
    if not HAS_RICH:
        return

    # Precise tokens from context
    stats = ctx.stats()

    # Dashboard elements
    dir_text = Text.assemble((" dir ", "bg:#333333 white"), (f" {workdir} ", "bg:#444444 yellow"))
    mode_text = Text.assemble((" mode ", "bg:#333333 white"), (f" {EXEC_MODE} ", f"bg:#444444 {'green' if EXEC_MODE=='auto' else 'cyan'}"))
    model_text = Text.assemble((" model ", "bg:#333333 white"), (f" {model} ", "bg:#444444 blue"))
    token_text = Text(f" {stats}", style="dim")

    console.print(Group(
        dir_text + Text(" ") + mode_text + Text(" ") + model_text + Text(" ") + token_text,
        Text("─" * console.width, style="dim")
    ))


def handle_slash(cmd: str, ctx: ContextWindow, state: dict) -> dict:
    global WORKDIR, EXEC_MODE
    parts = cmd.strip().split(maxsplit=1)
    name = parts[0].lower()
    arg = parts[1].strip() if len(parts) > 1 else ""

    if name == "/exit":
        if HAS_RICH:
            console.print("\n  [dim]bye.[/dim]\n")
        else:
            print("bye.")
        sys.exit(0)

    elif name == "/help":
        if HAS_RICH:
            console.print(Panel(HELP.strip(), border_style="dim", padding=(0, 1)))
        else:
            print(HELP)

    elif name == "/model":
        if arg:
            new_model = arg
        else:
            new_model = choose_model(state["models_list"])
        prof = model_profile(new_model)
        state.update({"model": new_model, "profile": prof})
        ctx.set_max(prof["max_context"], prof["context_length"])
        tiny = prof["num_predict"] <= 512
        ctx.system = build_system_prompt(WORKDIR, tiny=tiny)
        p_ok(f"Model: [cyan]{new_model}[/cyan]  [{prof['label']}]" if HAS_RICH
             else f"Model: {new_model}  [{prof['label']}]")

    elif name == "/compact":
        if len(ctx.messages) > 4:
            # summarize except last 2
            to_summarize = ctx.messages[:-2]
            keep = ctx.messages[-2:]
            
            summary_prompt = [{"role": "system", "content": "Summarize the following conversation in one paragraph."}]
            summary_prompt += to_summarize
            
            p_info("Compacting history...")
            summary = llm_generate(summary_prompt, state["model"], state["base_url"], state["profile"])
            
            ctx.messages = [{"role": "assistant", "content": f"Summary of previous conversation: {summary}"}] + keep
            p_ok("Conversation compacted.")
        else:
            p_info("Not enough messages to compact.")

    elif name == "/models":
        models = get_models(state["base_url"])
        state["models_list"] = models
        if HAS_RICH:
            t = Table(box=None, show_header=False, padding=(0, 2))
            t.add_column("num", style="dim", width=4)
            t.add_column("name", style="cyan")
            t.add_column("params", style="dim", justify="right")
            t.add_column("tag", style="dim")
            for i, m in enumerate(models, 1):
                params_b = m.get("params_b", 0)
                params = f"{params_b:.1f}B" if params_b > 0 else "?"
                marker = " ◆ current" if m["name"] == state["model"] else ""
                t.add_row(f"{i}.", m["name"], params, marker)
            console.print(t)
        else:
            for i, m in enumerate(models, 1):
                cur = " <" if m["name"] == state["model"] else ""
                print(f"  {i}. {m['name']}{cur}")

    elif name == "/cd":
        p = Path(arg or ".").expanduser().resolve()
        if p.is_dir():
            WORKDIR = str(p)
            tiny = state["profile"]["num_predict"] <= 512
            ctx.system = build_system_prompt(WORKDIR, tiny=tiny)
            p_ok(f"Working directory: {WORKDIR}")
        else:
            p_err(f"Directory not found: {arg}")

    elif name == "/clear":
        ctx.clear()
        p_ok("Context cleared.")

    elif name == "/ctx":
        p_info(ctx.stats())

    elif name == "/tokens":
        p_info(ctx.token_stats())

    elif name == "/usage":
        # Load persistent stats
        stats_dir = os.path.join(os.path.expanduser("~"), "Documents", "FORGE_agent_memory")
        stats_path = os.path.join(stats_dir, "usage_stats.json")
        raw_data = {"total_in": 0, "total_out": 0, "sessions": 0}
        
        if os.path.exists(stats_path):
            try:
                with open(stats_path, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    if isinstance(content, list):
                        # Support legacy list format with multiple key variants
                        total_in = 0
                        total_out = 0
                        for entry in content:
                            total_in += entry.get("prompt_tokens", entry.get("p", 0))
                            total_out += entry.get("completion_tokens", entry.get("c", 0))
                        raw_data = {"total_in": total_in, "total_out": total_out, "sessions": len(content)}
                    elif isinstance(content, dict):
                        raw_data = content
            except: pass
        
        total_in = raw_data.get("total_in", 0)
        total_out = raw_data.get("total_out", 0)
        total = total_in + total_out
        sessions = raw_data.get("sessions", 0)
        saved_usd = (total / 1_000_000) * 0.15 # Approx savings vs cloud

        if HAS_RICH:
            # Dashboard UI
            console.print(Panel(
                Text.assemble(
                    (" FORGE ", "bold white bg:#FFA000"),
                    (" USAGE DASHBOARD ", "bold #FFA000"),
                    (f"| {sessions} sessions", "dim")
                ),
                border_style="#FFA000", padding=(0, 1)
            ))

            table = Table(box=rich_box.SIMPLE, show_header=True, header_style="bold cyan", expand=True)
            table.add_column("Metric", style="white")
            table.add_column("Tokens", justify="right", style="cyan")
            table.add_column("Ratio", justify="right", style="dim")

            p_percent = (total_in / total * 100) if total > 0 else 0
            c_percent = (total_out / total * 100) if total > 0 else 0

            table.add_row("Input (Prompt)", f"{total_in:,}", f"{p_percent:.1f}%")
            table.add_row("Output (Completion)", f"{total_out:,}", f"{c_percent:.1f}%")
            table.add_section()
            table.add_row("[bold white]Total Tokens[/bold white]", f"[bold white]{total:,}[/bold white]", "100%")
            console.print(table)

            if total > 0:
                p_bar = "━" * int(p_percent / 4)
                c_bar = "━" * int(c_percent / 4)
                console.print(f"  [cyan]{p_bar}[/cyan][magenta]{c_bar}[/magenta]")
                console.print(f"  [dim]Input vs Output ratio[/dim]\n")

            console.print(Panel(
                f"[bold green]Estimated Savings: ${saved_usd:.4f} USD[/bold green]\n"
                f"[dim]Based on local execution vs cloud API rates[/dim]",
                border_style="green", title="Wallet", title_align="left"
            ))
        else:
            print(f"--- USAGE DASHBOARD ({sessions} sessions) ---")
            print(f"  Input:  {total_in:,}")
            print(f"  Output: {total_out:,}")
            print(f"  Total:  {total:,}")
            print(f"  Estimated Savings: ${saved_usd:.4f} USD")

    elif name == "/mode":
        p_info(f"Execution mode: {EXEC_MODE}  (auto | ask | manual)")

    elif name == "/auto":
        EXEC_MODE = "auto"
        p_ok("Auto mode: executing all tools without confirmation")

    elif name == "/ask":
        EXEC_MODE = "ask"
        p_ok(f"Ask mode: confirming {SAFE_TOOLS} auto, others ask")

    elif name == "/manual":
        EXEC_MODE = "manual"
        p_ok("Manual mode: confirming all tool execution")

    elif name == "/profile":
        prof = state["profile"]
        if HAS_RICH:
            t = Table(box=None, show_header=False, padding=(0, 2))
            t.add_column("k", style="dim")
            t.add_column("v", style="cyan")
            for k, v in prof.items():
                t.add_row(k, str(v))
            console.print(t)
        else:
            for k, v in prof.items():
                print(f"  {k}: {v}")

    elif name == "/tools":
        if HAS_RICH:
            t = Table(box=None, show_header=False, padding=(0, 2))
            t.add_column("name", style="cyan", width=10)
            t.add_column("params", style="dim", width=30)
            t.add_column("desc", style="")
            for tn, (_, desc, params) in TOOLS.items():
                t.add_row(tn, params, desc)
            console.print(t)
        else:
            for tn, (_, desc, params) in TOOLS.items():
                print(f"  {tn}({params}): {desc}")

    elif name == "/read":
        if arg:
            result = tool_read(arg)
            lang = Path(arg).suffix.lstrip(".") or "text"
            if HAS_RICH:
                console.print(Syntax(result, lang, theme="monokai", line_numbers=False))
            else:
                print(result)
        else:
            p_warn("Usage: /read <file>")

    elif name == "/shell":
        if arg:
            result = tool_shell(arg)
            if HAS_RICH:
                console.print(Syntax(result, "bash", theme="monokai"))
            else:
                print(result)
        else:
            p_warn("Usage: /shell <command>")

    else:
        p_warn(f"Unknown command: {name}  (try /help)")

    return state


# ---------------------------------------------------------------------------
# Post-load banner
# ---------------------------------------------------------------------------

def print_ready_banner(model: str, base_url: str, profile: dict, workdir: str):
    if HAS_RICH:
        p_separator()
        console.print(
            f"  [dim]ollama[/dim]  [green]●[/green] {base_url}\n"
            f"  [dim]model [/dim]  [cyan]{model}[/cyan]  [dim]({profile['label']})[/dim]\n"
            f"  [dim]dir   [/dim]  [yellow]{workdir}[/yellow]\n"
            f"  [dim]context[/dim] {profile['max_context']} msgs · {profile['max_tool_output']} chars tool output"
        )
        p_separator()
        console.print("  [dim]Type your task, or /help for commands[/dim]\n")
    else:
        print("-" * 50)
        print(f"  ollama:  {base_url}")
        print(f"  model:   {model}  ({profile['label']})")
        print(f"  dir:     {workdir}")
        print("-" * 50)
        print("  Type your task, or /help for commands\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    global WORKDIR, MAX_TOOL_OUTPUT

    preselect_model = os.getenv("MODEL", "")
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] in ("-m", "--model") and i + 1 < len(args):
            preselect_model = args[i + 1]; i += 2
        elif args[i] in ("-d", "--dir") and i + 1 < len(args):
            WORKDIR = os.path.abspath(args[i + 1]); i += 2
        elif args[i] in ("-h", "--help"):
            print(f"forge v{VERSION}  —  local AI coding agent")
            print("Usage: python forge.py [-m model] [-d dir]")
            print("  -m  Model name (shows picker if omitted)")
            print("  -d  Working directory (default: .)")
            sys.exit(0)
        else:
            i += 1

    # -- Startup animation ----------------------------------------------
    animate_startup()

    # -- Connection to Ollama -------------------------------------------
    base_url = spinner_task("connecting to ollama", detect_ollama)

    # -- Increment session count ----------------------------------------
    try:
        stats_dir = os.path.join(os.path.expanduser("~"), "Documents", "FORGE_agent_memory")
        os.makedirs(stats_dir, exist_ok=True)
        stats_path = os.path.join(stats_dir, "usage_stats.json")
        data = {"total_in": 0, "total_out": 0, "sessions": 0}
        if os.path.exists(stats_path):
            with open(stats_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        data["sessions"] = data.get("sessions", 0) + 1
        with open(stats_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except: pass

    if not base_url:
        p_err("Ollama not found on any address.")
        p_err("Start it with: ollama serve")
        sys.exit(1)

    p_ok(f"ollama connected  →  {base_url}")
    console.print() if HAS_RICH else None

    # -- Loading models -------------------------------------------------
    models_list = spinner_task("loading models", get_models, base_url)

    # -- Model selection ------------------------------------------------
    model_name = choose_model(models_list, preselect=preselect_model)
    # Find the model dict for extra info, or use name for backward compat
    model_dict = next((m for m in models_list if m["name"] == model_name), None) if models_list and isinstance(models_list[0], dict) else None
    profile = model_profile(model_dict if model_dict else model_name)

    # -- Init -----------------------------------------------------------
    tiny = profile["num_predict"] <= 512
    system = build_system_prompt(WORKDIR, tiny=tiny)
    ctx = ContextWindow(system, max_msgs=profile["max_context"], max_tokens=profile["context_length"])

    state = {
        "model": model_name,
        "base_url": base_url,
        "profile": profile,
        "models_list": models_list,
    }

    print_ready_banner(model_name, base_url, profile, WORKDIR)

    # -- Main loop ------------------------------------------------------
    while True:
        try:
            if HAS_RICH:
                # Stylish prompt like Claude Code
                prompt_label = Text.assemble(
                    (" forge ", "bold white bg:#FFA000"),
                    (" ", "default"),
                    (f"{os.path.basename(WORKDIR)}", "blue italic"),
                    (" > ", "bold #FFA000")
                )
                user_input = Prompt.ask(prompt_label).strip()
            else:
                user_input = input(f"forge:{os.path.basename(WORKDIR)}> ").strip()
        except (KeyboardInterrupt, EOFError):
            if HAS_RICH:
                console.print("\n  [dim]bye.[/dim]\n")
            else:
                print("\n  bye.\n")
            break


        if not user_input:
            continue

        if user_input.startswith("/"):
            state = handle_slash(user_input, ctx, state)
            continue

        console.print() if HAS_RICH else None
        agentic_loop(user_input, ctx, state["model"], state["base_url"], state["profile"])
        console.print() if HAS_RICH else None
        show_status_bar(state["model"], state["profile"], WORKDIR, ctx)


if __name__ == "__main__":
    main()
