# 🧠 Forge AI Brain — Architectural Summary (v0.7.0 Modular)

> **IMPORTANT:** Forge has transitioned from a monolith to a **Modular Framework**. Follow the rules in `AGENTS.md` and `ARCHITECTURE.md` strictly.

## 🚀 Current State: The Modular Framework
Forge is now a collection of specialized modules. SRP (Single Responsibility Principle) is the law.

### 🏗️ Directory Map
- `core/`: Brain & Context (`loop.py`, `context.py`, `agent.py`).
- `providers/`: AI backends (`ollama.py`, `base.py`). Add new providers here!
- `tools/`: Atomic tools (`file.py`, `shell.py`, `search.py`, `ask.py`). Register in `tools/registry.py`.
- `ui/`: Rich UI & Input handling (`display.py`, `themes.py`, `input.py`).
- `config/`: System settings & Validation (`settings.py`, `validator.py`).
- `tiers/`: Independent model profiles (Tiny, Small, Medium, Large).
- `plugins/`: Hook-based extension system (`hook_api.py`).

### 🛡️ Development Mandates
1.  **Surgical Edits Only:** No bulk rewrites. Use `replace`.
2.  **Registry-Only Registration:** Tools/Providers must be registered in their respective `registry.py`.
3.  **File Limit:** Keep files under **200 lines**.
4.  **Circular Imports:** Strictly forbidden. Follow the flow: `forge.py` -> `core` -> `rest`.

---

## 🔍 Next Steps (To-Do)
1.  **OpenAI Provider:** Add a new provider in `providers/openai.py` for cloud-based fallback.
2.  **Plugin Implementation:** Create the first real plugin (e.g., `plugins/git_logger.py`) using the Hook API.
3.  **Advanced Tests:** Expand `tests/test_loop.py` to cover complex multi-step scenarios.
4.  **Fuzzy Patching:** Improve `tools/file.py` with fuzzy matching for the `patch` tool.

---
*Last Architectural Sync: April 21, 2026*
