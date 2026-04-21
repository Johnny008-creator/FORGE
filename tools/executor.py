import inspect
from tools import registry
from ui.input import Prompt

EXEC_MODE = "ask"
SAFE_TOOLS = {"read", "list", "search", "ask_choice"}

def run_tool(name: str, args: dict) -> str:
    if name not in registry.TOOLS: return f"Unknown tool: {name}"
    func, param_info = registry.TOOLS[name]
    
    # Simple path validation
    if name in ["read", "write", "patch", "delete", "mkdir"] and not args.get("path"):
        return f"Error: Tool '{name}' requires 'path'."
    
    try:
        sig = inspect.signature(func)
        valid_args = {k: v for k, v in args.items() if k in sig.parameters}
        return func(**valid_args)
    except Exception as e: return f"Tool error: {e}"

def should_confirm(name):
    if EXEC_MODE == "auto": return False
    if EXEC_MODE == "manual": return True
    return name not in SAFE_TOOLS

def ask_confirm(name, args):
    display = f"{name}({str(args)[:50]})"
    ans = Prompt.ask(f"  [yellow]?[/yellow] {name.upper()}: [cyan]{display}[/cyan] [dim][Y/n][/dim]", default="y")
    return ans.lower() in ["y", "yes", ""]
