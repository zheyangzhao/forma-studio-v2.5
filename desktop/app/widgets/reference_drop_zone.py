"""Reference Image drag-drop widget（最多 4 張，PNG/JPEG/WebP）。

對應 SDD-v2.5 §4.1 多參考圖、PLAN-sprint-2.md §3.1。
"""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPixmap
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

MAX_IMAGES = 4
ACCEPTED_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
ACCEPTED_FILTER = "Images (*.png *.jpg *.jpeg *.webp)"


def _is_accepted(path: Path) -> bool:
    return path.suffix.lower() in ACCEPTED_SUFFIXES and path.exists()


class _ImageSlot(QFrame):
    """單一參考圖縮圖位。空時顯示 'drop #N'，有圖時顯示縮圖 + 移除鈕。"""

    cleared = pyqtSignal(int)

    def __init__(self, index: int, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._index = index
        self._path: Path | None = None
        self.setObjectName("ImageSlot")
        self.setFixedSize(140, 140)
        self.setFrameShape(QFrame.Shape.StyledPanel)

        self._thumb = QLabel(f"drop #{index + 1}", self)
        self._thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._thumb.setWordWrap(True)
        self._thumb.setStyleSheet("color: #94a3b8;")

        self._clear_btn = QPushButton("✕", self)
        self._clear_btn.setFixedSize(20, 20)
        self._clear_btn.setVisible(False)
        self._clear_btn.clicked.connect(lambda: self.cleared.emit(self._index))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.addWidget(self._clear_btn, 0, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self._thumb, 1)

    def set_image(self, path: Path) -> None:
        self._path = path
        pix = QPixmap(str(path))
        if pix.isNull():
            self._thumb.setText(path.name)
        else:
            self._thumb.setPixmap(
                pix.scaled(
                    120,
                    100,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        self._clear_btn.setVisible(True)

    def clear_image(self) -> None:
        self._path = None
        self._thumb.clear()
        self._thumb.setText(f"drop #{self._index + 1}")
        self._clear_btn.setVisible(False)


class ReferenceDropZone(QWidget):
    """最多 4 張 reference image，drag-drop 或點擊新增。"""

    images_changed = pyqtSignal(list)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._paths: list[Path] = []
        self._slots: list[_ImageSlot] = []
        self._status = QLabel("Reference Images（最多 4 張，可拖放或點擊新增）", self)
        self._status.setStyleSheet("color: #cbd5e1; font-size: 12px;")
        self._add_btn = QPushButton("+ 加入圖片", self)
        self._add_btn.clicked.connect(self._open_file_dialog)
        self._build_ui()
        self.setAcceptDrops(True)

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.addWidget(self._status)

        slot_row = QHBoxLayout()
        for i in range(MAX_IMAGES):
            slot = _ImageSlot(i, self)
            slot.cleared.connect(self._on_slot_cleared)
            slot_row.addWidget(slot)
            self._slots.append(slot)
        outer.addLayout(slot_row)

        outer.addWidget(self._add_btn)

    # ── public API ──────────────────────────────────────
    def image_paths(self) -> list[Path]:
        return list(self._paths)

    def add_paths(self, paths: list[Path]) -> None:
        added = 0
        for p in paths:
            if len(self._paths) >= MAX_IMAGES:
                self._status.setText(
                    f"已達 {MAX_IMAGES} 張上限，多餘已忽略"
                )
                break
            p = Path(p)
            if not _is_accepted(p):
                self._status.setText(f"略過：{p.name}（非 PNG/JPEG/WebP 或不存在）")
                continue
            if p in self._paths:
                continue
            self._paths.append(p)
            added += 1
        self._refresh_slots()
        if added:
            self.images_changed.emit(self.image_paths())

    def clear(self) -> None:
        self._paths.clear()
        self._refresh_slots()
        self.images_changed.emit([])

    def _refresh_slots(self) -> None:
        for i, slot in enumerate(self._slots):
            if i < len(self._paths):
                slot.set_image(self._paths[i])
            else:
                slot.clear_image()

    def _on_slot_cleared(self, index: int) -> None:
        if 0 <= index < len(self._paths):
            self._paths.pop(index)
            self._refresh_slots()
            self.images_changed.emit(self.image_paths())

    def _open_file_dialog(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self, "選擇 Reference Images", "", ACCEPTED_FILTER
        )
        if files:
            self.add_paths([Path(f) for f in files])

    # ── drag-drop ───────────────────────────────────────
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        urls = event.mimeData().urls()
        paths = [Path(u.toLocalFile()) for u in urls if u.isLocalFile()]
        if paths:
            self.add_paths(paths)
            event.acceptProposedAction()
