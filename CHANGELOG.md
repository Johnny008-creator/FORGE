# Changelog

All notable changes to Forge will be documented in this file.

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
