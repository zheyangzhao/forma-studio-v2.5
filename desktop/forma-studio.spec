# PyInstaller spec — Forma Studio Desktop v2.5
# 對應 PLAN-sprint-2.md §七 / SDD §四
#
# build：
#   cd desktop && pyinstaller forma-studio.spec --clean --noconfirm

# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

ROOT = Path(SPECPATH).resolve()

a = Analysis(
    ["main.py"],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        # 把 web/prompt-library 帶進去（gallery JSON 與桌面版同 source）
        (str(ROOT.parent / "web" / "prompt-library"), "prompt-library"),
    ],
    hiddenimports=[
        "app",
        "app.api",
        "app.api.key_store",
        "app.api.openai_client",
        "app.pages",
        "app.pages.brand_settings_tab",
        "app.utils",
        "app.utils.design_memory",
        "app.widgets",
        "app.widgets.image_edit_panel",
        "app.widgets.mask_uploader",
        "app.widgets.quality_dial",
        "app.widgets.reference_drop_zone",
        "keyring.backends.macOS",
        "keyring.backends.Windows",
        "keyring.backends.SecretService",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的 PyQt6 模組以縮小 .app
        "PyQt6.Qt3DAnimation",
        "PyQt6.Qt3DCore",
        "PyQt6.Qt3DExtras",
        "PyQt6.Qt3DInput",
        "PyQt6.Qt3DLogic",
        "PyQt6.Qt3DRender",
        "PyQt6.QtBluetooth",
        "PyQt6.QtMultimedia",
        "PyQt6.QtPositioning",
        "PyQt6.QtQml",
        "PyQt6.QtQuick",
        "PyQt6.QtQuick3D",
        "PyQt6.QtWebChannel",
        "PyQt6.QtWebEngineCore",
        "PyQt6.QtWebEngineWidgets",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="FormaStudio",  # macOS 內部 binary 名稱
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,  # Sprint 2D 後續可加 Apple Developer ID
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="forma-studio",
)

# 產 macOS .app bundle
app = BUNDLE(
    coll,
    name="Forma Studio.app",
    icon=None,  # icon 先不附（Sprint 2D 後續加 .icns）
    bundle_identifier="ai.formastudio.desktop",
    info_plist={
        "CFBundleName": "Forma Studio",
        "CFBundleDisplayName": "Forma Studio",
        "CFBundleVersion": "2.5.0",
        "CFBundleShortVersionString": "2.5",
        "NSHighResolutionCapable": True,
        "LSApplicationCategoryType": "public.app-category.graphics-design",
        "LSMinimumSystemVersion": "12.0",
        # 注意：Keychain 寫入由 macOS 自己處理，第一次寫入會跳系統對話框，
        # 不需 NSAppleEventsUsageDescription（那是 Apple Events 自動化權限）。
    },
)
