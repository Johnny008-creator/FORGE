import os
from pathlib import Path

WORKDIR = os.getcwd()

def tool_list(path: str = ".", pattern: str = "*") -> str:
    base = Path(WORKDIR) / path if not Path(path).is_absolute() else Path(path)
    try:
        res = [f"{'[D]' if f.is_dir() else '[F]'} {f.relative_to(base)}" 
               for f in sorted(base.rglob(pattern)) 
               if not any(s in f.parts for s in {".git", "__pycache__", "node_modules"})]
        return "\n".join(res[:100]) or "(empty)"
    except Exception as e: return f"List error: {e}"

def tool_search(pattern: str, path: str = ".", file_glob: str = "*") -> str:
    base = Path(WORKDIR) / path if not Path(path).is_absolute() else Path(path)
    res = []
    try:
        for f in sorted(base.rglob(file_glob)):
            if f.is_file() and ".git" not in f.parts:
                try:
                    for i, l in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                        if pattern.lower() in l.lower():
                            res.append(f"{f.relative_to(base)}:{i}: {l.strip()}")
                except: pass
        return "\n".join(res) if res else "No matches."
    except Exception as e: return f"Search error: {e}"
