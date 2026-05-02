"""Mask uploader（PNG alpha 驗證）。

對應 SDD-v2.5 §4.1 mask 可選 PNG alpha、PLAN-sprint-2.md §3.2。
"""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def validate_png_alpha(path: Path) -> tuple[bool, str]:
    """驗證 mask 是否為 PNG 且含 alpha channel。回 (ok, message)。

    使用 QImage 不引入 Pillow 依賴。
    """
    if not path.exists():
        return False, "檔案不存在"
    if path.suffix.lower() != ".png":
        return False, "mask 必須是 .png 副檔名"
    image = QImage(str(path))
    if image.isNull():
        return False, "mask 無法讀取，可能格式損壞"
    if not image.hasAlphaChannel():
        return False, "mask 必須含 alpha channel（透明區為要重繪的區域）"
    return True, ""


class MaskUploader(QWidget):
    """選填 mask 上傳；emit None 代表清除、emit Path 代表新 mask。"""

    mask_changed = pyqtSignal(object)  # Optional[Path]

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._mask_path: Path | None = None
        self._label = QLabel("Mask（選填，PNG alpha；透明 = 要重繪）", self)
        self._label.setStyleSheet("color: #cbd5e1; font-size: 12px;")
        self._status = QLabel("尚未選擇 mask", self)
        self._status.setStyleSheet("color: #94a3b8; font-size: 11px;")
        self._upload_btn = QPushButton("上傳 mask", self)
        self._clear_btn = QPushButton("清除", self)
        self._upload_btn.clicked.connect(self._open_file_dialog)
        self._clear_btn.clicked.connect(self.clear_mask)
        self._build_ui()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.addWidget(self._label)
        row = QHBoxLayout()
        row.addWidget(self._status, 1)
        row.addWidget(self._upload_btn)
        row.addWidget(self._clear_btn)
        outer.addLayout(row)

    # ── public API ──────────────────────────────────────
    def mask_path(self) -> Path | None:
        return self._mask_path

    def set_mask(self, path: Path) -> None:
        ok, msg = validate_png_alpha(path)
        if not ok:
            # invalid 時清舊 mask 避免 stale state 被 submit
            had_path = self._mask_path is not None
            self._mask_path = None
            self._status.setText(f"⚠️ {msg}")
            self._status.setStyleSheet("color: #f87171; font-size: 11px;")
            if had_path:
                self.mask_changed.emit(None)
            return
        self._mask_path = path
        self._status.setText(f"已選：{path.name}")
        self._status.setStyleSheet("color: #34d399; font-size: 11px;")
        self.mask_changed.emit(path)

    def clear_mask(self) -> None:
        self._mask_path = None
        self._status.setText("尚未選擇 mask")
        self._status.setStyleSheet("color: #94a3b8; font-size: 11px;")
        self.mask_changed.emit(None)

    def _open_file_dialog(self) -> None:
        file, _ = QFileDialog.getOpenFileName(
            self, "選擇 PNG alpha mask", "", "PNG (*.png)"
        )
        if file:
            self.set_mask(Path(file))
