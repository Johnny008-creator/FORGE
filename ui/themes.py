from rich.console import Console

VERSION = "0.7.0"
CODENAME = "forge"
TAGLINE = "local AI coding agent"

FORGE_LOGO = r"""
  ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
  █████╗  ██║   ██║██████╔╝██║  ███╗█████╗  
  ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  
  ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
  ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
"""

ACTIVITY_WORDS = [
    "Synthesizing thoughts", "Polishing code", "Consulting the binary gods",
    "Rerouting power to logic", "Analyzing patterns", "Waking up neural nets",
    "Optimizing context", "Thinking really hard", "Brewing coffee for the AI",
    "Aligning sub-tokens", "Scanning repository", "Parsing intentions"
]

FLOWER_SPINNER = ["◐", "◓", "◑", "◒", "◌", "◍"]

console = Console()

def supports_unicode() -> bool:
    try:
        "⠋⣾🌟⟳".encode(sys.stdout.encoding or "utf-8")
        return True
    except:
        return False

SUPPORTS_UNICODE = supports_unicode()
