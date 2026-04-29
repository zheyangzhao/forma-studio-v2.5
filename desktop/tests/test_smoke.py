"""UI smoke tests：MainWindow / BrandSettingsTab 開頁不 crash。

對應 PLAN-sprint-2.md §2.7（main_window_smoke）+ §4.5（brand_settings_tab_smoke）。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.main_window import MainWindow
from app.pages.brand_settings_tab import BrandSettingsTab


def test_main_window_smoke(qtbot, tmp_path: Path) -> None:
    window = MainWindow(project_root=tmp_path)
    qtbot.addWidget(window)
    assert window.tabs.count() == 4
    titles = [window.tabs.tabText(i) for i in range(window.tabs.count())]
    assert titles == ["Prompt Gallery", "圖像生成 / 修改", "品牌記憶", "設定"]
    assert window.image_edit_panel is not None
    assert window.brand_settings_tab is not None


def test_brand_settings_tab_smoke(qtbot, tmp_path: Path) -> None:
    tab = BrandSettingsTab(project_root=tmp_path)
    qtbot.addWidget(tab)
    # 沒 DESIGN.md 時 status 顯示提示
    tab.load_from_project(tmp_path)
    assert "DESIGN.md" in tab.status_label.text()
    # 填入後 save 應不 crash
    tab.brand_name_edit.setText("ACME")
    tab.save_to_project()
    saved = tmp_path / "DESIGN.md"
    assert saved.exists()
    # 重新 load 應拿到 brand_name
    tab.load_from_project(tmp_path)
    assert tab.brand_name_edit.text() == "ACME"
