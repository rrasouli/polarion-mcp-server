#!/bin/bash
# Quick setup script for Polarion MCP Server

echo "============================================"
echo "Polarion MCP Server Setup"
echo "============================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "Please edit .env file and add your Polarion token:"
    echo "  POLARION_TOKEN=your-token-here"
    echo ""
fi

# Test connection
echo ""
echo "Testing connection to Polarion..."
export $(cat .env | grep -v '^#' | xargs)

python3 << EOF
from polarion_client import PolarionClient
import os

client = PolarionClient(
    url=os.getenv("POLARION_URL"),
    token=os.getenv("POLARION_TOKEN"),
    verify_ssl=False
)

result = client.test_connection(os.getenv("POLARION_PROJECT", "OSE"))
print(result)
EOF

echo ""
echo "============================================"
echo "Setup complete!"
echo ""
echo "To use the MCP server with Claude Desktop:"
echo "  1. Edit ~/.claude/claude_desktop_config.json"
echo "  2. Add the polarion server configuration"
echo "  3. Restart Claude Desktop"
echo ""
echo "To use standalone:"
echo "  python3 server.py"
echo "============================================"
