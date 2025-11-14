#!/bin/bash
# Setup Aster GitHub Remote
# Run this after creating the GitHub repo: https://github.com/Eenjaco/aster

echo "🚀 Setting up Aster GitHub remote..."

cd ~/Documents/Applications/aster_standalone || exit

echo "📍 Current directory: $(pwd)"
echo ""

echo "✅ Checking git status..."
git status
echo ""

echo "🔗 Adding GitHub remote..."
git remote add origin https://github.com/Eenjaco/aster.git
echo ""

echo "📤 Pushing to GitHub..."
git push -u origin main
echo ""

echo "✅ Verifying remote..."
git remote -v
echo ""

echo "🎉 Done! Aster is now on GitHub!"
echo "   Visit: https://github.com/Eenjaco/aster"
