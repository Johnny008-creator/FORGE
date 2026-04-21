# 🤖 Forge AI Agent Protocol (v1.0)

These are mandatory rules for the development and modification of the Forge project. Every AI agent must follow them.

## 🏗️ Architectural Principles
- **Single Responsibility Principle (SRP):** Each file has one clear responsibility.
- **Length Limit:** No file may exceed **200 lines**.
- **Circular Imports:** Strictly forbidden. Dependencies must flow downwards.
- **Surgical Edits:** Do not use bulk rewrites. Use `replace` for targeted changes.

## 🛠️ How to Add a New Tool
1. Create a new file in `tools/` (e.g., `tools/my_tool.py`).
2. Implement the tool function.
3. Register the tool in `tools/registry.py` (import it and add it to the `TOOLS` dict).
4. **IMPORTANT:** Registration takes place EXCLUSIVELY in `tools/registry.py`.

## 📡 How to Add a New Provider
1. Create a new file in `providers/` (e.g., `providers/openai.py`).
2. Implement a class inheriting from `BaseProvider`.
3. Register the provider in `providers/registry.py`.

## 📁 Directory Structure
- `core/`: Agent core and loop.
- `providers/`: Abstractions for different AI backends.
- `tools/`: Modular tools (always one file = one category).
- `tiers/`: Specific configurations for different model sizes.
- `ui/`: Everything related to the Rich UI and user interaction.
- `utils/`: Helper functions and statistics.
- `config/`: Settings and validation.
- `plugins/`: Hook system for extensions.

## 🔬 Testing
Every new piece of code must have a corresponding test in `tests/`. Verify integrity with `pytest` before completing a task.
