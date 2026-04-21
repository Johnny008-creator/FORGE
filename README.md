# 🛠️ Forge — Local AI Coding Agent

[![Version](https://img.shields.io/badge/version-0.7.0-blue.svg)](https://github.com/Johnny008-creator/FORGE)
[![Ollama](https://img.shields.io/badge/powered%20by-Ollama-orange.svg)](https://ollama.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()

Forge is a high-performance, lightweight CLI agent designed to bring **Claude Code-like capabilities** to your local machine. It works 100% offline using Ollama, optimized for everything from tiny 0.5B models to large-scale reasoning engines.

---

## ✨ New in v0.7.0: The Modular Framework Update

- 🏗️ **Scalable Architecture**: Entire project refactored into modular components (`core`, `providers`, `tools`, `ui`, `utils`, `tiers`).
- 📡 **Provider Abstraction**: Decoupled AI backend (Ollama) enabling future multi-provider support (OpenAI, Anthropic).
- 🧩 **Independent Tiers**: Each model group has dedicated logic, system prompts, and context limits for maximum stability.
- 🛡️ **Resilient Core**: Built-in "Sloppy JSON" repair and strict argument filtering to handle 0.5B model hallucinations.
- 🪝 **Hook API**: New plugin system for extending agent behavior without modifying the core codebase.
- 🧪 **Validation Suite**: Automated environment checks and comprehensive test coverage in `tests/`.

---

## 🚀 Installation & Usage

### 1. Requirements
*   **Python 3.10+**
*   **Ollama** (installed and reachable)

### 2. Quick Install
```bash
git clone https://github.com/Johnny008-creator/FORGE.git
cd FORGE
pip install -e .
```

### 3. Start Forge
```bash
forge                          # Interactive model picker
forge -m qwen2.5:7b            # Use specific model
forge -d /path/to/project      # Set working directory
```

---

## 🛠️ Built-in Capabilities
Forge can manipulate your environment using these robust tools:

| Tool | Description |
| :--- | :--- |
| `read` | Read files with line numbers for precise context. |
| `patch` | Surgical code replacement with unified diff preview. |
| `write` | Create or overwrite entire files with complete code. |
| `mkdir` | Safely create directory structures (recursively). |
| `ask_choice` | Interactive menu for picking between multiple options. |
| `shell` | Execute any terminal command (with confirmation). |
| `list` | Recursive file and directory listing. |
| `search` | Global text search (grep) across the codebase. |

---

## 💬 Slash Commands
Type these directly into the Forge prompt:
*   `/usage` — **New!** Show persistent lifetime usage statistics and savings.
*   `/compact` — Summarize conversation to save context space.
*   `/tokens` — Show session token statistics.
*   `/mode` — Switch between `auto`, `ask`, and `manual` execution modes.
*   `/model` — Switch models on the fly.
*   `/clear` — Reset conversation history.

---

## 📚 Project History
Detailed release notes for every version:
- [**v0.6.0 — The Claude Code Update**](docs/v0.6.0.md)
- [v0.5.0 — Agentic Transition](docs/v0.5.0.md)
- [v0.4.0 — Model Detection & UI](docs/v0.4.0.md)

---
*Developed by Johnny008-creator*
