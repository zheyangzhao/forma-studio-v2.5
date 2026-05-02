"""PDF export（v3.0 Sprint 3C，M2 Phase 2）。

對應 PLAN-sprint-3.md §四。

工具：reportlab（純 Python、可控 layout）
字型：Noto Sans TC（OFL 1.1，desktop/assets/fonts/NotoSansTC-Regular.ttf）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape as _xml_escape
from zoneinfo import ZoneInfo

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.utils.design_memory import DesignMemory


SCHEMA_VERSION = 1
FONT_NAME = "NotoSansTC"
DEFAULT_TIMEZONE = "Asia/Taipei"


def _default_font_path() -> Path:
    """從 assets/fonts/ 讀預設字型；PyInstaller bundle 也會放 Resources/。"""
    import sys

    candidates: list[Path] = []
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates.append(Path(meipass) / "assets" / "fonts" / "NotoSansTC-Regular.ttf")
        candidates.append(
            Path(meipass).parent / "Resources" / "assets" / "fonts" / "NotoSansTC-Regular.ttf"
        )
    # 開發環境：desktop/assets/fonts/
    repo_path = (
        Path(__file__).resolve().parents[3]
        / "assets"
        / "fonts"
        / "NotoSansTC-Regular.ttf"
    )
    candidates.append(repo_path)
    for path in candidates:
        if path.exists():
            return path
    # 都找不到也回第一個 expected path（讓 register 階段 raise FileNotFoundError）
    return candidates[0] if candidates else repo_path


def _now_iso() -> str:
    return datetime.now(ZoneInfo(DEFAULT_TIMEZONE)).isoformat()


def _safe_title(memory: DesignMemory | None) -> str:
    if memory and memory.project_name and memory.project_name.strip():
        return memory.project_name.strip()
    return "Forma Studio Export"


def _escape(value: str) -> str:
    """XML escape 給 Paragraph 用。"""
    return _xml_escape(value, {'"': "&quot;", "'": "&apos;"})


@dataclass(frozen=True)
class PDFExportMetadata:
    created_at: str = field(default_factory=_now_iso)
    quality: str | None = None
    source_attribution: list[str] = field(default_factory=list)


class PDFExporter:
    """產出 A4 PDF report：cover + image + prompt + memory + attribution。"""

    def __init__(self, font_path: Path | None = None) -> None:
        self.font_path = font_path or _default_font_path()
        self._font_registered = False

    def export(
        self,
        *,
        memory: DesignMemory | None,
        prompt: str,
        image_bytes: bytes | None,
        out_path: Path,
        quality: str | None = None,
        source_attribution: list[str] | None = None,
    ) -> Path:
        if not prompt.strip():
            raise ValueError("prompt is required")
        if out_path.suffix.lower() != ".pdf":
            raise ValueError("out_path must end with .pdf")

        out_path.parent.mkdir(parents=True, exist_ok=True)
        self._register_font()
        meta = PDFExportMetadata(
            quality=quality,
            source_attribution=source_attribution or [],
        )

        doc = SimpleDocTemplate(
            str(out_path),
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=16 * mm,
            title=_safe_title(memory),
            author="Forma Studio",
        )
        story = self._build_story(memory, prompt.strip(), image_bytes, meta)
        footer_callback = self._make_footer(meta)
        doc.build(story, onFirstPage=footer_callback, onLaterPages=footer_callback)
        return out_path

    # ── font ────────────────────────────────────────────
    def _register_font(self) -> None:
        if self._font_registered:
            return
        if not self.font_path.exists():
            raise FileNotFoundError(
                f"PDF font missing: {self.font_path}. "
                "Install or bundle NotoSansTC-Regular.ttf 到 desktop/assets/fonts/。"
            )
        # registerFont 重複 register 同名 OK，PDFExporter 內部 cache
        pdfmetrics.registerFont(TTFont(FONT_NAME, str(self.font_path)))
        self._font_registered = True

    # ── styles ──────────────────────────────────────────
    def _styles(self) -> dict[str, ParagraphStyle]:
        base = getSampleStyleSheet()
        return {
            "title": ParagraphStyle(
                "FormaTitle",
                parent=base["Title"],
                fontName=FONT_NAME,
                fontSize=18,
                leading=24,
                spaceAfter=10,
            ),
            "heading": ParagraphStyle(
                "FormaHeading",
                parent=base["Heading2"],
                fontName=FONT_NAME,
                fontSize=12,
                leading=16,
                spaceBefore=10,
                spaceAfter=6,
            ),
            "body": ParagraphStyle(
                "FormaBody",
                parent=base["BodyText"],
                fontName=FONT_NAME,
                fontSize=9.5,
                leading=14,
            ),
            "mono": ParagraphStyle(
                "FormaPrompt",
                parent=base["BodyText"],
                fontName=FONT_NAME,
                fontSize=9,
                leading=13,
                backColor=colors.HexColor("#f3f4f6"),
                borderPadding=6,
            ),
            "footer": ParagraphStyle(
                "FormaFooter",
                parent=base["BodyText"],
                fontName=FONT_NAME,
                fontSize=8,
                leading=10,
                textColor=colors.HexColor("#64748b"),
            ),
        }

    # ── story ───────────────────────────────────────────
    def _build_story(
        self,
        memory: DesignMemory | None,
        prompt: str,
        image_bytes: bytes | None,
        meta: PDFExportMetadata,
    ) -> list:
        styles = self._styles()
        story: list = []
        story.append(Paragraph(_escape(_safe_title(memory)), styles["title"]))
        story.append(self._metadata_table(memory, meta))
        story.append(Spacer(1, 8 * mm))

        if image_bytes:
            story.append(self._image_flowable(image_bytes))
            story.append(Spacer(1, 8 * mm))
            # PLAN §4.2：Page 1 cover (metadata + image)、Page 2+ prompt/memory
            story.append(PageBreak())

        story.append(Paragraph("Prompt", styles["heading"]))
        story.append(
            Paragraph(_escape(prompt).replace("\n", "<br/>"), styles["mono"])
        )

        memory_lines = self._memory_lines(memory)
        if memory_lines:
            story.append(Paragraph("Design Memory", styles["heading"]))
            for line in memory_lines:
                story.append(Paragraph(_escape(line), styles["body"]))

        if meta.source_attribution:
            story.append(Paragraph("Source Attribution", styles["heading"]))
            for item in meta.source_attribution:
                story.append(Paragraph(_escape(f"- {item}"), styles["body"]))

        return story

    def _metadata_table(
        self,
        memory: DesignMemory | None,
        meta: PDFExportMetadata,
    ) -> Table:
        rows = [
            ["Created at", meta.created_at],
            ["Schema", f"export.v{SCHEMA_VERSION}"],
        ]
        if meta.quality:
            rows.append(["Quality", meta.quality])
        if memory and memory.brand_name:
            rows.append(["Brand", memory.brand_name])
        if memory and memory.industry:
            rows.append(["Industry", memory.industry])
        if memory and memory.audience:
            rows.append(["Audience", ", ".join(memory.audience)])

        table = Table(rows, colWidths=[32 * mm, 120 * mm])
        table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
                    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#475569")),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cbd5e1")),
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f8fafc")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        return table

    def _image_flowable(self, image_bytes: bytes) -> Image:
        # 限制最大顯示尺寸，避免長圖佔滿頁面
        max_width = A4[0] - 36 * mm  # 18mm * 2 = 36
        max_height = 110 * mm
        image = Image(BytesIO(image_bytes))
        # reportlab Image.drawWidth/drawHeight 可以後設
        if image.imageWidth and image.imageHeight:
            ratio = image.imageHeight / image.imageWidth
            draw_w = min(max_width, image.imageWidth)
            draw_h = draw_w * ratio
            if draw_h > max_height:
                draw_h = max_height
                draw_w = draw_h / ratio
            image.drawWidth = draw_w
            image.drawHeight = draw_h
        return image

    def _memory_lines(self, memory: DesignMemory | None) -> list[str]:
        if memory is None or memory.is_empty():
            return []
        lines: list[str] = []
        # v2.5 Brand Identity（Codex Major fix：metadata table 有 Brand/Industry/Audience，
        # 但 Design Memory section 自身也應完整列出）
        if memory.project_name:
            lines.append(f"Project: {memory.project_name}")
        if memory.brand_name:
            lines.append(f"Brand: {memory.brand_name}")
        if memory.industry:
            lines.append(f"Industry: {memory.industry}")
        if memory.audience:
            lines.append(f"Audience: {', '.join(memory.audience)}")
        if memory.tone_of_voice:
            lines.append(f"Tone: {memory.tone_of_voice}")
        if memory.color_tokens:
            lines.append(
                "Colors: "
                + ", ".join(f"{k}={v}" for k, v in memory.color_tokens.items())
            )
        if memory.typography:
            lines.append(
                "Typography: "
                + ", ".join(f"{k}={v}" for k, v in memory.typography.items())
            )
        if memory.visual_rules:
            lines.append("Visual rules: " + "; ".join(memory.visual_rules))
        if memory.prompt_defaults:
            lines.append(
                "Prompt defaults: "
                + ", ".join(f"{k}={v}" for k, v in memory.prompt_defaults.items())
            )
        if memory.negative_constraints:
            lines.append(
                "Negative: " + "; ".join(memory.negative_constraints)
            )
        # v3.0 4 個 optional
        if memory.spacing_tokens:
            lines.append(
                "Spacing/Layout: "
                + ", ".join(f"{k}={v}" for k, v in memory.spacing_tokens.items())
            )
        if memory.components:
            lines.append("Components: " + "; ".join(memory.components))
        if memory.motion:
            lines.append(
                "Motion: "
                + ", ".join(f"{k}={v}" for k, v in memory.motion.items())
            )
        if memory.voice_signals:
            lines.append("Voice/Copy: " + "; ".join(memory.voice_signals))
        return lines

    def _make_footer(self, meta: PDFExportMetadata):
        """產 onPage 回呼，畫頁碼與 timestamp。"""
        font_name = FONT_NAME

        def draw(canvas, doc) -> None:
            canvas.saveState()
            canvas.setFont(font_name, 8)
            canvas.setFillColor(colors.HexColor("#64748b"))
            footer_text = (
                f"Forma Studio · export.v{SCHEMA_VERSION} · "
                f"{meta.created_at} · page {doc.page}"
            )
            canvas.drawString(18 * mm, 10 * mm, footer_text)
            canvas.restoreState()

        return draw


def export_pdf(
    memory: DesignMemory | None,
    prompt: str,
    image_bytes: bytes | None,
    out_path: Path,
    *,
    quality: str | None = None,
    source_attribution: list[str] | None = None,
) -> Path:
    """GUI / 外部呼叫的 module-level entry。"""
    return PDFExporter().export(
        memory=memory,
        prompt=prompt,
        image_bytes=image_bytes,
        out_path=out_path,
        quality=quality,
        source_attribution=source_attribution,
    )
