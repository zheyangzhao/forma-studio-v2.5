"""DESIGN.md 解析、驗證、序列化、注入 system prompt。

v2.5：6 區塊（Brand Identity / Color Tokens / Typography / Visual Rules / Prompt Defaults / Negative Constraints）
v3.0：+4 optional 區塊（Spacing & Layout / Components / Motion / Voice & Copy）

對應 SDD-v2.5 §4.3、PLAN-sprint-2.md §4.1 / §4.4、PLAN-sprint-3.md §二。

DESIGN.md schema：

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

## Spacing & Layout
| token | value |
|---|---|
| spacing_base | 4px |
| container_max | 1120px |

## Components
- Button: 8px radius, icon-only when symbol is familiar

## Motion
- duration_fast: 120ms
- easing_standard: cubic-bezier(0.2, 0, 0, 1)

## Voice & Copy
- 直接、克制、可驗證
- 避免空泛口號
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

    # v3.0 新增 4 個 optional 欄位（PLAN-sprint-3 §2.3）
    spacing_tokens: dict[str, str] = field(default_factory=dict)
    components: list[str] = field(default_factory=list)
    motion: dict[str, str] = field(default_factory=dict)
    voice_signals: list[str] = field(default_factory=list)

    def is_empty(self) -> bool:
        return not any(asdict(self).values())


@dataclass
class ParseResult:
    """v3.0：parser 同時回 memory + warnings list（warning 不 raise）。"""
    memory: DesignMemory
    warnings: list[str] = field(default_factory=list)


# v3.0 新增 sections（optional）
V3_OPTIONAL_SECTIONS = {
    "Spacing & Layout",
    "Components",
    "Motion",
    "Voice & Copy",
}

# 常見 typo → 預期 section 名稱（warning hint）
SECTION_TYPO_HINTS = {
    "Spacing Layout": "Spacing & Layout",
    "Voice and Copy": "Voice & Copy",
    "Voice & Tone": "Voice & Copy",
    "Component": "Components",
    "Negative Constraint": "Negative Constraints",
}


# ── parsing ─────────────────────────────────────────────
_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
_BULLET_KV_RE = re.compile(r"^\s*-\s+([^:：]+)[:：]\s*(.+?)\s*$")
# v3.0：lenient kv 接受空 value（給 motion empty value warning 用）
_BULLET_KV_LENIENT_RE = re.compile(r"^\s*-\s+([^:：]+)[:：]\s*(.*?)\s*$")
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
    """v2.5 list parser：排除含 `:` 的行（避免 kv 被誤抓為 list）。"""
    out: list[str] = []
    for line in lines:
        m = _BULLET_LIST_RE.match(line)
        if m and ":" not in m.group(1) and "：" not in m.group(1):
            out.append(m.group(1).strip())
    return out


def _parse_text_lines(lines: list[str]) -> list[str]:
    """v3.0：完整收集 bullet 行（含 `:`）。給 Components / Voice & Copy 用。"""
    out: list[str] = []
    for line in lines:
        m = _BULLET_LIST_RE.match(line)
        if m:
            text = m.group(1).strip()
            if text:
                out.append(text)
    return out


def _parse_kv_lenient(lines: list[str]) -> dict[str, str]:
    """v3.0：接受空 value 的 kv parser；給 Motion empty value warning 用。"""
    out: dict[str, str] = {}
    for line in lines:
        m = _BULLET_KV_LENIENT_RE.match(line)
        if m:
            key = m.group(1).strip().lower().replace(" ", "_")
            out[key] = m.group(2).strip()
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


def parse_design_memory_with_warnings(text: str) -> ParseResult:
    """v3.0 parser：解析 9 區塊（v2.5 6 + v3 4 optional），回 memory + warnings。"""
    sections = _split_sections(text)
    memory = DesignMemory()
    warnings: list[str] = []

    # ── v2.5 stable sections（行為不變）──
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

    # ── v3.0 optional sections ──
    if "Spacing & Layout" in sections:
        # table 優先；fallback bullet kv
        spacing_lines = sections["Spacing & Layout"]
        table_values = _parse_table_lines(spacing_lines)
        bullet_values = _parse_kv_lines(spacing_lines)
        memory.spacing_tokens = table_values or bullet_values
        # 對非 table / 非 kv 的行 warning（PLAN §2.3）
        for line in spacing_lines:
            text = line.strip()
            if not text or text.startswith("|") or text.startswith("-"):
                continue
            warnings.append(f"Spacing & Layout 無法解析行：{text[:80]}")

    if "Components" in sections:
        # Components 行可能含 `:` (e.g. "Button: 8px radius")，需用 _parse_text_lines
        memory.components = _parse_text_lines(sections["Components"])

    if "Motion" in sections:
        # 用 lenient kv 接受空 value，方便產 warning
        memory.motion = _parse_kv_lenient(sections["Motion"])
        for key, value in memory.motion.items():
            if not value:
                warnings.append(f"Motion 欄位 '{key}' 沒值")

    if "Voice & Copy" in sections:
        # Voice 也可能含 `:`，用 _parse_text_lines
        memory.voice_signals = _parse_text_lines(sections["Voice & Copy"])

    # ── typo 偵測（warning 不 raise；即使 expected 也存在也 warn 提示重複）──
    for seen, expected in SECTION_TYPO_HINTS.items():
        if seen in sections:
            warnings.append(
                f"疑似 section typo：'{seen}'，是否要寫成 '{expected}'"
            )

    return ParseResult(memory=memory, warnings=warnings)


def parse_design_memory(text: str) -> DesignMemory:
    """保留 v2.5 public API；呼叫者不需要處理 warnings。"""
    return parse_design_memory_with_warnings(text).memory


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

    # v3.0 optional sections：有值才 emit，避免空 section
    if memory.spacing_tokens:
        out.append("## Spacing & Layout")
        out.append("")
        out.append("| token | value |")
        out.append("|---|---|")
        for token, value in memory.spacing_tokens.items():
            out.append(f"| {token} | {value} |")
        out.append("")

    if memory.components:
        out.append("## Components")
        for c in memory.components:
            out.append(f"- {c}")
        out.append("")

    if memory.motion:
        out.append("## Motion")
        _emit_kv(out, memory.motion)
        out.append("")

    if memory.voice_signals:
        out.append("## Voice & Copy")
        for v in memory.voice_signals:
            out.append(f"- {v}")
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
    # v3.0：4 個 optional 欄位有值才注入；做摘要化（PLAN §2.6 cap：避免長 schema 灌爆 prompt）
    if memory.spacing_tokens:
        spacing_items = list(memory.spacing_tokens.items())[:12]
        spacing = ", ".join(f"{k}={v}" for k, v in spacing_items)
        lines.append(f"- Spacing: {spacing}")
    if memory.components:
        lines.append("- Components: " + "; ".join(memory.components[:12]))
    if memory.motion:
        motion_items = list(memory.motion.items())[:8]
        motion = ", ".join(f"{k}={v}" for k, v in motion_items)
        lines.append(f"- Motion: {motion}")
    if memory.voice_signals:
        lines.append("- Voice: " + "; ".join(memory.voice_signals[:8]))
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
