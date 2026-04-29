"""Forma Studio v2.5 桌面版主視窗。

PLAN-sprint-2.md §2.2。
4 個 tab：Prompt Gallery / Image Generate / Brand Memory / Settings
+ ApiKeyBar（頂部）+ QualityDial（image tab 下方）
"""

from __future__ import annotations

import json
from pathlib import Path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app.api import key_store
from app.api.openai_client import OpenAIClient
from app.pages.brand_settings_tab import BrandSettingsTab
from app.utils.design_memory import DesignMemory
from app.widgets.image_edit_panel import ImageEditPanel


class ApiKeyBar(QWidget):
    key_changed = pyqtSignal(str)
    key_cleared = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.key_input = QLineEdit(self)
        self.save_button = QPushButton("儲存 Key", self)
        self.clear_button = QPushButton("清除", self)
        self.status_label = QLabel("API Key：未設定", self)
        self._build_ui()
        self._connect_signals()
        self.refresh_status()

    def _build_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_input.setPlaceholderText("sk-...（存入系統鑰匙圈，不寫檔）")
        layout.addWidget(self.status_label)
        layout.addWidget(self.key_input, 1)
        layout.addWidget(self.save_button)
        layout.addWidget(self.clear_button)

    def _connect_signals(self) -> None:
        self.save_button.clicked.connect(self.save_key)
        self.clear_button.clicked.connect(self.clear_key)

    def refresh_status(self) -> None:
        key = key_store.get_key()
        self.status_label.setText("API Key：已設定" if key else "API Key：未設定")

    def save_key(self) -> None:
        key = self.key_input.text().strip()
        if not key:
            QMessageBox.warning(self, "API Key", "請輸入 API Key")
            return
        key_store.set_key(key)
        self.key_input.clear()
        self.refresh_status()
        self.key_changed.emit(key)

    def clear_key(self) -> None:
        key_store.clear_key()
        self.refresh_status()
        self.key_cleared.emit()


