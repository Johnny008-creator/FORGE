#!/usr/bin/env python3
import os, sys

# Ensure Forge modules are findable when run from outside the root directory
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from core.agent import ContextWindow, agentic_loop, build_prompt
from providers.detect import auto_detect_provider
from ui import display, input, themes
from config.settings import Settings
from config.validator import validate_startup
from utils.counter import TokenCounter

def handle_cmd(cmd, ctx, settings, counter):
    if cmd == "/exit": sys.exit(0)
    elif cmd == "/clear": 
        ctx.messages = []; display.p_ok("Context cleared.")
    elif cmd in ["/usage", "/tokens"]: 
        display.p_info(counter.format_usage())
    elif cmd.startswith("/mode"):
        settings.exec_mode = cmd.split()[1] if len(cmd.split()) > 1 else settings.exec_mode
        from tools import executor
        executor.EXEC_MODE = settings.exec_mode
        display.p_info(f"Mode: {settings.exec_mode}")
    elif cmd.startswith("/cd"):
        path = cmd.split()[1] if len(cmd.split()) > 1 else "."
        try: os.chdir(path); settings.workdir = os.getcwd(); display.p_ok(f"Dir: {settings.workdir}")
        except Exception as e: display.p_err(f"CD error: {e}")
    return True

def main():
    settings = Settings()
    display.animate_startup()
    p_name, provider = auto_detect_provider()
    if not provider: display.p_err("Ollama not found."); sys.exit(1)
    
    models = provider.get_models()
    settings.model_name = input.model_picker(models)
    if not validate_startup(settings): sys.exit(1)
    
    from tiers.manager import get_tier_module
    m_dict = next(m for m in models if m["name"] == settings.model_name)
    tier = get_tier_module(m_dict["params_b"])
    
    ctx = ContextWindow(build_prompt(tier, settings.workdir))
    counter = TokenCounter()
    display.p_info(f"Model: {settings.model_name} ({tier.LABEL}) | Provider: {p_name}")
    display.p_separator()

    while True:
        try:
            prompt = f" forge {os.path.basename(os.getcwd())} > "
            inp = input.Prompt.ask(prompt).strip()
            if not inp: continue
            if inp.startswith("/"): handle_cmd(inp, ctx, settings, counter)
            else:
                agentic_loop(inp, ctx, settings.model_name, provider, tier, counter)
                display.p_separator()
        except KeyboardInterrupt: break

if __name__ == "__main__": main()
