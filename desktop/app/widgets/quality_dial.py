"""Quality 預算撥盤 widget。

對應 SDD-v2.5 §4.2、PLAN-sprint-1.5 §4.2 cost 表格。
PLAN-sprint-2.md §2.5。
"""

from __future__ import annotations

from dataclasses import dataclass

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QButtonGroup, QGroupBox, QLabel, QRadioButton, QVBoxLayout


@dataclass(frozen=True)
class QualityOption:
    key: str
    label: str
    usd_per_image: float
    description: str


QUALITY_OPTIONS: list[QualityOption] = [
    QualityOption("low", "草稿 low", 0.005, "快速構圖與方向測試"),
    QualityOption("medium", "探索 medium", 0.04, "一般 prompt 測試與方向比較"),
    QualityOption("high", "交付 high", 0.17, "中文文字、海報、資訊圖與客戶交付圖"),
]

# 偵測到 prompt 含這些字串時自動建議升級到 high
HIGH_QUALITY_TRIGGERS = [
    "中文", "繁體", "海報", "poster", "infographic",
    "資訊圖", "報表", "圖表", "文字清晰", "可讀文字",
]


def estimate_image_cost(n: int, quality: str) -> float:
    unit = {item.key: item.usd_per_image for item in QUALITY_OPTIONS}.get(quality)
    if unit is None:
        raise ValueError(f"unknown quality key: {quality}")
    return round(max(0, n) * unit, 3)


def suggest_quality(prompt: str, current: str) -> tuple[str, str]:
    """若 prompt 含 HIGH_QUALITY_TRIGGERS 且當前不是 high，回 (high, 訊息)；否則 (current, '')。"""
    text = (prompt or "").lower()
    if current != "high" and any(token.lower() in text for token in HIGH_QUALITY_TRIGGERS):
        return "high", "偵測到中文文字、海報或資訊圖需求，建議改用交付 high。"
    return current, ""


class QualityDial(QGroupBox):
    quality_changed = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__("Quality / 成本", parent)
        self._buttons: dict[str, QRadioButton] = {}
        self._group = QButtonGroup(self)
        self._cost_label = QLabel(self)
        self._image_count = 1
        self._build_ui()
        self.set_quality("medium")

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        for option in QUALITY_OPTIONS:
            button = QRadioButton(
                f"{option.label} · ${option.usd_per_image:.3f}/張", self
            )
            button.setToolTip(option.description)
            self._buttons[option.key] = button
            self._group.addButton(button)
            layout.addWidget(button)
            button.toggled.connect(
                lambda checked, key=option.key: self._on_toggled(key, checked)
            )
        layout.addWidget(self._cost_label)

    def _on_toggled(self, key: str, checked: bool) -> None:
        if checked:
            self._update_cost_label()
            self.quality_changed.emit(key)

    def quality(self) -> str:
        for key, button in self._buttons.items():
            if button.isChecked():
                return key
        return "medium"

    def set_quality(self, quality: str) -> None:
        if quality not in self._buttons:
            raise ValueError(f"unknown quality: {quality}")
        self._buttons[quality].setChecked(True)
        self._update_cost_label()

    def set_image_count(self, count: int) -> None:
        self._image_count = max(1, count)
        self._update_cost_label()

    def _update_cost_label(self) -> None:
        quality = self.quality()
        total = estimate_image_cost(self._image_count, quality)
        self._cost_label.setText(
            f"Estimated cost: {self._image_count} × {quality} = ${total:.3f}"
        )
