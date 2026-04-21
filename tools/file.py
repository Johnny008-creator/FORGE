import os
import shutil
from pathlib import Path

WORKDIR = os.getcwd()

def tool_read(path: str, start_line: int = 1, end_line: int = 0) -> str:
    p = Path(WORKDIR) / path if not Path(path).is_absolute() else Path(path)
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        sl, el = max(1, int(start_line)), int(end_line)
        chunk = lines[sl-1:el] if el > 0 else lines[sl-1:]
        res = [f"{sl+i:5}│ {l}" for i, l in enumerate(chunk)]
        return f"[{path} {len(lines)} lines]\n" + "\n".join(res)
    except Exception as e: return f"Read error: {e}"

def tool_write(path: str, content: str) -> str:
    p = Path(WORKDIR) / path if not Path(path).is_absolute() else Path(path)
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Written: {path}"
    except Exception as e: return f"Write error: {e}"

def tool_patch(path: str, old_text: str, new_text: str) -> str:
    p = Path(WORKDIR) / path if not Path(path).is_absolute() else Path(path)
    try:
        orig = p.read_text(encoding="utf-8")
        if old_text not in orig: return f"Error: text not found in {path}"
        p.write_text(orig.replace(old_text, new_text, 1), encoding="utf-8")
        return f"Patched: {path}"
    except Exception as e: return f"Patch error: {e}"

def tool_delete(path: str) -> str:
    p = Path(WORKDIR) / path
    try:
        if p.is_file(): p.unlink(); return f"Deleted: {path}"
        if p.is_dir(): shutil.rmtree(p); return f"Deleted dir: {path}"
        return "Not found."
    except Exception as e: return f"Delete error: {e}"

def tool_mkdir(path: str) -> str:
    try: os.makedirs(Path(WORKDIR)/path, exist_ok=True); return f"Created: {path}"
    except Exception as e: return f"Mkdir error: {e}"
