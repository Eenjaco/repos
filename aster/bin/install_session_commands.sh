#!/usr/bin/env bash
# Install session management commands system-wide

set -e

echo "📦 Installing session management commands..."
echo ""

# Make scripts executable
chmod +x "$(dirname "$0")/session_end.sh"
chmod +x "$(dirname "$0")/session_start.sh"

# Create symlinks in user bin
mkdir -p ~/bin

ln -sf "$(pwd)/$(dirname "$0")/session_end.sh" ~/bin/session_end
ln -sf "$(pwd)/$(dirname "$0")/session_start.sh" ~/bin/session_start

echo "✅ Scripts installed to ~/bin/"
echo ""

# Check if ~/bin is in PATH
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo "⚠️  ~/bin is not in your PATH"
    echo ""
    echo "Add this to your ~/.zshrc or ~/.bashrc:"
    echo ""
    echo '  export PATH="$HOME/bin:$PATH"'
    echo ""
    echo "Then run: source ~/.zshrc"
    echo ""
else
    echo "✅ ~/bin is already in PATH"
    echo ""
fi

# Check if ollama is available
if command -v ollama &> /dev/null; then
    echo "✅ Ollama found"

    # Check if llama3.2:1b is available
    if ollama list 2>/dev/null | grep -q "llama3.2:1b"; then
        echo "✅ llama3.2:1b model found"
    else
        echo "⚠️  llama3.2:1b model not found"
        echo ""
        echo "Pull it with: ollama pull llama3.2:1b"
        echo ""
    fi
else
    echo "❌ Ollama not found"
    echo ""
    echo "Install from: https://ollama.ai"
    echo ""
fi

echo "🎉 Installation complete!"
echo ""
echo "Usage (in any git repo):"
echo "  session_end    - Commit changes with AI-generated message"
echo "  session_start  - Get briefing and suggestions"
echo ""
