# CHANGELOG

<!-- version list -->

## v1.2.0 (2025-12-28)

### Refactoring & Polish
- Modularized codebase into a structured package (`config`, `logic`, `models`, `utils`).
- Replaced manual config parsing with `pydantic-settings`.
- Improved Curl command parsing (better Windows support and URL detection).
- Integrated `pydantic` for strict data validation and structured report exporting.

### Testing
- Added comprehensive unit test suite with `pytest`.
- Added request mocking with `respx`.

### Community
- Added MIT License and Contributing guidelines.
- Added GitHub Actions for automated CI (Testing & Linting).
- Revamped README for better visibility and clarity.

## v1.1.0 (2025-12-28)

### Bug Fixes

- Updated export path configuration
  ([`f497a0c`](https://github.com/tuanpep/API-AutotestMCP/commit/f497a0cd158aeeaea1d23153814781ce203f7892))

### Documentation

- Add authentication workflows and endpoint configuration examples
  ([`c3def33`](https://github.com/tuanpep/API-AutotestMCP/commit/c3def33ecba795e394ba728a9d9a6f7a09ded2a8))

### Features

- Add AI instructions for using API Auto-Test MCP tools
  ([`ccee948`](https://github.com/tuanpep/API-AutotestMCP/commit/ccee94875c9d44f9dfbd4bcd6de276527a0ac17e))

- Enable environment variable configuration for export and profile directories and return absolute
  report path in exports
  ([`7e25392`](https://github.com/tuanpep/API-AutotestMCP/commit/7e253920ea6d3c410340218238efc0b888834f5f))


## v1.0.1 (2025-12-28)

### Bug Fixes

- Install script path handling
  ([`8088560`](https://github.com/tuanpep/API-AutotestMCP/commit/808856043d24814c5ce2c1f0246430feedef51bc))


## v1.0.0 (2025-12-28)

- Initial Release
