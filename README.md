# API Auto-Test MCP Server

An MCP server that allows AI agents to perform automated backend testing, simulate real client behavior (iOS, Android, Web), and export session logs for audit.

## Quick Install (One-Line)

Run this command in your terminal:
```bash
curl -fsSL https://raw.githubusercontent.com/tuanpep/api-test-mcp/main/install.sh | bash
```

## Manual Installation

### Using uv (Recommended)
```bash
uv tool install git+https://github.com/tuanpep/api-test-mcp
```

### Using pip
```bash
pip install git+https://github.com/tuanpep/api-test-mcp
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

## Configuration

You can configure the server using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `API_TEST_EXPORTS_DIR` | Directory where test reports are saved | `./exports` |
| `API_TEST_PROFILES_DIR` | Directory for client profiles | `./profiles` |

| `API_TEST_PROFILES_DIR` | Directory for client profiles | `./profiles` |

### Auto-Set to IDE Workspace
To automatically save reports to your current open project folder, configure the `env` in your MCP settings file (e.g., `claude_desktop_config.json` or Cursor settings):

```json
{
  "mcpServers": {
    "api-tester": {
      "command": "uv",
      "args": ["tool", "run", "api-test-mcp"],
      "env": {
        "API_TEST_EXPORTS_DIR": "${workspaceFolder}/test-reports"
      }
    }
  }
}
```
*Note: `${workspaceFolder}` is supported by most editors likes VS Code and Cursor.*

## Workflows & Examples

### 1. Configuring the Endpoint
There is no hardcoded "base URL" in the server. You (or the AI) provide the full URL for every request.
*   **Via Tool:** Pass `url="http://localhost:8088/api/v1/..."` argument.
*   **Via Curl:** Include the URL in the curl string: `curl http://api.com/endpoint`.

### 2. Handling Authentication
You can test secure APIs in two ways:

#### Method A: Using `simulate_client_request` (Easier)
If you have a Bearer token, simply pass it to the `auth_token` parameter. The tool will automatically add the `Authorization: Bearer <token>` header.

#### Method B: Using `run_curl` (More Flexible)
Include your custom headers directly in the command. This is perfect for complex auth like API Keys, Custom Schemes, or Cookies.
```bash
curl -H "X-API-KEY: 12345" -H "Authorization: CustomScheme xyz" https://api.com/secure
```

#### Method C: The "Agentic" Chain (Login + Action)
You can instruct the AI to perform a multi-step workflow. The AI will handle the "variable passing" for you.

**Prompt to AI:**
> "First, login to `POST /auth/login` with these credentials...
> Then, take the `access_token` from the response and use it to test `GET /user/profile`."

**What happens:**
1. AI calls `simulate_client_request(url="/login"...)`.
2. Tool returns JSON response with token.
3. AI reads token, then calls `simulate_client_request(url="/profile", auth_token="eyJ...")`.

## Development

### Directory Structure
- `src/api_test_mcp/server.py`: Main server logic.
- `exports/`: Generated reports.
- `profiles/`: Client profiles.
