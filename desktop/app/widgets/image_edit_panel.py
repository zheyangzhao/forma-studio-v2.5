"""ImageEditPanel：整合 prompt + reference + mask + quality + 兩個送出按鈕。

對應 SDD-v2.5 §4.1 按鈕分開、PLAN-sprint-2.md §3.3。

async OpenAI call 用 QThread + Worker 包（PyQt6 標準），
避免 GUI 主執行緒阻塞。
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from pathlib import Path
from typing import Any

from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.api.openai_client import ImageResult, OpenAIClient, OpenAIClientError
from app.widgets.mask_uploader import MaskUploader, validate_png_alpha
from app.widgets.quality_dial import QualityDial
from app.widgets.reference_drop_zone import ReferenceDropZone


class _OpenAIWorker(QObject):
    """跑 async coroutine 的 QThread worker；finished/error 回 GUI thread。"""

    finished = pyqtSignal(object)  # ImageResult
    error = pyqtSignal(str)

    def __init__(self, coro_factory: Callable[[], Any]) -> None:
        super().__init__()
        self._coro_factory = coro_factory

    def run(self) -> None:
        try:
            result = asyncio.run(self._wrap())
        except OpenAIClientError as e:
            self.error.emit(str(e))
            return
        except (ValueError, RuntimeError) as e:
            self.error.emit(str(e))
            return
        except Exception as e:  # 防最後一道：未預期 error 也回 GUI
            self.error.emit(f"未預期錯誤：{e}")
            return
        self.finished.emit(result)

    async def _wrap(self) -> ImageResult:
        client_aware = self._coro_factory()
        # coro_factory 可能回 (client, coro) tuple，方便 finally close
        if isinstance(client_aware, tuple) and len(client_aware) == 2:
            client, coro = client_aware
            try:
                return await coro
            finally:
                await client.close()
        return await client_aware


class ImageEditPanel(QWidget):
    """主面板：generations vs edits 兩個 endpoint 分按鈕。"""

    image_generated = pyqtSignal(bytes)
    error_raised = pyqtSignal(str)

    def __init__(
        self,
        client_factory: Callable[[], OpenAIClient],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._client_factory = client_factory
        self._thread: QThread | None = None
        self._worker: _OpenAIWorker | None = None
        self._last_result: bytes | None = None

        self.prompt_edit = QTextEdit(self)
        self.reference_zone = ReferenceDropZone(self)
        self.mask_uploader = MaskUploader(self)
        self.quality_dial = QualityDial(self)
        self.generate_btn = QPushButton("生成新圖", self)
        self.edit_btn = QPushButton("修改既有圖", self)
        self.status_label = QLabel("Ready", self)

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        prompt_label = QLabel("Prompt", self)
        prompt_label.setStyleSheet("color: #cbd5e1; font-weight: bold;")
        self.prompt_edit.setPlaceholderText(
            "描述你要生成或修改的圖像；中文/海報/infographic 會自動建議升 high。"
        )
        self.prompt_edit.setMinimumHeight(120)
        layout.addWidget(prompt_label)
        layout.addWidget(self.prompt_edit)
        layout.addWidget(self.reference_zone)
        layout.addWidget(self.mask_uploader)
        layout.addWidget(self.quality_dial)

        button_row = QHBoxLayout()
        button_row.addWidget(self.status_label, 1)
        button_row.addWidget(self.generate_btn)
        button_row.addWidget(self.edit_btn)
        layout.addLayout(button_row)

    def _connect_signals(self) -> None:
        self.generate_btn.clicked.connect(self._on_generate_clicked)
        self.edit_btn.clicked.connect(self._on_edit_clicked)

    # ── public API ──────────────────────────────────────
    def set_prompt(self, prompt: str) -> None:
        self.prompt_edit.setPlainText(prompt)

    def prompt(self) -> str:
        return self.prompt_edit.toPlainText().strip()

    def last_result(self) -> bytes | None:
        return self._last_result

    # ── send ────────────────────────────────────────────
    def _on_generate_clicked(self) -> None:
        prompt = self.prompt()
        if not prompt:
            self._show_error("請先輸入 prompt", modal=False)
            return
        quality = self.quality_dial.quality()
        self._dispatch(
            lambda: self._make_generate_task(prompt, quality)
        )

    def _on_edit_clicked(self) -> None:
        prompt = self.prompt()
        if not prompt:
            self._show_error("請先輸入 prompt", modal=False)
            return
        images = self.reference_zone.image_paths()
        if not images:
            self._show_error("修改既有圖需要至少 1 張參考圖", modal=False)
            return
        if len(images) > 4:
            self._show_error("最多 4 張，請移除多餘圖片", modal=False)
            return
        mask = self.mask_uploader.mask_path()
        if mask is not None:
            # submit 前重驗 mask（檔案可能被外部刪/改）
            ok, msg = validate_png_alpha(mask)
            if not ok:
                self._show_error(f"mask 已失效：{msg}", modal=False)
                return
        quality = self.quality_dial.quality()
        self._dispatch(
            lambda: self._make_edit_task(prompt, images, mask, quality)
        )

    def _make_generate_task(self, prompt: str, quality: str) -> tuple:
        client = self._client_factory()
        coro = client.generate_image(prompt, quality=quality)

        async def _take_first() -> ImageResult:
            results = await coro
            if not results:
                raise OpenAIClientError("OpenAI 回傳空結果")
            return results[0]

        return client, _take_first()

    def _make_edit_task(
        self,
        prompt: str,
        images: list[Path],
        mask: Path | None,
        quality: str,
    ) -> tuple:
        client = self._client_factory()
        coro = client.edit_image(prompt, images, mask, quality=quality)
        return client, coro

    def _dispatch(self, coro_factory: Callable[[], Any]) -> None:
        if self._thread is not None and self._thread.isRunning():
            self._show_error("仍在處理上一次請求", modal=False)
            return
        self._set_busy(True)
        self.status_label.setText("處理中...")

        self._thread = QThread(self)
        self._worker = _OpenAIWorker(coro_factory)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.error.connect(self._on_worker_error)
        # 標準 cleanup：worker.finished/error → worker.deleteLater（同步排程）
        # thread.finished → thread.deleteLater（thread event loop 結束時清）
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker.error.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.finished.connect(self._on_thread_finished)
        self._thread.start()

    def _on_worker_finished(self, result: Any) -> None:
        if isinstance(result, ImageResult):
            self._last_result = result.data
            self.status_label.setText(
                f"完成（{len(result.data)} bytes，session cache）"
            )
            self.image_generated.emit(result.data)
        else:
            self.status_label.setText("完成（未解碼）")
        self._set_busy(False)

    def _on_worker_error(self, message: str) -> None:
        self._show_error(message, modal=True)
        self._set_busy(False)

    def _on_thread_finished(self) -> None:
        # deleteLater 會在 thread event loop 結束時排隊；只重置本地引用
        self._worker = None
        self._thread = None

    def _set_busy(self, busy: bool) -> None:
        self.generate_btn.setDisabled(busy)
        self.edit_btn.setDisabled(busy)

    def _show_error(self, message: str, *, modal: bool = True) -> None:
        # validation error 用 modal=False（不彈窗，方便 pytest-qt）
        # API error 用 modal=True
        self.status_label.setText(f"⚠️ {message}")
        self.error_raised.emit(message)
        if modal:
            QMessageBox.warning(self, "Forma Studio", message)

    def closeEvent(self, event: Any) -> None:
        # 視窗關閉時若 worker 仍跑，等最多 2 秒；避免 "Destroyed while running"
        if self._thread is not None and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait(2000)
        super().closeEvent(event)
