"""GUI multi-step walkthrough（pytest-qt + offscreen 截圖）。

用 qtbot 模擬使用者實際操作：
1. 開啟 MainWindow
2. 切換 4 個 tab + 截圖
3. BrandSettingsTab 填欄位 + 存 DESIGN.md
4. 載回確認
5. ImageEditPanel 填 prompt + 設 quality + monkeypatch 模擬生成完成
6. 點匯出 Markdown / PDF（用 monkeypatch QFileDialog 避免互動）
7. 確認檔案產出 + 截圖

對應 Codex audit 立即動作項 §8.1 的自動化版本。
"""

from __future__ import annotations

import base64
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from app.api.openai_client import ImageResult
from app.main_window import MainWindow


# 1x1 透明 PNG（給 reportlab Image flowable 用，避免 PIL UnidentifiedImageError）
TINY_PNG = base64.b64decode(
    b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
)


ARTIFACT_DIR = Path(__file__).parent / "walkthrough-artifacts"


@pytest.fixture(autouse=True)
def _ensure_artifact_dir() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def _grab(window: MainWindow, name: str) -> Path:
    out = ARTIFACT_DIR / f"{name}.png"
    pix = window.grab()
    pix.save(str(out))
    return out


def test_walkthrough_full_session(qtbot, tmp_path: Path, monkeypatch) -> None:
    """完整 walkthrough：開窗 → 切 4 tab → 填 brand → 存 → 模擬生成 → export MD/PDF。"""
    window = MainWindow(project_root=tmp_path)
    qtbot.addWidget(window)
    window.show()
    qtbot.wait(50)

    # ── Step 1：4 tab 截圖 ──────────────────────────
    for i in range(window.tabs.count()):
        window.tabs.setCurrentIndex(i)
        qtbot.wait(30)
        # sanitize tab title 去掉 filesystem 不允許的字元
        safe = (
            window.tabs.tabText(i)
            .replace("/", "-")
            .replace(" ", "_")
        )
        out = _grab(window, f"step-1-tab-{i+1:02d}-{safe}")
        assert out.exists() and out.stat().st_size > 1000

    # ── Step 2：填 BrandSettingsTab 並儲存 DESIGN.md ──
    window.tabs.setCurrentIndex(2)  # 品牌記憶
    bst = window.brand_settings_tab
    assert bst is not None
    bst.brand_name_edit.setText("ACME Legal")
    bst.industry_edit.setText("legal")
    bst.audience_edit.setText("律師, 企業客戶")
    bst.tone_edit.setText("嚴肅高端")
    bst._add_color_row("primary", "oklch(55% 0.18 250)")
    bst._add_spacing_row("base", "4px")
    bst.components_edit.setPlainText("Button: 8px radius")
    bst.motion_edit.setPlainText("duration_fast: 120ms")
    bst.voice_edit.setPlainText("直接、克制")
    qtbot.wait(50)
    _grab(window, "step-2-brand-filled")

    # 點儲存
    bst.save_to_project()
    qtbot.wait(50)
    saved = tmp_path / "DESIGN.md"
    assert saved.exists()
    text = saved.read_text(encoding="utf-8")
    assert "ACME Legal" in text
    assert "## Spacing & Layout" in text
    assert "## Components" in text
    _grab(window, "step-2-brand-saved")

    # ── Step 3：載回 DESIGN.md 應顯示剛存的內容 ──
    bst.set_memory(__import__("app.utils.design_memory", fromlist=["DesignMemory"]).DesignMemory())  # 清空
    bst.load_from_project(tmp_path)
    qtbot.wait(30)
    assert bst.brand_name_edit.text() == "ACME Legal"
    assert "Button: 8px radius" in bst.components_edit.toPlainText()
    _grab(window, "step-3-brand-reloaded")

    # ── Step 4：image tab 填 prompt + 模擬生成完成 ──
    window.tabs.setCurrentIndex(1)  # 圖像生成
    iep = window.image_edit_panel
    assert iep is not None
    iep.set_prompt("為 ACME Legal 製作併購提案封面，黑底金字")
    iep.quality_dial.set_quality("high")
    qtbot.wait(30)
    _grab(window, "step-4-image-prompt")

    # 模擬 OpenAI 回傳成功（不真打 API）
    # 用真 1x1 PNG 讓 reportlab 不會 PIL UnidentifiedImageError
    iep._on_worker_finished(ImageResult(data=TINY_PNG))
    qtbot.wait(30)
    assert iep.export_md_btn.isEnabled()
    assert iep.export_pdf_btn.isEnabled()
    _grab(window, "step-4-image-generated")

    # ── Step 5：monkeypatch QFileDialog 後點 export Markdown ──
    md_out = tmp_path / "walkthrough-export.md"
    monkeypatch.setattr(
        "app.widgets.image_edit_panel.QFileDialog.getSaveFileName",
        lambda *a, **k: (str(md_out), ""),
    )
    iep._on_export_markdown_clicked()
    qtbot.wait(50)
    assert md_out.exists()
    assert "ACME Legal" in md_out.read_text(encoding="utf-8")
    assert (tmp_path / "walkthrough-export.png").exists()  # sidecar
    _grab(window, "step-5-md-exported")

    # ── Step 6：點 export PDF（同樣 monkeypatch） ──
    pdf_out = tmp_path / "walkthrough-export.pdf"
    monkeypatch.setattr(
        "app.widgets.image_edit_panel.QFileDialog.getSaveFileName",
        lambda *a, **k: (str(pdf_out), ""),
    )
    iep._on_export_pdf_clicked()
    qtbot.wait(100)
    assert pdf_out.exists()
    assert pdf_out.read_bytes().startswith(b"%PDF-")
    assert pdf_out.stat().st_size > 1024
    _grab(window, "step-6-pdf-exported")

    # ── Step 7：close window 應不出現 QThread destroyed warning ──
    window.close()
    qtbot.wait(50)
    _grab(window, "step-7-closed")
