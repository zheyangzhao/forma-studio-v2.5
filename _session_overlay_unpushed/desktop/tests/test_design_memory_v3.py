"""Sprint 3A v3.0 schema 擴充 unit tests（PLAN-sprint-3 §2.7）。"""

from __future__ import annotations

from pathlib import Path

from app.utils.design_memory import (
    DesignMemory,
    apply_design_memory_to_prompt,
    build_system_prompt,
    load_design_memory,
    memory_to_markdown,
    parse_design_memory,
    parse_design_memory_with_warnings,
    save_design_memory,
)


V25_LEGACY_MD = """# Forma Studio · DESIGN.md

## Brand Identity
- brand_name: ACME

## Color Tokens

| token | value |
|---|---|
| primary | #ff0000 |

## Typography
- heading: Noto Serif TC

## Visual Rules
- 不用紫漸層

## Negative Constraints
- watermark
"""

V3_FULL_MD = V25_LEGACY_MD + """
## Spacing & Layout

| token | value |
|---|---|
| spacing_base | 4px |
| container_max | 1120px |

## Components
- Button: 8px radius, icon-only when symbol is familiar
- Card: only for repeated items

## Motion
- duration_fast: 120ms
- easing_standard: cubic-bezier(0.2, 0, 0, 1)

## Voice & Copy
- 直接、克制、可驗證
- 避免空泛口號
"""


def test_v25_design_md_still_parses() -> None:
    """v2.5 寫的 DESIGN.md 內容，v3.0 parser 應正確讀，新欄位回 default。"""
    m = parse_design_memory(V25_LEGACY_MD)
    assert m.brand_name == "ACME"
    assert m.color_tokens == {"primary": "#ff0000"}
    # v3 新欄位都應為 default
    assert m.spacing_tokens == {}
    assert m.components == []
    assert m.motion == {}
    assert m.voice_signals == []


def test_v3_full_schema_parse() -> None:
    """9 區塊全填 → parse 正確，所有欄位都有值。"""
    m = parse_design_memory(V3_FULL_MD)
    assert m.brand_name == "ACME"
    assert m.spacing_tokens == {"spacing_base": "4px", "container_max": "1120px"}
    assert "Button: 8px radius, icon-only when symbol is familiar" in m.components
    assert m.motion["duration_fast"] == "120ms"
    assert "直接、克制、可驗證" in m.voice_signals


def test_v3_full_schema_roundtrip(tmp_path: Path) -> None:
    """save → load 後 v3 欄位仍一致。"""
    original = parse_design_memory(V3_FULL_MD)
    save_design_memory(tmp_path, original)
    reloaded = load_design_memory(tmp_path)
    assert reloaded is not None
    assert reloaded.spacing_tokens == original.spacing_tokens
    assert reloaded.components == original.components
    assert reloaded.motion == original.motion
    assert reloaded.voice_signals == original.voice_signals


def test_serializer_skips_empty_v3_sections() -> None:
    """v3 欄位空時不應 emit section（避免空 ## Spacing & Layout）。"""
    m = DesignMemory(brand_name="X")
    md = memory_to_markdown(m)
    assert "## Spacing & Layout" not in md
    assert "## Components" not in md
    assert "## Motion" not in md
    assert "## Voice & Copy" not in md


def test_serializer_emits_only_filled_v3_sections() -> None:
    """部分 v3 欄位有值時，只 emit 有值的 section。"""
    m = DesignMemory(brand_name="X", components=["Button: rounded"])
    md = memory_to_markdown(m)
    assert "## Components" in md
    assert "Button: rounded" in md
    assert "## Spacing & Layout" not in md
    assert "## Motion" not in md


def test_build_system_prompt_includes_v3_fields() -> None:
    """system prompt 含 spacing / components / motion / voice。"""
    m = parse_design_memory(V3_FULL_MD)
    sp = build_system_prompt("BASE", m)
    assert "Spacing:" in sp
    assert "spacing_base=4px" in sp
    assert "Components:" in sp
    assert "Motion:" in sp
    assert "Voice:" in sp


def test_apply_design_memory_to_prompt_v3() -> None:
    """apply 含新欄位摘要。"""
    m = parse_design_memory(V3_FULL_MD)
    out = apply_design_memory_to_prompt("draw a logo", m)
    assert "draw a logo" in out
    assert "Spacing:" in out
    assert "Components:" in out


def test_parse_warns_on_section_typo() -> None:
    """section typo（如 Voice & Tone）應 warning，不 crash。"""
    md = V25_LEGACY_MD + "\n## Voice & Tone\n- 直接\n"
    result = parse_design_memory_with_warnings(md)
    assert any("Voice & Tone" in w and "Voice & Copy" in w for w in result.warnings)
    # parser 仍回 valid memory（只是 typo section 被忽略，不 crash）
    assert result.memory.brand_name == "ACME"


def test_parse_warns_on_motion_empty_value() -> None:
    """Motion 欄位有 key 但無 value 應 warning。"""
    md = V25_LEGACY_MD + "\n## Motion\n- duration_fast:\n"
    result = parse_design_memory_with_warnings(md)
    assert any("Motion" in w and "duration_fast" in w for w in result.warnings)


def test_parse_with_warnings_back_compat_no_typos() -> None:
    """乾淨 v3 markdown 應 0 warnings。"""
    result = parse_design_memory_with_warnings(V3_FULL_MD)
    assert result.warnings == []
