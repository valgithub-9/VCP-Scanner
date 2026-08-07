#!/bin/bash

# VCP Scanner with AI Finance Agent - Setup Script
# This script automates the installation process

set -e

echo "======================================"
echo "🚀 VCP Scanner AI Finance Agent Setup"
echo "======================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python version: $python_version"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "✓ Creating virtual environment..."
    python3 -m venv venv
else
    echo ""
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "✓ Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null

# Install requirements
echo "✓ Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
echo ""
if [ ! -f ".env" ]; then
    echo "✓ Creating .env file from template..."
    cp .env.example .env
    echo "  Please edit .env and add your ANTHROPIC_API_KEY"
else
    echo "✓ .env file already exists"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "✓ Creating .gitignore..."
    cat > .gitignore << EOF
.env
__pycache__/
*.pyc
*.pyo
*.egg-info/
venv/
.vscode/
.DS_Store
vcp_scan_*.csv
*.log
EOF
fi

# Verify installation
echo ""
echo "✓ Verifying installation..."

# Test imports
python -c "import yfinance; import pandas; import numpy" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "  ✅ Core dependencies verified"
fi

python -c "import anthropic" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "  ✅ Anthropic SDK verified"
fi

# Final summary
echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your ANTHROPIC_API_KEY:"
echo "   nano .env"
echo ""
echo "2. Get your API key from:"
echo "   https://console.anthropic.com/account/keys"
echo ""
echo "3. Run the VCP Scanner:"
echo "   source venv/bin/activate"
echo "   python vcp_scanner.py"
echo ""
echo "4. Run the AI Finance Agent:"
echo "   python ai_finance_agent.py"
echo ""
echo "For more help, see INSTALL.md"
echo ""
