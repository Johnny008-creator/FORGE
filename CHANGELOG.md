# Changelog

## v0.4.0 — Auto Model Detection & Claude Code Animations (2026-04-18)

### Added

**Auto Model Detection from Ollama API**
- `get_models()` now returns rich model dicts with real data:
  - `params_b` — actual parameter count parsed from Ollama API (e.g., "494.03M" → 0.49B)
  - `quant` — quantization level (Q4_K_M, Q8_0, etc.)
  - `family` — model family (qwen2, mistral, etc.)
  - `size_mb` — model size in megabytes
  - `context_length` — available if provided by API
- `parse_param_size()` — parses "494.03M" or "3.1B" format from Ollama API
- `model_profile()` now accepts both dict (new) and string (backward compatible)
- Model picker shows all details: params, quant, size, family
- Real parameter counts replace regex guessing

**Unicode Detection & Fallback**
- `supports_unicode()` — detects if terminal supports Unicode
- Falls back to ASCII for Windows (braille `⠋` → `|/-\`, arrows `⟳` → `~`, etc.)
- All animations work on Windows cp1250 encoding

**Claude Code-Style Animations**
- `spinner_task()` — uses Rich's `Spinner("dots")` with auto-fallback
  - Supports multiple spinner styles
  - Graceful degradation on Windows
- Tool execution visual feedback:
  - `  ⟳ reading forge.py...` (running)
  - `  ✓ reading forge.py` (success)
  - `  ✗ reading forge.py` (error/cancelled)
- Thinking indicator during model response generation
- Logo animation without disruptive `console.clear()`

**Enhanced p_tool() Output**
- Status parameter: "run", "ok", "err"
- Live updates during execution
- Colored icons: `⟳` (running), `✓` (success), `✗` (error)

### Changed

- Model picker display completely redesigned with quantization, family, size
- `get_models()` behavior — now returns model objects, not just names
- Status icons use Unicode with ASCII fallback

### Fixed

- Windows terminal compatibility for animations
- Unicode encoding issues on Windows cp1250
- Model detection from API instead of regex guessing

### Architecture

- Lines: 1,114 → 1,230 (+116 lines)
- New: `parse_param_size()`, `supports_unicode()`, enhanced `get_models()`, enhanced `choose_model()`
- All animations have Windows/non-Unicode fallback

## v0.3.0 — Execution Modes & Robust Tool Parsing (2026-04-18)

### Added

**Execution Modes**
- `/auto` — Execute all tools automatically without confirmation
- `/ask` — Default mode: safe tools (read/list/search) auto-execute, destructive ops ask for confirmation
- `/manual` — Confirm every single tool execution
- `/mode` — Show current execution mode
- Mode indicator in status bar

**Robust Tool Call Parsing**
Tiny models (0.5B) now supported with multiple parsing strategies:
1. **Standard JSON**: `{"tool":"name","args":{...}}`
2. **Markdown code blocks**: ` ```json {...}``` `
3. **Function calls**: `read("path")` or `shell("cmd", timeout)`

Parser uses depth-first brace matching for nested JSON objects.

**Few-Shot Examples**
- System prompt includes concrete examples for tiny models showing tool call syntax
- Dramatically improves tool-calling reliability on 0.5B models
- Different prompt format for tiny vs regular models

**Improved Tool Execution**
- `should_confirm(tool_name)` — determines if confirmation needed
- `ask_confirm(tool_name, args)` — unified confirmation prompt for all tools
- Better display of tool invocation with parameters

### Changed

- `extract_tool_calls()` now uses multiple strategies instead of single regex
- Status bar now shows execution mode
- Few-shot examples in system prompt for all models

### Fixed

- JSON parsing for nested `{"args":{...}}` structures
- Function-call parsing for tools with positional arguments
- Parameter name extraction from tool definitions

## v0.2.0 — Token Counting & Execution (2026-04-18)

### Added

**Token Statistics**
- Real-time token counting from Ollama API responses
- Display format: `in: 1,234 tok | out: 456 tok | 23.5 tok/s | 2.1s`
- Session total tracking with `/tokens` command
- Live token velocity meter during response streaming
- Per-response timing in seconds

**Command Execution with Confirmation**
- AI models can now propose and execute shell/file tools
- Shell commands require explicit user confirmation before execution
  - Prompt: `? Execute: <command> [y/N]:`
- Read-only tools (read, list, search) execute without confirmation
- Status display when commands are approved/rejected

**New Commands**
- `/tokens` — Show cumulative session token usage (input, output, total)

**Improved Display**
- Status separator after each response
- Token stats formatted with thousand separators
- Live status updates during generation (every 0.5s)
- Better error handling for Windows Unicode issues

**Developer Additions**
- `ContextWindow.add_tokens(prompt, completion)` — Track tokens per response
- `ContextWindow.token_stats()` — Get session total display string
- `stream_chat()` now returns tuple: `(response_text, stats_dict)`
  - `stats_dict` includes: `prompt_tokens`, `completion_tokens`, `tokens_per_sec`, `elapsed`
- `ask_shell_confirm()` — Interactive confirmation for shell execution

### Changed

- System prompt is more concise for tiny models (≤512 token output)
- Stream output shows live token count updates every 0.5 seconds
- Shell tool execution moved to agentic loop for proper confirmation

### Fixed

- Windows encoding issues with Unicode characters in status display
- Fallback to ASCII characters if Unicode rendering fails
- Better error handling in startup animation

### Files

- `forge.py` — +100 lines (0.9K → 1.0K), refactored stream_chat, added ContextWindow.add_tokens
- `README.md` — New comprehensive documentation
- `demo.sh` — Quick demo script with example commands
- `CHANGELOG.md` — This file

## v0.1.0 — Initial Release (2026-04-17)

- Basic Ollama integration
- Tool calling via JSON in responses
- Auto-detected model profiling
- Rich terminal UI with animations
- Slash commands for navigation and settings
