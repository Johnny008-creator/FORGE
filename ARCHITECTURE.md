# 🏗️ Forge Architecture (v1.0)

This document describes the modular structure of the Forge project and the rules for its expansion.

## 📁 Layer Overview

### 1. Entry Point (`forge.py`)
- The highest layer, the orchestrator.
- Processes CLI arguments and slash commands.
- Initializes UI, Providers, and starts the agentic loop.

### 2. Core (`core/`)
- **`agent.py`**: Export interface for the core.
- **`loop.py`**: The agentic loop itself (The Brain). Decides the next step.
- **`context.py`**: Conversation history management and context trimming.
- **`parser.py`**: Extraction and repair of JSON tool calls from model output.

### 3. Providers (`providers/`)
- Abstraction layer for AI backends.
- Each provider inherits from `BaseProvider`.
- Supports auto-discovery (detecting running services).

### 4. Tools (`tools/`)
- Atomic functions that the agent can call.
- Each file (`file.py`, `shell.py`, `search.py`, `ask.py`) represents a category of tools.
- Registration takes place in `registry.py`.

### 5. Tiers (`tiers/`)
- Model configuration based on size (Tiny, Small, Medium, Large).
- Each Tier has its own context limits and system prompt.

### 6. UI (`ui/`)
- Everything related to the Rich UI.
- Separate themes (`themes.py`), outputs (`display.py`), and inputs (`input.py`).

### 7. Config (`config/`)
- Settings management (`settings.py`) and environment validation (`validator.py`).

## 📊 Dependency Diagram (Import Flow)

```text
forge.py ──▶ core/agent.py ──▶ core/loop.py
  │               │              │
  ▼               ▼              ▼
config/        tiers/         providers/
settings.py    manager.py     base.py
  │               │              │
  ▼               ▼              ▼
utils/         ui/            tools/
counter.py     display.py     executor.py
```

## 📜 Contribution Rules
- **No circular imports:** Follow the diagram above.
- **SRP:** Each function does one thing.
- **Limits:** Max 200 lines per file.
- **Surgical edits:** Change only what is necessary.
- **Tests:** Every new tool or provider must have a test in `tests/`.