class PlaceholderTab(QWidget):
    """Sprint 2A 的暫時 tab；2B/2C 會逐步替換。"""

    def __init__(
        self, title: str, body: str, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        heading = QLabel(title, self)
        heading.setObjectName("PageHeading")
        note = QLabel(body, self)
        note.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(note)
        layout.addStretch(1)


def _read_gallery_index(project_root: Path) -> dict | None:
    """讀 web/prompt-library/gallery-index.json；找不到回 None。"""
    idx_path = project_root / "web" / "prompt-library" / "gallery-index.json"
    if not idx_path.exists():
        return None
    try:
        return json.loads(idx_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


class MainWindow(QMainWindow):
    prompt_selected = pyqtSignal(str)
    api_key_changed = pyqtSignal(str)

    def __init__(
        self, project_root: Path, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.project_root = project_root
        self.api_key_bar = ApiKeyBar(self)
        self.tabs = QTabWidget(self)
        self.image_edit_panel: ImageEditPanel | None = None
        self.brand_settings_tab: BrandSettingsTab | None = None
        self._build_ui()
        self._connect_signals()
        self._apply_theme()
        self.statusBar().showMessage("Ready")

    def _build_ui(self) -> None:
        self.setWindowTitle("Forma Studio v2.5")
        root = QWidget(self)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.api_key_bar)
        layout.addWidget(self.tabs, 1)
        self.setCentralWidget(root)
        self.setStatusBar(QStatusBar(self))
        self._init_tabs()

    def _init_tabs(self) -> None:
        self.tabs.addTab(self._build_gallery_tab(), "Prompt Gallery")
        self.tabs.addTab(self._build_image_tab(), "圖像生成 / 修改")
        self.tabs.addTab(self._build_brand_tab(), "品牌記憶")
        self.tabs.addTab(self._build_settings_tab(), "設定")

    def _build_gallery_tab(self) -> QWidget:
        idx = _read_gallery_index(self.project_root)
        if idx:
            total = idx.get("total_count", 0)
            cats = len(idx.get("categories", []))
            sources = idx.get("sources", [])
            src_text = "、".join(
                f"{s.get('repo','?')} ({s.get('count','?')} 條)" for s in sources
            ) or "（無 sources 欄位）"
            body = (
                f"已載入 {total} 條 prompt、{cats} 個類別。\n"
                f"來源：{src_text}\n\n"
                "Sprint 2B 後可從這裡選 prompt 套用到圖像 tab。"
            )
        else:
            body = (
                "找不到 web/prompt-library/gallery-index.json。\n"
                "請確認 repo 結構或執行 tools/build_gallery.py。"
            )
        return PlaceholderTab("Prompt Gallery", body, self)

    def _build_image_tab(self) -> QWidget:
        # Sprint 2B：ImageEditPanel 取代之前的 placeholder
        self.image_edit_panel = ImageEditPanel(
            client_factory=self._create_openai_client, parent=self
        )
        self.image_edit_panel.image_generated.connect(self._on_image_generated)
        self.image_edit_panel.error_raised.connect(self._on_image_error)
        return self.image_edit_panel

    def _build_brand_tab(self) -> QWidget:
        # Sprint 2C：BrandSettingsTab 取代 placeholder
        self.brand_settings_tab = BrandSettingsTab(
            project_root=self.project_root, parent=self
        )
        # 注意：先 connect 再 load_from_project，否則啟動時的 emit 不會傳到 ImageEditPanel
        self.brand_settings_tab.memory_changed.connect(self._on_memory_changed)
        self.brand_settings_tab.load_from_project(self.project_root)
        return self.brand_settings_tab

    def _build_settings_tab(self) -> QWidget:
        return PlaceholderTab(
            "Settings",
            "API Key 使用 keyring；service=Forma Studio，account=openai_api_key。\n"
            "v2.5 桌面版規範請見 CLAUDE.md。",
            self,
        )

    def _connect_signals(self) -> None:
        self.api_key_bar.key_changed.connect(self._on_api_key_changed)
        self.api_key_bar.key_cleared.connect(self._on_api_key_cleared)
        # quality_changed signal 由 ImageEditPanel 內部 QualityDial 處理

    def _apply_theme(self) -> None:
        # 對齊 web 版深色主題（slate-900 系）
        self.setStyleSheet(
            """
            QMainWindow { background: #101418; color: #eef2f6; }
            QWidget { font-size: 14px; color: #eef2f6; }
            QTabWidget::pane { border: 1px solid #26313a; }
            QTabBar::tab {
                padding: 10px 14px;
                background: #1a2129;
                color: #cbd5e1;
                border: 1px solid #26313a;
            }
            QTabBar::tab:selected { background: #facc15; color: #0f172a; }
            QLineEdit, QTextEdit {
                background: #151b22;
                color: #eef2f6;
                border: 1px solid #2c3945;
                padding: 6px;
            }
            QPushButton {
                padding: 8px 12px;
                border: 1px solid #3a4754;
                background: #202a33;
                color: #eef2f6;
            }
            QPushButton:hover { background: #2a3744; }
            QGroupBox { border: 1px solid #2c3945; margin-top: 12px; padding-top: 12px; }
            QGroupBox::title { color: #facc15; }
            """
        )

    def _on_api_key_changed(self, key: str) -> None:
        self.api_key_changed.emit(key)
        self.statusBar().showMessage("API Key 已更新", 3000)

    def _on_api_key_cleared(self) -> None:
        self.statusBar().showMessage("API Key 已清除", 3000)

    def _create_openai_client(self) -> OpenAIClient:
        # Sprint 2B：image_edit_panel 透過此 factory 取得 client
        # 每次呼叫產一個新 client（含獨立 httpx.AsyncClient），完成後 close
        key = key_store.get_key()
        if not key:
            raise RuntimeError("請先設定 API Key（鑰匙圈）")
        return OpenAIClient(key)

    def _on_image_generated(self, data: bytes) -> None:
        self.statusBar().showMessage(f"圖像就緒：{len(data)} bytes（session cache）", 5000)

    def _on_image_error(self, message: str) -> None:
        self.statusBar().showMessage(f"⚠️ {message}", 5000)

    def _on_memory_changed(self, memory: DesignMemory | None) -> None:
        # 把 DESIGN.md 記憶傳給 ImageEditPanel；None 代表清空
        if self.image_edit_panel is not None:
            self.image_edit_panel.set_design_memory(memory)
        if memory is None:
            self.statusBar().showMessage("DESIGN.md 已清除", 3000)
        else:
            brand = memory.brand_name or "(unnamed)"
            self.statusBar().showMessage(f"DESIGN.md 已套用：{brand}", 3000)
