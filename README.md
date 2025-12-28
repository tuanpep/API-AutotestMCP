# API Auto-Test MCP Server

An MCP server that allows AI agents to perform automated backend testing, simulate real client behavior (iOS, Android, Web), and export session logs for audit.

## Quick Install (One-Line)

Run this command in your terminal:
```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/api-test-mcp/main/install.sh | bash
```

## Manual Installation

### Using uv (Recommended)
```bash
uv tool install git+https://github.com/YOUR_GITHUB_USERNAME/api-test-mcp
```

### Using pip
```bash
pip install git+https://github.com/YOUR_GITHUB_USERNAME/api-test-mcp
```

### From Source (Development)
1. Clone the repository.
2. Run:
   ```bash
   chmod +x install.sh && ./install.sh
   ```

## Usage

### Running Locally
To run the server manually:
```bash
api-test-mcp
```

### Integration with Claude Desktop / Cursor
Add the following to your MCP configuration file:

```json
{
  "mcpServers": {
    "api-tester": {
      "command": "uv",
      "args": [
        "tool",
        "run",
        "api-test-mcp"
      ]
    }
  }
}
```

## Tools Available
- **`simulate_client_request`**: Execute requests simulating specific devices.
- **`run_curl`**: Execute raw curl commands (supports Windows CMD escaping).
- **`export_test_report`**: Export request logs to JSON or Markdown.

## Development

### Directory Structure
- `src/api_test_mcp/server.py`: Main server logic.
- `exports/`: Generated reports.
- `profiles/`: Client profiles.
