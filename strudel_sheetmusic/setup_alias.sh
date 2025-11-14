#!/bin/bash
# Add StrudelSheet aliases to ~/.zshrc

echo ""
echo "Adding StrudelSheet aliases to ~/.zshrc..."

# Check if aliases already exist
if grep -q "alias strudel_sheet=" ~/.zshrc 2>/dev/null; then
    echo "✓ Aliases already exist in ~/.zshrc"
else
    # Add aliases
    cat >> ~/.zshrc << 'ZSHRC'

# StrudelSheet - Music Analysis Tool
alias strudel_sheet='cd ~/Documents/Applications/repos/strudel_sheet && source venv/bin/activate && python3 strudel_sheet'
alias ss='cd ~/Documents/Applications/repos/strudel_sheet && source venv/bin/activate && python3 strudel_sheet'
ZSHRC
    
    echo "✓ Added aliases to ~/.zshrc"
fi

echo ""
echo "To activate now, run:"
echo "  source ~/.zshrc"
echo ""
echo "Then you can use:"
echo "  strudel_sheet  (or just: ss)"
echo ""
