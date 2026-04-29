"""Sprint 2C design_memory unit tests（不需 PyQt6）。

對應 PLAN-sprint-2.md §4.5。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.utils.design_memory import (
    DESIGN_FILENAME,
    DesignMemory,
    apply_design_memory_to_prompt,
    build_system_prompt,
    load_design_memory,
    memory_to_markdown,
    parse_design_memory,
    save_design_memory,
    validate_design_memory,
)


SAMPLE_MD = """# Forma Studio · DESIGN.md

## Brand Identity
- project_name: 範例專案
- brand_name: ACME Corp
- industry: legal
- audience: 律師, 企業客戶
- tone_of_voice: 嚴肅高端

## Color Tokens

| Token | Value | Usage |
|---|---|---|
| primary | oklch(55% 0.18 250) | main brand |
| secondary | #112233 | accent |

## Typography
- heading: Noto Serif TC
- body: Noto Sans TC

## Visual Rules
- 不用 emoji 圖標
- 不用紫漸層

## Negative Constraints
- watermark
- fake brand logo
"""


def test_parse_design_memory_minimal() -> None:
    minimal = """## Brand Identity
- brand_name: ACME

## Color Tokens

| Token | Value |
|---|---|
| primary | #ff0000 |
"""
    m = parse_design_memory(minimal)
    assert m.brand_name == "ACME"
    assert m.color_tokens == {"primary": "#ff0000"}


def test_parse_design_memory_three_column_table() -> None:
    # 對應 SDD §4.3 三欄 table（regex fix 驗證）
    m = parse_design_memory(SAMPLE_MD)
    assert m.brand_name == "ACME Corp"
    assert m.industry == "legal"
    assert m.audience == ["律師", "企業客戶"]
    assert m.color_tokens["primary"] == "oklch(55% 0.18 250)"
    assert m.color_tokens["secondary"] == "#112233"
    assert m.typography == {"heading": "Noto Serif TC", "body": "Noto Sans TC"}
    assert "watermark" in m.negative_constraints


def test_validate_design_memory_requires_brand_name() -> None:
    empty = DesignMemory()
    warnings = validate_design_memory(empty)
    assert any("brand_name" in w for w in warnings)
    # 有 brand_name 後應通過
    filled = DesignMemory(brand_name="ACME")
    assert validate_design_memory(filled) == []


def test_save_design_memory_roundtrip(tmp_path: Path) -> None:
    original = parse_design_memory(SAMPLE_MD)
    out_path = save_design_memory(tmp_path, original)
    assert out_path.exists()
    assert out_path.name == DESIGN_FILENAME
    reloaded = load_design_memory(tmp_path)
    assert reloaded is not None
    assert reloaded.brand_name == original.brand_name
    assert reloaded.color_tokens == original.color_tokens
    assert reloaded.audience == original.audience
    assert reloaded.negative_constraints == original.negative_constraints


def test_load_design_memory_missing(tmp_path: Path) -> None:
    # 沒檔案時回 None，不 crash
    assert load_design_memory(tmp_path) is None


def test_build_system_prompt_injects_negative_constraints() -> None:
    memory = parse_design_memory(SAMPLE_MD)
    base = "BASE INSTRUCTIONS"
    sp = build_system_prompt(base, memory)
    assert "watermark" in sp
    assert "fake brand logo" in sp
    assert "ACME Corp" in sp
    assert base in sp
    # None memory 應回原 base
    assert build_system_prompt(base, None) == base


def test_apply_design_memory_to_prompt() -> None:
    memory = parse_design_memory(SAMPLE_MD)
    prompt = "draw a logo"
    out = apply_design_memory_to_prompt(prompt, memory)
    assert "draw a logo" in out
    assert "ACME Corp" in out
    # None 應原 prompt
    assert apply_design_memory_to_prompt(prompt, None) == prompt


def test_memory_to_markdown_roundtrip_idempotent() -> None:
    m = parse_design_memory(SAMPLE_MD)
    md1 = memory_to_markdown(m)
    m2 = parse_design_memory(md1)
    md2 = memory_to_markdown(m2)
    # 兩次序列化結果應一致（idempotent）
    assert md1 == md2


def test_parse_handles_empty_and_garbage() -> None:
    assert parse_design_memory("").brand_name == ""
    assert parse_design_memory("nonsense\n--\n***").brand_name == ""
