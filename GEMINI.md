# ♊ Forge Project Context (v0.7.0 Modular)

## 📌 Current State
The project has undergone a complete restructuring into a modular framework. 
- **Version:** 0.7.0
- **Architecture:** Modular (core, providers, tools, ui, config, tiers, plugins).
- **Mandatory Documentation:** `AGENTS.md` (AI rules) and `ARCHITECTURE.md` (diagrams).

## 🛡️ Development Mandates
1. **Surgical Edits:** Use `replace`, never rewrite entire files (unless a necessary refactor).
2. **File Limits:** No file may exceed 200 lines.
3. **Registry Pattern:** New tools are registered in `tools/registry.py`, providers in `providers/registry.py`.
4. **No Circular Imports:** Dependencies flow: `forge.py` -> `core` -> rest.

## 🚀 Next Steps
- Implementation of `providers/openai.py`.
- First plugin in `plugins/`.
- Fuzzy patching in `tools/file.py`.
