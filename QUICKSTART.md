# Forge Quick Start

## Installation

```bash
pip install requests rich
```

Ensure Ollama is running:
```bash
ollama serve
```

## First Run

```bash
python forge.py
```

It will:
1. Auto-detect Ollama provider
2. Show available models with size details
3. Pick a model (interactive picker)
4. Start an agentic session optimized for the selected model's Tier

## Common Tasks

### 1. Auto Mode (Full Autonomous)
```
forge> /auto
forge> list all Python files in this directory
→ model calls list() tool automatically, no confirmation
```

**Use when**: You trust the model and want maximum speed.

### 2. Ask Mode (Default)
```
forge> /ask
forge> run the tests
→ model suggests shell("pytest")
→ you see: "? SHELL: pytest [y/N]: "
→ you type: y
```

**Use for**: Safety — confirm destructive operations before they happen.

### 3. Manual Mode (Maximum Safety)
```
forge> /manual
forge> read setup.py
→ you see: "? READ: path='setup.py' [y/N]: "
→ you type: y
```

**Use when**: Working with untrusted or experimental models.

## How Model Tiers Work

Forge automatically adapts to the selected model's size:

- **Tiny (< 1.5B)**: Strict JSON, 4-message history, aggressive repair.
- **Small (1.5B - 4B)**: Standard logic, 8-message history.
- **Medium (4B - 14B)**: Reasoning enabled, 12-message history.
- **Large (> 14B)**: Maximum context (20+ messages), complex multi-step plans.

## Tips & Tricks

**See what's happening**:
```
/usage    # Show session token consumption
/tokens   # Alias for usage
/mode     # Show current execution mode
```

**Direct context control**:
```
/clear    # Clear conversation history (complete reset)
/cd <dir> # Change working directory
/exit     # Quit Forge
```

## Troubleshooting

**"Ollama not found"**:
- Ensure `ollama serve` is running.
- Check `http://localhost:11434` in your browser.

**Model won't generate tool calls**:
- Switch to a larger model using a different prompt or restarting Forge.
- Ensure your instructions are concrete and technical.

## Next Steps

- Read `ARCHITECTURE.md` for the technical overview.
- Check `AGENTS.md` before making code changes.
- Explore `tools/` to see available capabilities.
