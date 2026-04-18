# Forge — Local AI Coding Agent

Claude Code-like interface for local Ollama models. Works offline with tiny models like Qwen 0.5B.

## What's New (v0.5.0-dev)

### Context Management & Compacting
- **/compact**: New command to summarize long conversation history into a single paragraph, saving context space for tiny models.
- **Dynamic Context Length**: Automatically detects and respects model context limits from Ollama API.

### New Tools
- **mkdir**: AI can now safely create directory structures (`os.makedirs`).
- **Windows mkdir support**: Robust path handling for Windows environments.

### Execution Modes (Auto/Ask/Manual)
Three execution modes for tool calls:
- **Auto** (`/auto`): Model executes all tools automatically without asking
- **Ask** (`/ask`, default): Safe tools (read, list, search) auto-execute; destructive ops ask for confirmation
- **Manual** (`/manual`): Confirm every tool execution

Status bar shows current mode. Perfect for varying trust levels.

### Robust Tool Parsing
Tiny models (0.5B) often don't format JSON perfectly. Parser now handles:
1. **Standard JSON**: `{"tool":"read","args":{"path":"forge.py"}}`
2. **Markdown code blocks**: ` ```json {...}``` `
3. **Function calls**: `read("forge.py")` or `shell("ls -la")`

### Few-Shot Examples
Tiny models get explicit examples in system prompt showing how to call tools. Massively improves reliability with 0.5B models.

### Token Counting
Real-time token statistics:
- **Per-response**: `in: 1234 tok | out: 456 tok | 23 tok/s | 2.1s`
- **Session totals**: `/tokens` shows cumulative usage
- Live velocity meter during streaming

### Command Execution
AI can suggest and execute shell/file operations:
- **Read-only tools** (read, list, search): execute immediately
- **Destructive tools** (shell, delete, write, patch): requires user confirmation
- Example: Model suggests `ls -la` → you see command → approve with `y`

### Streaming & Animations
- Live token velocity display while generating
- Status separator between response and stats
- Model profile adapts to tiny models (reduced context window, shorter outputs)

## Installation

```bash
pip install requests rich
```

Ensure Ollama is running:
```bash
ollama serve
```

## Usage

### Basic
```bash
python forge.py                          # Interactive model picker
python forge.py -m qwen2.5:0.5b          # Use specific model
python forge.py -d /path/to/project      # Set working directory
```

### Commands
```
/help              Show available commands
/tokens            Show session token totals
/ctx               Show message history stats
/compact           Summarize conversation to save context
/profile           Show current model profile
/mode              Show current execution mode (auto/ask/manual)
/auto              Switch to auto mode (execute all without asking)
/ask               Switch to ask mode (confirm destructive ops)
/manual            Switch to manual mode (confirm all)
/models            List available Ollama models
/model <name>      Switch to different model
/cd <dir>          Change working directory
/clear             Clear conversation history
/read <file>       Read file directly
/shell <cmd>       Run command directly
/exit              Quit
```

## How It Works

1. **Startup**: Detects Ollama, loads models, picks one (or you specify)
2. **Prompt**: You describe the task in English
3. **AI Generates**: Model suggests tool calls as JSON
4. **Tools Execute**: Read files, patch code, run commands
5. **Confirmation**: Destructive ops (shell) need your approval
6. **Stats**: Token count shown after each response
7. **Loop**: AI can use tool results to make follow-up suggestions

## Model Profiles

Profiles are auto-detected from model name:

| Size | Max Context | Max Output | Num Predict | Label |
|------|-------------|-----------|-------------|-------|
| ≤1B | 4 msgs | 800 chars | 512 | tiny |
| ≤3B | 6 msgs | 1200 chars | 768 | small |
| ≤8B | 10 msgs | 2000 chars | 1536 | medium |
| ≤20B | 14 msgs | 3000 chars | 2048 | large |
| >20B | 20 msgs | 5000 chars | 4096 | xlarge |

Tiny models (0.5B) use simplified system prompt.

## Example Session

```
forge> read setup.py

[model output...]
| in: 234  out: 89  12.5 tok/s  0.7s

forge> add debug logging to line 45

[model suggests patch...]
? Execute: patch(setup.py, old_text, new_text) [y/N]: y

forge> /tokens
Session: 2,345 in  1,023 out  3,368 total

forge> /exit
```

## Files

- `forge.py` — main agent (single file, ~1000 lines)
- `README.md` — this file

## Limitations

- Works best with streaming-capable models (Qwen, Mistral, Phi)
- Context window is small for 0.5B models (4-6 messages)
- No multi-file project support yet
- No persistent session history

## Next Steps

Consider adding:
- Persistent session memory (`-save` flag)
- Code search/indexing for large projects
- Parallel tool execution
- Integration with git/version control
- Custom tool definitions
