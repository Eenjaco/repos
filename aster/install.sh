#!/usr/bin/env bash
# Aster - Automated Installation Script
# Installs all dependencies on a fresh Mac or Linux system

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ASCII Art Header
echo -e "${BLUE}"
cat << "EOF"
    ╔═══════════════════════════════════════════════════════════╗
    ║                    ✨ ASTER INSTALLER                    ║
    ║         Navigate your constellation of knowledge         ║
    ╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
    echo -e "${GREEN}✓${NC} Detected: macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo -e "${GREEN}✓${NC} Detected: Linux"
else
    echo -e "${RED}✗${NC} Unsupported OS: $OSTYPE"
    exit 1
fi

echo ""
echo -e "${BLUE}[1/7]${NC} Installing System Dependencies..."
echo "─────────────────────────────────────────────────────────────"

if [ "$OS" = "mac" ]; then
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo -e "${YELLOW}→${NC} Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo -e "${GREEN}✓${NC} Homebrew already installed"
    fi

    # Install dependencies
    echo -e "${YELLOW}→${NC} Installing packages via Homebrew..."
    brew install python@3.12 tesseract tesseract-lang poppler pandoc ffmpeg ollama

    # Start Ollama service
    echo -e "${YELLOW}→${NC} Starting Ollama service..."
    brew services start ollama
    sleep 2  # Give Ollama time to start

elif [ "$OS" = "linux" ]; then
    echo -e "${YELLOW}→${NC} Installing packages via apt..."
    sudo apt update
    sudo apt install -y python3.12 python3.12-venv tesseract-ocr tesseract-ocr-all \
        poppler-utils pandoc ffmpeg curl

    # Install Ollama
    if ! command -v ollama &> /dev/null; then
        echo -e "${YELLOW}→${NC} Installing Ollama..."
        curl -fsSL https://ollama.com/install.sh | sh
    else
        echo -e "${GREEN}✓${NC} Ollama already installed"
    fi
fi

echo -e "${GREEN}✓${NC} System dependencies installed"
echo ""

echo -e "${BLUE}[2/7]${NC} Setting Up Python Environment..."
echo "─────────────────────────────────────────────────────────────"

# Remove old venv if exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}→${NC} Removing old virtual environment..."
    rm -rf venv
fi

# Create virtual environment with Python 3.12
echo -e "${YELLOW}→${NC} Creating virtual environment with Python 3.12..."
if [ "$OS" = "mac" ]; then
    /usr/local/opt/python@3.12/bin/python3.12 -m venv venv
else
    python3.12 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}→${NC} Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}→${NC} Upgrading pip..."
pip install --upgrade pip --quiet

echo -e "${GREEN}✓${NC} Python environment ready"
echo ""

echo -e "${BLUE}[3/7]${NC} Installing Python Packages..."
echo "─────────────────────────────────────────────────────────────"
echo -e "${YELLOW}→${NC} This may take 5-10 minutes (downloading ~500MB)..."

# Install from requirements.txt
pip install -r requirements.txt --quiet

# Install QR code library
pip install 'qrcode[pil]' --quiet

echo -e "${GREEN}✓${NC} Python packages installed"
echo ""

echo -e "${BLUE}[4/7]${NC} Downloading NLTK Data..."
echo "─────────────────────────────────────────────────────────────"

python3 -c "
import nltk
import sys
try:
    nltk.download('punkt_tab', quiet=True)
    nltk.download('averaged_perceptron_tagger_eng', quiet=True)
    print('✓ NLTK data downloaded')
except Exception as e:
    print(f'⚠ NLTK download warning: {e}', file=sys.stderr)
"

echo ""

echo -e "${BLUE}[5/7]${NC} Downloading Ollama Models..."
echo "─────────────────────────────────────────────────────────────"
echo -e "${YELLOW}→${NC} Downloading llama3.2:1b (1.3GB) - this may take a few minutes..."

# Pull the recommended model
ollama pull llama3.2:1b

echo -e "${GREEN}✓${NC} Ollama model downloaded"
echo ""

echo -e "${BLUE}[6/7]${NC} Creating Directory Structure..."
echo "─────────────────────────────────────────────────────────────"

# Create necessary directories
mkdir -p tests/training_data/{books,newsletters,religious,financial,technical,personal,audio,images}
mkdir -p tests/outputs
mkdir -p tests/training_outputs
mkdir -p uploads
mkdir -p outputs

echo -e "${GREEN}✓${NC} Directory structure created"
echo ""

echo -e "${BLUE}[7/7]${NC} Making Scripts Executable..."
echo "─────────────────────────────────────────────────────────────"

chmod +x aster.py aster_web

echo -e "${GREEN}✓${NC} Scripts are executable"
echo ""

# Test installation
echo -e "${BLUE}[TEST]${NC} Verifying Installation..."
echo "─────────────────────────────────────────────────────────────"

echo -e "${YELLOW}→${NC} Testing Python packages..."
python3 -c "
import pandas
import unstructured
import ollama
import fastapi
print('✓ All packages load successfully')
" || echo -e "${RED}✗${NC} Package test failed"

echo -e "${YELLOW}→${NC} Testing Tesseract..."
if command -v tesseract &> /dev/null; then
    LANG_COUNT=$(tesseract --list-langs 2>&1 | grep -c "^[a-z]")
    echo -e "${GREEN}✓${NC} Tesseract installed with $LANG_COUNT languages"
else
    echo -e "${RED}✗${NC} Tesseract not found"
fi

echo -e "${YELLOW}→${NC} Testing Ollama..."
if ollama list | grep -q "llama3.2:1b"; then
    echo -e "${GREEN}✓${NC} Ollama model ready"
else
    echo -e "${YELLOW}⚠${NC} Ollama model may still be downloading"
fi

echo ""
echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                    🎉 INSTALLATION COMPLETE!              ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo -e "  ${GREEN}1.${NC} Test CLI processing:"
echo -e "     ${YELLOW}./aster.py tests/Year\\ A\\ 2022-2023.xlsx -o /tmp/test.md${NC}"
echo ""
echo -e "  ${GREEN}2.${NC} Start web server for iPhone access:"
echo -e "     ${YELLOW}./aster_web${NC}"
echo ""
echo -e "  ${GREEN}3.${NC} Scan the QR code with your iPhone camera"
echo ""
echo -e "  ${GREEN}4.${NC} Import training data to ${YELLOW}tests/training_data/${NC}"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo -e "  • INSTALL.md - Complete installation guide"
echo -e "  • README.md - Project overview"
echo -e "  • docs/IPHONE_INTEGRATION.md - iPhone setup details"
echo ""
echo -e "${GREEN}Enjoy navigating your constellation of knowledge! ✨${NC}"
echo ""

# Add to shell RC file for auto-activation (optional)
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
    echo -e "${YELLOW}→${NC} Optional: Add auto-activation to $SHELL_RC? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        cat >> "$SHELL_RC" << 'EOL'

# Auto-activate Python venv when entering aster directory
cd() {
  builtin cd "$@"
  if [[ -f "venv/bin/activate" ]]; then
    source venv/bin/activate
  fi
}
EOL
        echo -e "${GREEN}✓${NC} Added auto-activation to $SHELL_RC"
        echo -e "   Run: ${YELLOW}source $SHELL_RC${NC} to apply now"
    fi
fi
