# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2025-11-23

### Fixed
- **Windows Compatibility**: Fixed `ModuleNotFoundError` for `resource` module on Windows by making the import and file handle limit adjustment conditional (Unix-only). The application now runs on both Windows and Unix-based systems.

### Changed
- **Puzzle Selection**: Updated `SELECTED_PROBLEMS` in `main.py` to include specific test puzzles (28a6681f, 2b83f449, 4e34c42c, b9e38dc0) for initial Gemini 3 Pro Preview model testing.
- **Cross-Platform Support**: Replaced `resource` module import with conditional import based on `sys.platform` detection.

## [1.0.0] - 2025-01-20

### Added
- Initial implementation of Poetiq's ARC-AGI solver reproduction
- Iterative LLM-based code generation for abstract reasoning tasks
- Support for multiple LLM providers (OpenAI, Anthropic, Google Gemini, xAI, Groq)
- Parallel expert solving with voting aggregation system
- Sandboxed Python code execution environment
- Kaggle submission format output
- Configurable solver parameters and prompts
- Rate limiting and retry logic for LLM API calls
- Scoring system for training and evaluation tasks
- Support for ARC Prize 2024/2025 datasets

---

## Version History

- **1.0.1** - Windows compatibility fix + test configuration
- **1.0.0** - Initial stable release
