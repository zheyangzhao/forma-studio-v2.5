#!/usr/bin/env bash
# Forma Studio v2.5 macOS build script
# 對應 PLAN-sprint-2.md §七

set -euo pipefail

cd "$(dirname "$0")"

if [[ ! -d "../.venv" ]]; then
  echo "❌ 找不到 ../.venv；請先：python3 -m venv ../.venv && ../.venv/bin/pip install -r requirements.txt"
  exit 1
fi

VENV_PY="../.venv/bin/python"

# 確保 pyinstaller 已裝
if ! "$VENV_PY" -c "import PyInstaller" 2>/dev/null; then
  echo "📦 安裝 PyInstaller..."
  "$VENV_PY" -m pip install pyinstaller
fi

echo "🛠  Building Forma Studio.app..."
rm -rf build dist
"$VENV_PY" -m PyInstaller forma-studio.spec --clean --noconfirm

APP_PATH="dist/Forma Studio.app"
if [[ -d "$APP_PATH" ]]; then
  size=$(du -sh "$APP_PATH" | cut -f1)
  echo "✅ Build 完成：$APP_PATH ($size)"
  echo ""
  echo "下一步（可選）："
  echo "  1. 簽名：codesign --force --deep --sign \"Developer ID Application: <YOUR NAME>\" \"$APP_PATH\""
  echo "  2. notarize：xcrun notarytool submit ... (需 Apple Developer ID)"
  echo "  3. 測試：open \"$APP_PATH\""
else
  echo "❌ Build 失敗：找不到 $APP_PATH"
  exit 1
fi
