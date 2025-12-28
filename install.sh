#!/bin/bash
set -e

echo "🚀 Installing API Auto-Test MCP..."

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check if uv is installed
if ! command_exists uv; then
    echo "📦 'uv' not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add to path for this session
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install the tool
echo "📦 Installing api-test-mcp via uv tool..."
# Ensure we are using the uv we just might have installed or the system one
UV_BIN=$(command -v uv || echo "$HOME/.local/bin/uv")

"$UV_BIN" tool install --force git+https://github.com/tuanpep/API-AutotestMCP.git

echo "✅ Installation complete!"
echo "   Run 'api-test-mcp --help' to verify."
echo "   To use with Claude/Cursor, check the README for config details."
