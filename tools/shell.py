import subprocess
import os

WORKDIR = os.getcwd()

def tool_shell(cmd: str, timeout: int = 30) -> str:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=int(timeout), cwd=WORKDIR)
        return (r.stdout + r.stderr) + f"\n[exit: {r.returncode}]"
    except Exception as e: return f"Shell error: {e}"
