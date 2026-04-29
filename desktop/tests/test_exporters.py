"""Sprint 3B Markdown export 測試（PLAN-sprint-3 §3.5）。"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.utils.design_memory import DesignMemory
from app.utils.exporters import MarkdownExporter, export_markdown
from app.utils.exporters.markdown_exporter import (
    SCHEMA_VERSION,
    ExportMetadata,
)
from app.widgets.image_edit_panel import ImageEditPanel


def _no_client() -> None:
    raise RuntimeError("client_factory not expected to be called")


def test_markdown_export_requires_prompt(tmp_path: Path) -> None:
    """空 prompt → ValueError。"""
    with pytest.raises(ValueError, match="prompt is required"):
        export_markdown(
            None, "   ", None, tmp_path / "x.md"
        )


def test_markdown_export_requires_md_extension(tmp_path: Path) -> None:
    """副檔名非 .md → ValueError。"""
    with pytest.raises(ValueError, match=".md"):
        export_markdown(
            None, "hello", None, tmp_path / "x.txt"
        )


def test_markdown_export_writes_frontmatter(tmp_path: Path) -> None:
    """frontmatter 含 schema_version / export_type / created_at。"""
    out = export_markdown(
        None, "draw a thing", None, tmp_path / "out.md", quality="high"
    )
    text = out.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert f"schema_version: {SCHEMA_VERSION}" in text
    assert 'export_type: "markdown"' in text
    assert "created_at:" in text
    assert 'quality: "high"' in text


def test_markdown_export_writes_image_sidecar(tmp_path: Path) -> None:
    """有 image bytes 時寫同名 .png sidecar 與 ![] reference。"""
    memory = DesignMemory(project_name="ACME", brand_name="ACME")
    out = export_markdown(
        memory,
        "create a legal proposal cover",
        b"fake-png-bytes",
        tmp_path / "proposal.md",
    )
    assert out.exists()
    sidecar = tmp_path / "proposal.png"
    assert sidecar.exists()
    assert sidecar.read_bytes() == b"fake-png-bytes"
    text = out.read_text(encoding="utf-8")
    assert 'image_file: "proposal.png"' in text
    assert "![Generated image](proposal.png)" in text


def test_markdown_export_includes_v3_memory(tmp_path: Path) -> None:
    """spacing/components/motion/voice 都應出現在 Design Memory section。"""
    memory = DesignMemory(
        brand_name="ACME",
        spacing_tokens={"base": "4px"},
        components=["Button: 8px radius"],
        motion={"duration_fast": "120ms"},
        voice_signals=["直接、克制"],
    )
    out = export_markdown(
        memory, "draw a logo", None, tmp_path / "v3.md"
    )
    text = out.read_text(encoding="utf-8")
    assert "## Design Memory" in text
    assert "Spacing/Layout: base=4px" in text
    assert "Components: Button: 8px radius" in text
    assert "Motion: duration_fast=120ms" in text
    assert "Voice/Copy: 直接、克制" in text


def test_markdown_export_includes_attribution(tmp_path: Path) -> None:
    """source_attribution 出現在末尾 Source Attribution section。"""
    out = export_markdown(
        None,
        "p",
        None,
        tmp_path / "x.md",
        source_attribution=["wuyoscar/gpt_image_2_skill, CC BY 4.0"],
    )
    text = out.read_text(encoding="utf-8")
    assert "## Source Attribution" in text
    assert "wuyoscar/gpt_image_2_skill, CC BY 4.0" in text


def test_render_markdown_handles_no_memory() -> None:
    """memory=None 時不應出現 Design Memory section。"""
    text = MarkdownExporter().render_markdown(
        memory=None,
        prompt="x",
        image_name=None,
        meta=ExportMetadata(),
    )
    assert "## Design Memory" not in text
    assert "## Generated Image" not in text


def test_image_edit_panel_export_md_button_state(qtbot, tmp_path: Path) -> None:
    """生成前 disabled，set _last_result 後 enabled，busy 期間又 disabled。"""
    panel = ImageEditPanel(client_factory=_no_client)
    qtbot.addWidget(panel)
    assert panel.export_md_btn.isEnabled() is False
    from app.api.openai_client import ImageResult
    panel._on_worker_finished(ImageResult(data=b"fake"))
    assert panel.export_md_btn.isEnabled() is True
    # busy 期間應 disable（Codex Major fix：避免匯出新 prompt + 舊圖）
    panel._set_busy(True)
    assert panel.export_md_btn.isEnabled() is False


def test_markdown_export_includes_prompt_defaults(tmp_path: Path) -> None:
    """完整 v2.5 memory：prompt_defaults 應出現在 Design Memory section。"""
    memory = DesignMemory(
        brand_name="ACME",
        prompt_defaults={"size": "portrait", "quality": "high"},
    )
    out = export_markdown(
        memory, "p", None, tmp_path / "x.md"
    )
    text = out.read_text(encoding="utf-8")
    assert "Prompt defaults:" in text
    assert "size=portrait" in text


def test_markdown_export_overwrites_sidecar(tmp_path: Path) -> None:
    """同名 .png sidecar 已存在時覆蓋（釘住行為）。"""
    md_path = tmp_path / "x.md"
    png_path = tmp_path / "x.png"
    png_path.write_bytes(b"old-bytes")
    export_markdown(None, "p", b"new-bytes", md_path)
    assert png_path.read_bytes() == b"new-bytes"
