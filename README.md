# 🛠️ Forge — Local AI Coding Agent

[![Version](https://img.shields.io/badge/version-0.5.0--dev-blue.svg)](https://github.com/Johnny008-creator/FORGE)
[![Ollama](https://img.shields.io/badge/powered%20by-Ollama-orange.svg)](https://ollama.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()

Forge is a high-performance, lightweight CLI agent designed to bring **Claude Code-like capabilities** to your local machine. It works 100% offline using Ollama, optimized for everything from tiny 0.5B models to large-scale reasoning engines.

---

## ✨ Key Features

- 🧠 **Smart Context Management**: Dynamic token tracking using Ollama API and a `/compact` command to summarize long histories.
- 📁 **Advanced File Control**: Robust toolset (`read`, `patch`, `write`, `mkdir`, `shell`) fully optimized for Windows environments.
- ⚡ **Lightning Fast**: Built for local execution with real-time token velocity metrics and streaming animations.
- 🎨 **Rich Terminal UI**: Interactive animations, status bars, and modern Unicode icons (with ASCII fallbacks).
- 🛡️ **Execution Modes**: Three safety levels (`auto`, `ask`, `manual`) to keep you in control of destructive operations.

---

## 🚀 Quick Start

### 1. Requirements
*   **Python 3.10+**
*   **Ollama** (running locally: `ollama serve`)
*   **Rich & Requests**: `pip install requests rich`

### 2. Installation
```bash
git clone https://github.com/Johnny008-creator/FORGE.git
cd FORGE
```

### 3. Usage
```bash
python forge.py                          # Interactive model picker
python forge.py -m qwen2.5:0.5b          # Use specific model
python forge.py -d /path/to/project      # Set working directory
```

---

## 🛠️ Toolset
Forge can manipulate your environment using these built-in capabilities:

| Tool | Description | Example |
| :--- | :--- | :--- |
| `read` | Read files with line numbers | `read("main.py")` |
| `patch` | Surgical code replacement (safe) | `patch("app.py", "old", "new")` |
| `write` | Create or overwrite entire files | `write("test.js", "console.log('hi')")` |
| `mkdir` | Safely create directory structures | `mkdir("src/components")` |
| `list` | Recursive file listing | `list("src/", "*.py")` |
| `search` | Global text search (grep) | `search("TODO", ".", "*.md")` |
| `shell` | Run any terminal command | `shell("npm test")` |
| `delete` | Remove files or directories | `delete("temp.txt")` |

---

## 💬 Commands
Type these directly in the Forge prompt:
*   `/help` — Show all available commands.
*   `/compact` — **New!** Summarize conversation to save context space.
*   `/tokens` — Show session token statistics.
*   `/mode` — Switch between `auto`, `ask`, and `manual` modes.
*   `/model <name>` — Switch models on the fly.
*   `/clear` — Reset conversation history.

---

## 🗺️ Roadmap (v0.5.0+)

- [x] **Full English UI/UX**
- [x] **Windows Directory Management (`mkdir`)**
- [x] **Dynamic Context Trimming**
- [ ] **Persistent History**: Save sessions to `.history/` files.
- [ ] **Git Integration**: Auto-commit changes with AI-generated messages.
- [ ] **Multi-turn Planning**: Break down complex tasks into sub-steps.

---

## 🤝 Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Developed by Johnny008-creator*
