"""Sprint 3C PDF export 測試（PLAN-sprint-3 §4.6）。"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.utils.design_memory import DesignMemory
from app.utils.exporters import PDFExporter, export_pdf
from app.utils.exporters.pdf_exporter import _default_font_path
from app.widgets.image_edit_panel import ImageEditPanel


def _no_client() -> None:
    raise RuntimeError("client_factory not expected to be called")


@pytest.fixture(scope="module")
def font_available() -> bool:
    return _default_font_path().exists()


def test_pdf_export_requires_prompt(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="prompt is required"):
        export_pdf(None, "   ", None, tmp_path / "out.pdf")


def test_pdf_export_requires_pdf_suffix(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match=".pdf"):
        export_pdf(None, "hello", None, tmp_path / "out.txt")


def test_pdf_export_missing_font_friendly_error(tmp_path: Path) -> None:
    """字型缺失時友善 error（PLAN §4.4 fallback）。"""
    exporter = PDFExporter(font_path=tmp_path / "missing.otf")
    with pytest.raises(FileNotFoundError, match="NotoSansTC"):
        exporter.export(
            memory=DesignMemory(brand_name="ACME"),
            prompt="hello",
            image_bytes=None,
            out_path=tmp_path / "out.pdf",
        )


def test_pdf_export_writes_file(tmp_path: Path, font_available: bool) -> None:
    """有字型時實際產 PDF，assert file size > 1KB。"""
    if not font_available:
        pytest.skip("NotoSansTC font not available")
    out = export_pdf(
        DesignMemory(project_name="ACME 提案", brand_name="ACME"),
        "請繪製一份併購提案封面",
        None,
        tmp_path / "out.pdf",
        quality="high",
    )
    assert out.exists()
    assert out.stat().st_size > 1024
    # PDF magic header
    assert out.read_bytes().startswith(b"%PDF-")


def test_pdf_export_includes_v3_memory(font_available: bool) -> None:
    """memory_lines() 含 v3 4 欄位摘要。"""
    if not font_available:
        pytest.skip("NotoSansTC font not available")
    memory = DesignMemory(
        brand_name="ACME",
        spacing_tokens={"base": "4px"},
        components=["Button: rounded"],
        motion={"duration_fast": "120ms"},
        voice_signals=["直接、克制"],
    )
    exporter = PDFExporter()
    lines = exporter._memory_lines(memory)
    joined = "\n".join(lines)
    assert "Spacing/Layout: base=4px" in joined
    assert "Components: Button: rounded" in joined
    assert "Motion: duration_fast=120ms" in joined
    assert "Voice/Copy: 直接、克制" in joined


def test_pdf_export_metadata_table_optional_rows() -> None:
    """metadata table：quality / brand / industry 有值才 emit row。"""
    exporter = PDFExporter()
    from app.utils.exporters.pdf_exporter import PDFExportMetadata

    meta = PDFExportMetadata(quality="high")
    table = exporter._metadata_table(
        DesignMemory(brand_name="ACME", industry="legal"),
        meta,
    )
    # _cellvalues 是 reportlab Table 內部 attr（暴露 row data）
    rows = table._cellvalues
    keys = [r[0] for r in rows]
    assert "Quality" in keys
    assert "Brand" in keys
    assert "Industry" in keys


def test_image_edit_panel_export_pdf_button_state(qtbot) -> None:
    """生成前 disabled，生成完後 enabled，busy 期間 disabled。"""
    panel = ImageEditPanel(client_factory=_no_client)
    qtbot.addWidget(panel)
    assert panel.export_pdf_btn.isEnabled() is False
    from app.api.openai_client import ImageResult
    panel._on_worker_finished(ImageResult(data=b"fake"))
    assert panel.export_pdf_btn.isEnabled() is True
    panel._set_busy(True)
    assert panel.export_pdf_btn.isEnabled() is False
