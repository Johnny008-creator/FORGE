from rich.prompt import Prompt
from rich.table import Table
from ui.themes import console

def ask_confirm(name: str, args: dict) -> bool:
    display = f"{name}({str(args)[:50]})"
    ans = Prompt.ask(f"  [yellow]?[/yellow] {name.upper()}: [cyan]{display}[/cyan] [dim][Y/n][/dim]", default="y")
    return ans.lower() in ["y", "yes", ""]

def model_picker(models: list) -> str:
    if not models: return ""
    t = Table(box=None, show_header=False, padding=(0, 2))
    for i, m in enumerate(models, 1):
        params = f"{m.get('params_b', 0):.1f}B"
        t.add_row(f"{i}.", m["name"], params, f"{m.get('size_mb', 0)}MB")
    
    console.print("\n  [bold]Available models[/bold]")
    console.print(t)
    
    choices = [str(i) for i in range(1, len(models)+1)] + [m["name"] for m in models]
    ans = Prompt.ask("  Select model number or name", choices=choices, default="1")
    
    if ans.isdigit():
        return models[int(ans)-1]["name"]
    return ans
