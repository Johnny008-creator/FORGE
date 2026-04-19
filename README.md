# 🛠️ Forge — Local AI Coding Agent

[![Version](https://img.shields.io/badge/version-0.6.0-blue.svg)](https://github.com/Johnny008-creator/FORGE)
[![Ollama](https://img.shields.io/badge/powered%20by-Ollama-orange.svg)](https://ollama.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()

Forge is a high-performance, lightweight CLI agent designed to bring **Claude Code-like capabilities** to your local machine. It works 100% offline using Ollama, optimized for everything from tiny 0.5B models to large-scale reasoning engines.

---

## ✨ New in v0.6.0: The "Claude Code" Overhaul

- 🎨 **Modern Streaming UI**: A three-part layout featuring a "Flower" spinner, real-time thinking metrics, and clean response bodies (hidden raw JSON).
- 🧠 **Interactive Decisions (`ask_choice`)**: Forge now asks for your input when faced with multiple paths, giving you full architectural control.
- ⚡ **Auto-Ollama Engine**: Automatically detects and launches the Ollama server in the background if it's not running.
- 📊 **Usage Dashboard**: Track your lifetime token consumption and see how much you've saved vs. cloud APIs with the new `/usage` command.
- 🛡️ **Improved Stability**: Robust Ctrl+C handling and refined error self-correction logic.

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
