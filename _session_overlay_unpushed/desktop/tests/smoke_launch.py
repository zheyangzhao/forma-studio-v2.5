"""Sprint 2 headless smoke：launch MainWindow + 驗 4 tab + 存截圖。

跑法：
    QT_QPA_PLATFORM=offscreen python desktop/tests/smoke_launch.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# 讓 import 走 desktop/app
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "desktop"))

# headless 模式
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from app.main_window import MainWindow

EXPECTED_TABS = ["Prompt Gallery", "圖像生成 / 修改", "品牌記憶", "設定"]


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow(project_root=ROOT)
    window.resize(1180, 820)
    window.show()

    # 驗 4 個 tab title
    actual = [window.tabs.tabText(i) for i in range(window.tabs.count())]
    print(f"tabs found ({len(actual)}): {actual}")
    if actual != EXPECTED_TABS:
        print(f"FAIL: expected {EXPECTED_TABS}", file=sys.stderr)
        return 1

    # 驗 ImageEditPanel / BrandSettingsTab / quality dial 都建好
    assert window.image_edit_panel is not None, "image_edit_panel not built"
    assert window.brand_settings_tab is not None, "brand_settings_tab not built"
    assert window.image_edit_panel.quality_dial.quality() == "medium"
    print("widgets OK: ImageEditPanel + BrandSettingsTab built, quality default=medium")

    # 切到每個 tab、各存一張截圖
    artifacts_dir = ROOT / "desktop" / "tests" / "smoke-artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    for i, name in enumerate(actual):
        window.tabs.setCurrentIndex(i)
        app.processEvents()
        pix = window.grab()
        out_path = artifacts_dir / f"smoke-tab-{i+1:02d}-{name.replace(' ', '_').replace('/', '-')}.png"
        pix.save(str(out_path))
        size_kb = out_path.stat().st_size // 1024
        print(f"  tab {i+1} '{name}' -> {out_path.name} ({size_kb} KB)")

    # 驗 brand tab 已嘗試載入根目錄 DESIGN.md（應該不存在 → status 顯示提示）
    print(f"brand status: {window.brand_settings_tab.status_label.text()}")

    # 0.5 秒後 quit（headless 不需互動）
    QTimer.singleShot(500, app.quit)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
