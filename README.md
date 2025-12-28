# API Auto-Test MCP Server

[![CI](https://github.com/tuanpep/API-AutotestMCP/actions/workflows/ci.yml/badge.svg)](https://github.com/tuanpep/API-AutotestMCP/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An MCP server that allows AI agents to perform automated backend testing, simulate real client behavior (iOS, Android, Web), and export session logs for audit.

## 🚀 Key Features

- **Client Simulation**: Test your APIs as an iPhone, Android, or Desktop browser.
- **Curl Parsing**: Copy/paste `curl` commands from Chrome DevTools directly into the tool.
- **Performance Monitoring**: Automatically flags requests slower than 500ms.
- **Auto-Logging**: Every request is saved as a JSON artifact for debugging.
- **Session Reports**: Export full test sessions to Markdown or JSON.

## 📦 Installation

### Quick Install (One-Line)

```bash
curl -fsSL https://raw.githubusercontent.com/tuanpep/API-AutotestMCP/main/install.sh | bash
```

### Manual Installation (Using uv)

```bash
uv tool install git+https://github.com/tuanpep/API-AutotestMCP.git
```

## 🛠 Usage in Claude Desktop / Cursor

Add the following to your MCP configuration file (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "api-tester": {
      "command": "uv",
      "args": [
        "tool",
        "run",
        "api-test-mcp"
      ],
      "env": {
        "API_TEST_EXPORTS_DIR": "${workspaceFolder}/test-reports"
      }
    }
  }
}
```

## 🧰 Tools Available

| Tool | Description |
|------|-------------|
| `simulate_client_request` | Execute requests simulating specific devices (iPhone, Android, Desktop). |
| `run_curl` | Parses and executes a raw curl command. |
| `export_test_report` | Packages all recent requests into a single Markdown or JSON report. |

## ⚙️ Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `API_TEST_EXPORTS_DIR` | Directory where test reports and logs are saved. Supports `${workspaceFolder}`. | `exports` |
| `API_TEST_LOG_LEVEL` | Logging level. | `INFO` |

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
