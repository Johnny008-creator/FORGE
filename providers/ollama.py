import requests
import json
import time
import random
from providers.base import BaseProvider
from ui.themes import console, FLOWER_SPINNER, ACTIVITY_WORDS
from rich.live import Live
from rich.text import Text
from rich.console import Group

class OllamaProvider(BaseProvider):
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    def detect(self) -> str:
        for url in ["http://localhost:11434", "http://127.0.0.1:11434"]:
            try:
                if requests.get(f"{url}/api/tags", timeout=1).status_code == 200:
                    self.base_url = url
                    return url
            except: pass
        return ""

    def get_models(self) -> list:
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=5)
            models = r.json().get("models", [])
            enriched = []
            for m in models:
                d = m.get("details", {})
                ps = d.get("parameter_size", "7B").strip().upper()
                pb = float(ps.replace("M",""))/1000.0 if "M" in ps else (float(ps.replace("B","")) if "B" in ps else 7.0)
                enriched.append({
                    "name": m["name"], "params_b": pb, 
                    "family": d.get("family", "?"), "size_mb": m.get("size", 0)//1048576
                })
            return sorted(enriched, key=lambda x: x["params_b"])
        except: return []

    def stream_chat(self, messages: list, model: str, profile: dict) -> tuple:
        payload = {"model": model, "messages": messages, "stream": True, "options": {"temperature": profile.get("temperature", 0.1), "num_predict": profile.get("num_predict", 1024)}}
        try:
            r = requests.post(f"{self.base_url}/api/chat", json=payload, stream=True, timeout=120)
            full_text = []; c_tokens = 0; start_time = time.time(); spin_idx = 0
            
            def make_layout(status, footer):
                header = Text.assemble((f"  {FLOWER_SPINNER[spin_idx]} ", "#FFA000"), (f"{model} ", "cyan"), (f"| {status} ", "dim"))
                return Group(header, Text("".join(full_text)), Text(f"  {footer}", style="dim italic"))

            with Live(make_layout(random.choice(ACTIVITY_WORDS), ""), console=console, refresh_per_second=12) as live:
                for line in r.iter_lines():
                    if not line: continue
                    chunk = json.loads(line)
                    token = chunk.get("message", {}).get("content", "")
                    if token:
                        full_text.append(token); c_tokens += 1; spin_idx = (spin_idx + 1) % len(FLOWER_SPINNER)
                        el = time.time() - start_time
                        live.update(make_layout(f"{el:.1f}s", f"{c_tokens} tok · {c_tokens/max(0.1,el):.1f} t/s"))
                    if chunk.get("done"):
                        return "".join(full_text), {"prompt": chunk.get("prompt_eval_count", 0), "completion": chunk.get("eval_count", 0)}
            return "".join(full_text), {"prompt": 0, "completion": c_tokens}
        except Exception as e: return f"Error: {e}", {"prompt": 0, "completion": 0}
