# Changelog

All notable changes to Forge will be documented in this file.

## [0.7.0] — 2026-04-21
### Added
- **Modular Framework Rewrite**: The entire project has been refactored into a scalable modular architecture (`core`, `providers`, `tools`, `ui`, `utils`, `config`, `tiers`).
- **Provider Abstraction**: Introduced `BaseProvider` system, isolating Ollama logic and enabling future backend integrations (OpenAI, Anthropic).
- **Independent Model Tiers**: Each model group (Tiny, Small, Medium, Large) now lives in its own configuration file with dedicated system prompts and context limits.
- **Hook API**: New plugin-ready system with `before_tool`, `after_tool`, and `on_response` hooks.
- **Robust Argument Filtering**: Tools now use `inspect.signature` to automatically ignore hallucinated arguments from smaller models.
- **Surgical Edit Mandate**: New development protocol enforced via `AGENTS.md` and `ARCHITECTURE.md`.
- **Validation Suite**: Added `config/validator.py` for environment checks and a comprehensive `tests/` suite.

### Fixed
- Fixed **Infinite Loops**: Improved nudging logic and aggressive context trimming for 0.5B models.
- Fixed **Path Safety**: Added path validation to all file tools to prevent root-directory write attempts.
- Fixed **Import Conflicts**: Resolved circular dependencies via a clean import flow.

## [0.6.0] — 2026-04-19

### Added
- **Claude Code Style UI**: Complete overhaul of the streaming interface with a 3-part layout (Header, Body, Footer).
- **Interactive Decision Making (`ask_choice`)**: New tool allowing the model to present multiple options to the user via a stylish menu.
- **Auto-Ollama Startup**: Forge now automatically detects if the Ollama server is running and attempts to start it in the background if needed.
- **Persistent Usage Tracking**: Total token consumption and session counts are now saved to `usage_stats.json` in the user's Documents.
- **Usage Dashboard (`/usage`)**: New command to display a visual summary of lifetime token usage, ratios, and estimated cost savings.
- **Enhanced Reliability for Tiny Models**: Optimized system prompts (Analyze -> Plan -> Act) and "Choice-Loop" prevention for models under 3B parameters.

### Fixed
- Improved **Ctrl+C handling**: Interrupting a stream or an interactive menu now returns safely to the prompt instead of crashing the application.
- Fixed **`patch` tool bug** where diff generation would fail on certain Python versions due to generator subscripting.
- Corrected **Markdown JSON extraction** to better handle tool calls nested inside code blocks.

### Changed
- Refactored `agentic_loop` to provide clearer feedback during plan execution.
- Updated main prompt with current directory context and a more modern look.

## [0.5.0-dev] — 2026-04-18
### Added
- **English-Only Transition**: Entire codebase, comments, and CLI translated to English for a global professional standard.
- **Windows Directory Control (`mkdir`)**: New tool `mkdir` allows safe creation of directory structures (handling parent folders automatically).
- **Context Compacting (`/compact`)**: New slash command to summarize long conversations, freeing up context tokens for tiny models.
- **Dynamic Context Trimming**: Integrated Ollama API `context_length` to dynamically manage sliding window based on model capabilities.

### Changed
- Refactored `ContextWindow` to use token-based estimation (heuristic) alongside message limits.
- Improved Windows compatibility for Unicode animations and file paths.

## [0.4.0] — 2026-04-17
### Added
- Real Model Detection via Ollama API (params, quant, family).
- Claude Code-like animations (spinners, tool status icons).
- Windows Unicode safety with ASCII fallbacks.

## [0.3.0] — 2026-04-16
### Added
- Execution Modes: `auto`, `ask`, `manual`.
- Token counting and real-time velocity metrics.
- Support for tiny (0.5B) model prompting with few-shot examples.
