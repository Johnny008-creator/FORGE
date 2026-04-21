import time
import random
import threading
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from rich import box as rich_box
from ui.themes import console, FORGE_LOGO, TAGLINE, VERSION, ACTIVITY_WORDS, FLOWER_SPINNER, SUPPORTS_UNICODE

def animate_startup():
    logo_text = Text(FORGE_LOGO, style="bold #FFA000")
    console.clear()
    console.print()
    with Live(Panel(logo_text, box=rich_box.ROUNDED, padding=(0, 2), border_style="#FFA000"),
              console=console, refresh_per_second=10) as live:
        time.sleep(0.5)
        live.update(Panel(Text.assemble(logo_text, (f"\n{TAGLINE}  v{VERSION}", "dim")),
                          box=rich_box.ROUNDED, padding=(0, 2), border_style="#FFA000"))
        time.sleep(0.5)
    console.print()

def spinner_task(label: str, func, *args, **kwargs):
    result_container = [None]
    done = threading.Event()
    def worker():
        result_container[0] = func(*args, **kwargs)
        done.set()
    threading.Thread(target=worker, daemon=True).start()
    with Live(Spinner("dots", text=f" {label}", style="dim"), console=console, refresh_per_second=12):
        done.wait()
    return result_container[0]

def p_ok(msg): console.print(f"  [green]✓[/green] {msg}")
def p_err(msg): console.print(f"  [bold red]✗[/bold red] {msg}")
def p_warn(msg): console.print(f"  [yellow]![/yellow] {msg}")
def p_info(msg): console.print(f"  [dim]{msg}[/dim]")

def p_tool(name, args_str, status="run"):
    icon = "●" if status == "run" else ("✓" if status == "ok" else "✗")
    color = "#FFA000" if status == "run" else ("green" if status == "ok" else "bold red")
    console.print(f"  [{color}]{icon}[/{color}] [cyan]{name}[/cyan][dim]({args_str})[/dim]")

def p_tool_result(msg): console.print(f"  [dim]  {msg}[/dim]")
def p_separator(): console.print("[dim]" + "─" * 60 + "[/dim]")
