"""Sprint 2A QualityDial 與 cost helpers。

對應 PLAN-sprint-2.md §2.5。
"""

from __future__ import annotations

import pytest

from app.widgets.quality_dial import (
    QUALITY_OPTIONS,
    QualityDial,
    estimate_image_cost,
    suggest_quality,
)


def test_quality_options_three_levels() -> None:
    keys = [opt.key for opt in QUALITY_OPTIONS]
    assert keys == ["low", "medium", "high"]


def test_estimate_image_cost() -> None:
    assert estimate_image_cost(1, "low") == 0.005
    assert estimate_image_cost(3, "medium") == 0.12
    assert estimate_image_cost(2, "high") == 0.34
    assert estimate_image_cost(0, "low") == 0.0


def test_estimate_image_cost_unknown() -> None:
    with pytest.raises(ValueError):
        estimate_image_cost(1, "ultra")


def test_suggest_quality_for_zh_poster() -> None:
    q, msg = suggest_quality("繁體中文活動海報，標題需清晰", "medium")
    assert q == "high"
    assert "建議" in msg


def test_suggest_quality_keeps_when_already_high() -> None:
    q, msg = suggest_quality("中文 poster", "high")
    assert q == "high"
    assert msg == ""


def test_suggest_quality_no_change_for_neutral_prompt() -> None:
    q, msg = suggest_quality("a cat in a yard", "medium")
    assert q == "medium"
    assert msg == ""


def test_quality_dial_defaults_to_medium(qtbot) -> None:
    widget = QualityDial()
    qtbot.addWidget(widget)
    assert widget.quality() == "medium"


def test_quality_dial_set_quality_and_cost(qtbot) -> None:
    widget = QualityDial()
    qtbot.addWidget(widget)
    widget.set_image_count(4)
    widget.set_quality("high")
    assert widget.quality() == "high"
    # 4 × $0.17 = $0.68
    assert estimate_image_cost(4, "high") == 0.68
