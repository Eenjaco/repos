#!/usr/bin/env bash
# Create a clean export ZIP of Aster for transferring to another computer

set -e

echo "📦 Creating Aster export package..."
echo ""

# Get the parent directory (one level up from aster)
PARENT_DIR=$(cd .. && pwd)
ASTER_DIR=$(basename "$PWD")

cd "$PARENT_DIR"

# Create timestamp
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
EXPORT_NAME="aster-export-${TIMESTAMP}.zip"

echo "→ Packaging files (excluding venv, cache, outputs)..."

# Create ZIP excluding unnecessary files
zip -r "$EXPORT_NAME" "$ASTER_DIR" \
  -x "${ASTER_DIR}/venv/*" \
  -x "${ASTER_DIR}/__pycache__/*" \
  -x "${ASTER_DIR}/**/__pycache__/*" \
  -x "${ASTER_DIR}/.git/*" \
  -x "${ASTER_DIR}/uploads/*" \
  -x "${ASTER_DIR}/outputs/*" \
  -x "${ASTER_DIR}/tests/outputs/*" \
  -x "${ASTER_DIR}/tests/training_outputs/*" \
  -x "${ASTER_DIR}/**/*.pyc" \
  -x "${ASTER_DIR}/.DS_Store" \
  -x "${ASTER_DIR}/**/.DS_Store" \
  -q

# Get file size
SIZE=$(ls -lh "$EXPORT_NAME" | awk '{print $5}')

echo ""
echo "✅ Export created successfully!"
echo ""
echo "   File: $EXPORT_NAME"
echo "   Size: $SIZE"
echo "   Location: $PARENT_DIR"
echo ""
echo "📋 Next steps:"
echo ""
echo "   1. Transfer $EXPORT_NAME to the new computer"
echo "   2. Extract: unzip $EXPORT_NAME"
echo "   3. Install: cd aster && ./install.sh"
echo ""
echo "📄 See EXPORT_GUIDE.md for complete instructions"
echo ""
