# Contributing to API Auto-Test MCP

Thank you for your interest in improving this tool!

## How to Contribute

1. **Bug Reports & Feature Requests**: Please open an Issue on GitHub with a clear description and steps to reproduce.
2. **Pull Requests**:
    - Fork the repository.
    - Create a new branch (`feat/your-feature` or `fix/your-fix`).
    - Ensure your code follows the existing style.
    - Add tests for new logic.
    - Submit a PR with a detailed description of changes.

## Development Setup

We use `uv` for dependency management.

```bash
# Install dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Linting
uv run ruff check .
```

## Project Structure

- `src/api_test_mcp/server.py`: MCP Server entry point and tool definitions.
- `src/api_test_mcp/logic.py`: Core request execution logic.
- `src/api_test_mcp/utils.py`: Helpers like the curl parser.
- `src/api_test_mcp/config.py`: Configuration handling.
- `src/api_test_mcp/models.py`: Pydantic models for structured data.

## Code of Conduct

Please be respectful and professional in all interactions.
