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
1. Auto-detect Ollama
2. Show available models
3. Pick default model (or you select)
4. Start interactive session

## Common Tasks

### 1. Auto Mode (Full Autonomous)
```
forge> /auto
forge> list all Python files in this directory
→ model calls list() tool automatically, no confirmation
```

**Use when**: You trust the model and want speed

### 2. Ask Mode (Default)
```
forge> /ask
forge> run the tests
→ model suggests shell("pytest")
→ you see: "? SHELL: pytest [y/N]: "
→ you type: y
```

**Use for**: Safety — confirm destructive operations

### 3. Manual Mode (Maximum Safety)
```
forge> /manual
forge> read setup.py
→ you see: "? READ: path='setup.py' [y/N]: "
→ you type: y
```

**Use when**: Working with untrusted/experimental models

## Example Session

```
forge> /auto
  ✓ Auto mode: executing all tools without confirmation

forge> what files exist?

  >> qwen2.5:0.5b
  Let me list the files in the current directory.
  
  ⟩ list({})
  
  ─────────────────────────────
  in: 234 tok  out: 89 tok  12.5 tok/s  0.7s

forge> /tokens
  Session: 4,567 in  2,341 out  6,908 total

forge> /mode
  Execution mode: auto  (auto | ask | manual)

forge> /ask
  ✓ Ask mode: confirming {read, list, search} auto, others ask

forge> create a test.py file
  
  ⟩ write(path='test.py', content='print("hello")')
  
  ? WRITE: path='test.py', content='print("hello")' [y/N]: y
  
  Written: test.py  (1 lines)
  
  ─────────────────────────────
  in: 156 tok  out: 42 tok  8.3 tok/s  0.5s

forge> /exit
  bye.
```

## How Tiny Models Work

Qwen 0.5B is extremely small (397MB). Key points:

1. **Context limit**: 4 messages max (vs 20 for large models)
2. **Token limit**: Can only output 512 tokens before getting cut off
3. **Tool parsing**: Needs examples (provided in system prompt)
4. **Accuracy**: Lower than big models, but still useful

Best practices:
- Use `/auto` mode for speed
- Give concrete, short instructions
- Check `/tokens` to see remaining context
- Use `/clear` when running out of context
- Read files directly with `/read` to avoid model confusion

## Execution Modes Comparison

| Mode | Safe Tools | Shell | Write/Patch | Delete |
|------|-----------|-------|------------|--------|
| **auto** | Auto | Auto | Auto | Auto |
| **ask** (default) | Auto | Ask | Ask | Ask |
| **manual** | Ask | Ask | Ask | Ask |

## Tips & Tricks

**See what's happening**:
```
/ctx      # Show message history stats
/tokens   # Show session token totals
/profile  # Show model's token/output limits
```

**Direct tool usage** (no AI):
```
/read forge.py          # Read file directly
/shell ls -la           # Run command without AI
/cd /path/to/project    # Change dir
```

**Context management**:
```
/compact                # Summarize history to save space (keep latest messages)
/clear                  # Clear conversation history (complete reset)
/model qwen2.5:3b       # Switch to bigger model if 0.5B is too small
```

**Common Patterns**

**Create directory structures**:
```
forge> create a new directory src/utils
→ model calls mkdir(path="src/utils")
```

**Explore project**:
```
forge> list all files
forge> read main.py
forge> search for TODO
forge> what does this project do?
```

**Modify code**:
```
forge> /ask                              # Switch to safe mode
forge> read config.py                    # Check what we're modifying
forge> update the database URL in line 5 # AI suggests patch
[confirm patch]
```

**Run commands**:
```
forge> /auto                       # Switch to auto
forge> run the unit tests
[auto-executes pytest]
```

## Troubleshooting

**"Ollama not found"**:
- Run `ollama serve` in another terminal
- Check `http://localhost:11434/api/tags` in browser

**Model won't generate tool calls**:
- Check `/profile` — model might be too constrained
- Try `/model` to pick a different one
- Give more explicit instructions

**Out of context**:
- Type `/clear` to reset conversation
- Type `/tokens` to see usage
- Switch to bigger model if needed

**Command didn't execute**:
- Check execution mode: `/mode`
- Switch to `/auto` if you want it to execute automatically
- Confirm with `y` when prompted

## Next Steps

- Read `README.md` for architecture details
- Check `forge.py` comments for tool implementation
- Modify system prompt in `build_system_prompt()` for custom behavior
