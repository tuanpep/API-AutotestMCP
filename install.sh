#!/bin/bash
set -e

echo "🚀 Installing API Auto-Test MCP..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 'uv' not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Install the tool
echo "📦 Installing api-test-mcp via uv tool..."
uv tool install --force .

echo "✅ Installation complete!"
echo "   Run 'api-test-mcp --help' to verify."
echo "   To use with Claude/Cursor, check the README for config details."
