from ui.themes import console
from ui.input import Prompt

def tool_ask_choice(question: str, options: list) -> str:
    console.print(f"\n[yellow]?[/yellow] [bold]{question}[/bold]")
    for i, opt in enumerate(options, 1):
        console.print(f"  [cyan]{i}.[/cyan] {opt}")
    raw = Prompt.ask("  Select", default="1")
    if raw.isdigit() and 1 <= int(raw) <= len(options):
        return f"User selected: {options[int(raw)-1]}"
    return f"User response: {raw}"
