"""DESIGN.md 解析、驗證、序列化、注入 system prompt。

對應 SDD-v2.5 §4.3 共享記憶、PLAN-sprint-2.md §4.1 / §4.4。

DESIGN.md schema（六大區塊）：

```markdown
# Forma Studio · DESIGN.md

## Brand Identity
- project_name: 範例專案
- brand_name: ACME Corp
- industry: legal
- audience: 律師, 企業客戶
- tone_of_voice: 嚴肅高端

## Color Tokens

| token | value |
|---|---|
| primary | oklch(55% 0.18 250) |
| secondary | oklch(75% 0.10 90) |

## Typography
- heading: Noto Serif TC
- body: Noto Sans TC

## Visual Rules
- 不用 emoji 圖標
- 不用紫漸層

## Prompt Defaults
- size: portrait
- quality: high

## Negative Constraints
- watermark
- fake brand logo
```
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

DESIGN_FILENAME = "DESIGN.md"


@dataclass
class DesignMemory:
    project_name: str = ""
    brand_name: str = ""
    industry: str = ""
    audience: list[str] = field(default_factory=list)
    tone_of_voice: str = ""
    color_tokens: dict[str, str] = field(default_factory=dict)
    typography: dict[str, str] = field(default_factory=dict)
    visual_rules: list[str] = field(default_factory=list)
    prompt_defaults: dict[str, str] = field(default_factory=dict)
    negative_constraints: list[str] = field(default_factory=list)

    def is_empty(self) -> bool:
        return not any(asdict(self).values())


# ── parsing ─────────────────────────────────────────────
_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
_BULLET_KV_RE = re.compile(r"^\s*-\s+([^:：]+)[:：]\s*(.+?)\s*$")
_BULLET_LIST_RE = re.compile(r"^\s*-\s+(.+?)\s*$")
# 接受 ≥2 欄 markdown table（SDD §4.3 範例可能含 Usage 欄等多欄；只取前兩欄）
_TABLE_ROW_RE = re.compile(r"^\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|.*$")


def _split_sections(text: str) -> dict[str, list[str]]:
    """切分 markdown 文字成 {section_title: [lines]}。"""
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        m = _HEADING_RE.match(line)
        if m:
            current = m.group(1).strip()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def _parse_kv_lines(lines: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in lines:
        m = _BULLET_KV_RE.match(line)
        if m:
            key = m.group(1).strip().lower().replace(" ", "_")
            out[key] = m.group(2).strip()
    return out


def _parse_list_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        m = _BULLET_LIST_RE.match(line)
        if m and ":" not in m.group(1) and "：" not in m.group(1):
            out.append(m.group(1).strip())
    return out


def _parse_table_lines(lines: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    seen_header = False
    for line in lines:
        m = _TABLE_ROW_RE.match(line)
        if not m:
            continue
        left, right = m.group(1).strip(), m.group(2).strip()
        # 跳過 header 與 separator
        if not seen_header and left.lower() in {"token", "key", "name"}:
            seen_header = True
            continue
        if set(left + right) <= set("-:| "):
            continue
        out[left] = right
    return out


def _parse_audience(value: str) -> list[str]:
    """audience 欄位可能是 `律師, 企業客戶` 或 `律師、企業客戶`。"""
    if not value:
        return []
    parts = re.split(r"[,，、;；/]", value)
    return [p.strip() for p in parts if p.strip()]


def parse_design_memory(text: str) -> DesignMemory:
    sections = _split_sections(text)
    memory = DesignMemory()

    if "Brand Identity" in sections:
        kv = _parse_kv_lines(sections["Brand Identity"])
        memory.project_name = kv.get("project_name", "")
        memory.brand_name = kv.get("brand_name", "")
        memory.industry = kv.get("industry", "")
        memory.tone_of_voice = kv.get("tone_of_voice", "")
        memory.audience = _parse_audience(kv.get("audience", ""))

    if "Color Tokens" in sections:
        memory.color_tokens = _parse_table_lines(sections["Color Tokens"])

    if "Typography" in sections:
        memory.typography = _parse_kv_lines(sections["Typography"])

    if "Visual Rules" in sections:
        memory.visual_rules = _parse_list_lines(sections["Visual Rules"])

    if "Prompt Defaults" in sections:
        memory.prompt_defaults = _parse_kv_lines(sections["Prompt Defaults"])

    if "Negative Constraints" in sections:
        memory.negative_constraints = _parse_list_lines(
            sections["Negative Constraints"]
        )

    return memory


# ── validation ──────────────────────────────────────────
def validate_design_memory(memory: DesignMemory) -> list[str]:
    """回 warning list；空 list 代表 OK。"""
    warnings: list[str] = []
    if not memory.brand_name:
        warnings.append("缺 brand_name")
    if memory.color_tokens:
        for tok, val in memory.color_tokens.items():
            if not val:
                warnings.append(f"color token '{tok}' 沒值")
    return warnings


# ── serialization ───────────────────────────────────────
def _emit_kv(out: list[str], items: dict[str, str]) -> None:
    for k, v in items.items():
        out.append(f"- {k}: {v}")


def memory_to_markdown(memory: DesignMemory) -> str:
    out: list[str] = ["# Forma Studio · DESIGN.md", ""]

    out.append("## Brand Identity")
    out.append(f"- project_name: {memory.project_name}")
    out.append(f"- brand_name: {memory.brand_name}")
    out.append(f"- industry: {memory.industry}")
    out.append(f"- audience: {', '.join(memory.audience)}")
    out.append(f"- tone_of_voice: {memory.tone_of_voice}")
    out.append("")

    out.append("## Color Tokens")
    out.append("")
    if memory.color_tokens:
        out.append("| token | value |")
        out.append("|---|---|")
        for tok, val in memory.color_tokens.items():
            out.append(f"| {tok} | {val} |")
    out.append("")

    out.append("## Typography")
    _emit_kv(out, memory.typography)
    out.append("")

    out.append("## Visual Rules")
    for rule in memory.visual_rules:
        out.append(f"- {rule}")
    out.append("")

    out.append("## Prompt Defaults")
    _emit_kv(out, memory.prompt_defaults)
    out.append("")

    out.append("## Negative Constraints")
    for item in memory.negative_constraints:
        out.append(f"- {item}")
    out.append("")

    return "\n".join(out)


def save_design_memory(project_dir: Path, memory: DesignMemory) -> Path:
    project_dir.mkdir(parents=True, exist_ok=True)
    path = project_dir / DESIGN_FILENAME
    path.write_text(memory_to_markdown(memory), encoding="utf-8")
    return path


def load_design_memory(project_dir: Path) -> DesignMemory | None:
    path = project_dir / DESIGN_FILENAME
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    return parse_design_memory(text)


# ── system prompt 注入 ──────────────────────────────────
def build_system_prompt(base: str, memory: DesignMemory | None) -> str:
    """把 memory 摘要 prepend 到既有 system prompt。"""
    if memory is None or memory.is_empty():
        return base
    lines = ["[Project DESIGN.md memory]"]
    if memory.brand_name:
        lines.append(f"- Brand: {memory.brand_name}")
    if memory.industry:
        lines.append(f"- Industry: {memory.industry}")
    if memory.audience:
        lines.append(f"- Audience: {', '.join(memory.audience)}")
    if memory.tone_of_voice:
        lines.append(f"- Tone: {memory.tone_of_voice}")
    if memory.color_tokens:
        cols = ", ".join(f"{k}={v}" for k, v in memory.color_tokens.items())
        lines.append(f"- Colors: {cols}")
    if memory.typography:
        typ = ", ".join(f"{k}={v}" for k, v in memory.typography.items())
        lines.append(f"- Typography: {typ}")
    if memory.visual_rules:
        lines.append("- Visual rules: " + "; ".join(memory.visual_rules))
    if memory.negative_constraints:
        lines.append(
            "- Negative: " + "; ".join(memory.negative_constraints)
        )
    return "\n".join(lines) + "\n\n" + base


def apply_design_memory_to_prompt(
    prompt: str, memory: DesignMemory | None
) -> str:
    """把 memory 摘要 prepend 到使用者 prompt（用於 generate/edit 不 system role 場景）。"""
    if memory is None or memory.is_empty():
        return prompt
    return build_system_prompt("User prompt:\n" + prompt, memory).replace(
        "[Project DESIGN.md memory]",
        "[Project DESIGN.md memory — apply to all output below]",
        1,
    )
