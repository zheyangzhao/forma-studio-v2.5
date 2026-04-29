"""Markdown export（v3.0 Sprint 3B）。

對應 PLAN-sprint-3.md §三。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from app.utils.design_memory import DesignMemory


SCHEMA_VERSION = 1
DEFAULT_TIMEZONE = "Asia/Taipei"


def _now_iso() -> str:
    return datetime.now(ZoneInfo(DEFAULT_TIMEZONE)).isoformat()


@dataclass(frozen=True)
class ExportMetadata:
    export_type: str = "markdown"
    created_at: str = field(default_factory=_now_iso)
    quality: str | None = None
    source_attribution: list[str] = field(default_factory=list)


def _yaml_escape(value: str) -> str:
    # YAML frontmatter 用雙引號字串：只 escape backslash 與 quote
    return value.replace("\\", "\\\\").replace('"', '\\"')


class MarkdownExporter:
    """產出 frontmatter + body 的 Markdown export。

    對外 API：`MarkdownExporter().export(...)` 或 `render_markdown(...)`。
    GUI 走 module-level `export_markdown(...)` 包裝。
    """

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
        if out_path.suffix.lower() != ".md":
            raise ValueError("out_path must end with .md")

        out_path.parent.mkdir(parents=True, exist_ok=True)
        image_name = self._write_image_sidecar(out_path, image_bytes)
        meta = ExportMetadata(
            quality=quality,
            source_attribution=source_attribution or [],
        )
        text = self.render_markdown(
            memory=memory,
            prompt=prompt.strip(),
            image_name=image_name,
            meta=meta,
        )
        out_path.write_text(text, encoding="utf-8")
        return out_path

    def render_markdown(
        self,
        *,
        memory: DesignMemory | None,
        prompt: str,
        image_name: str | None,
        meta: ExportMetadata,
    ) -> str:
        title = (
            memory.project_name
            if memory and memory.project_name
            else "Forma Studio Export"
        )
        lines: list[str] = []
        lines.extend(self._frontmatter(memory, image_name, meta))
        lines.append(f"# {title}")
        lines.append("")
        lines.append("## Prompt")
        lines.append("")
        lines.append(prompt)
        lines.append("")
        lines.extend(self._memory_section(memory))
        lines.extend(self._image_section(image_name))
        lines.extend(self._attribution_section(meta.source_attribution))
        return "\n".join(lines).rstrip() + "\n"

    # ── private helpers ────────────────────────────
    def _frontmatter(
        self,
        memory: DesignMemory | None,
        image_name: str | None,
        meta: ExportMetadata,
    ) -> list[str]:
        lines = [
            "---",
            f"schema_version: {SCHEMA_VERSION}",
            f'export_type: "{meta.export_type}"',
            f'created_at: "{meta.created_at}"',
        ]
        if memory and memory.project_name:
            lines.append(f'project_name: "{_yaml_escape(memory.project_name)}"')
        if memory and memory.brand_name:
            lines.append(f'brand_name: "{_yaml_escape(memory.brand_name)}"')
        if memory and memory.industry:
            lines.append(f'industry: "{_yaml_escape(memory.industry)}"')
        if meta.quality:
            lines.append(f'quality: "{_yaml_escape(meta.quality)}"')
        if image_name:
            lines.append(f'image_file: "{_yaml_escape(image_name)}"')
        lines.append("---")
        lines.append("")
        return lines

    def _memory_section(self, memory: DesignMemory | None) -> list[str]:
        if memory is None or memory.is_empty():
            return []
        lines = ["## Design Memory", ""]
        if memory.brand_name:
            lines.append(f"- Brand: {memory.brand_name}")
        if memory.industry:
            lines.append(f"- Industry: {memory.industry}")
        if memory.audience:
            lines.append(f"- Audience: {', '.join(memory.audience)}")
        if memory.tone_of_voice:
            lines.append(f"- Tone: {memory.tone_of_voice}")
        if memory.color_tokens:
            lines.append(
                "- Colors: "
                + ", ".join(f"{k}={v}" for k, v in memory.color_tokens.items())
            )
        if memory.typography:
            lines.append(
                "- Typography: "
                + ", ".join(f"{k}={v}" for k, v in memory.typography.items())
            )
        if memory.visual_rules:
            lines.append("- Visual rules: " + "; ".join(memory.visual_rules))
        if memory.prompt_defaults:
            lines.append(
                "- Prompt defaults: "
                + ", ".join(f"{k}={v}" for k, v in memory.prompt_defaults.items())
            )
        if memory.negative_constraints:
            lines.append(
                "- Negative: " + "; ".join(memory.negative_constraints)
            )
        # v3.0 4 個 optional 欄位（PLAN §3.2）
        if memory.spacing_tokens:
            lines.append(
                "- Spacing/Layout: "
                + ", ".join(f"{k}={v}" for k, v in memory.spacing_tokens.items())
            )
        if memory.components:
            lines.append("- Components: " + "; ".join(memory.components))
        if memory.motion:
            lines.append(
                "- Motion: "
                + ", ".join(f"{k}={v}" for k, v in memory.motion.items())
            )
        if memory.voice_signals:
            lines.append("- Voice/Copy: " + "; ".join(memory.voice_signals))
        lines.append("")
        return lines

    def _image_section(self, image_name: str | None) -> list[str]:
        if not image_name:
            return []
        return [
            "## Generated Image",
            "",
            f"![Generated image]({image_name})",
            "",
        ]

    def _attribution_section(self, items: list[str]) -> list[str]:
        if not items:
            return []
        lines = ["## Source Attribution", ""]
        lines.extend(f"- {item}" for item in items)
        lines.append("")
        return lines

    def _write_image_sidecar(
        self, out_path: Path, image_bytes: bytes | None
    ) -> str | None:
        if not image_bytes:
            return None
        # 與 .md 同名同目錄的 .png sidecar
        image_path = out_path.with_suffix(".png")
        image_path.write_bytes(image_bytes)
        return image_path.name


def export_markdown(
    memory: DesignMemory | None,
    prompt: str,
    image_bytes: bytes | None,
    out_path: Path,
    *,
    quality: str | None = None,
    source_attribution: list[str] | None = None,
) -> Path:
    """GUI / 外部呼叫的 module-level entry。"""
    return MarkdownExporter().export(
        memory=memory,
        prompt=prompt,
        image_bytes=image_bytes,
        out_path=out_path,
        quality=quality,
        source_attribution=source_attribution,
    )
