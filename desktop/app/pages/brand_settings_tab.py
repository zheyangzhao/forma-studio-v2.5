"""DESIGN.md 編輯 GUI（品牌記憶 tab）。

PLAN-sprint-2.md §4.2。
"""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.utils.design_memory import (
    DESIGN_FILENAME,
    DesignMemory,
    load_design_memory,
    save_design_memory,
    validate_design_memory,
)


def _list_to_text(items: list[str]) -> str:
    return "\n".join(items)


def _text_to_list(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def _kv_to_text(items: dict[str, str]) -> str:
    return "\n".join(f"{k}: {v}" for k, v in items.items())


def _text_to_kv(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip()
    return out


class BrandSettingsTab(QWidget):
    memory_changed = pyqtSignal(object)  # DesignMemory | None

    def __init__(
        self, project_root: Path, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.project_root = project_root
        self._project_dir: Path = project_root
        # 基本欄位
        self.project_name_edit = QLineEdit(self)
        self.brand_name_edit = QLineEdit(self)
        self.industry_edit = QLineEdit(self)
        self.audience_edit = QLineEdit(self)
        self.audience_edit.setPlaceholderText("以 , 分隔，例如：律師, 企業客戶")
        self.tone_edit = QLineEdit(self)
        # 多行欄位
        self.typography_edit = QPlainTextEdit(self)
        self.typography_edit.setPlaceholderText(
            "key: value，每行一筆\n例如：\nheading: Noto Serif TC\nbody: Noto Sans TC"
        )
        self.visual_rules_edit = QPlainTextEdit(self)
        self.visual_rules_edit.setPlaceholderText("每行一條 visual rule")
        self.prompt_defaults_edit = QPlainTextEdit(self)
        self.prompt_defaults_edit.setPlaceholderText(
            "key: value，每行一筆\n例如：\nsize: portrait\nquality: high"
        )
        self.negative_edit = QPlainTextEdit(self)
        self.negative_edit.setPlaceholderText("每行一條 negative constraint")
        # v3.0 新增 4 個 optional 欄位（PLAN-sprint-3 §2.5）
        self.spacing_table = QTableWidget(0, 2, self)
        self.spacing_table.setHorizontalHeaderLabels(["token", "value"])
        self.spacing_table.horizontalHeader().setStretchLastSection(True)
        self.spacing_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.add_spacing_btn = QPushButton("+ 加 spacing", self)
        self.del_spacing_btn = QPushButton("− 移除選中", self)
        self.components_edit = QPlainTextEdit(self)
        self.components_edit.setPlaceholderText(
            "每行一條 component spec\n例如：\nButton: 8px radius, icon-only when symbol is familiar"
        )
        self.motion_edit = QPlainTextEdit(self)
        self.motion_edit.setPlaceholderText(
            "key: value，每行一筆\n例如：\nduration_fast: 120ms\neasing_standard: cubic-bezier(0.2, 0, 0, 1)"
        )
        self.voice_edit = QPlainTextEdit(self)
        self.voice_edit.setPlaceholderText("每行一條 voice signal")
        # color tokens table
        self.color_table = QTableWidget(0, 2, self)
        self.color_table.setHorizontalHeaderLabels(["token", "value"])
        self.color_table.horizontalHeader().setStretchLastSection(True)
        self.color_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        # buttons
        self.add_color_btn = QPushButton("+ 加色票", self)
        self.del_color_btn = QPushButton("− 移除選中", self)
        self.dir_label = QLabel(str(self._project_dir), self)
        self.choose_dir_btn = QPushButton("選擇專案目錄", self)
        self.load_btn = QPushButton("載入 DESIGN.md", self)
        self.save_btn = QPushButton("儲存 DESIGN.md", self)
        self.status_label = QLabel("尚未載入", self)
        self.status_label.setStyleSheet("color: #94a3b8;")

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        # 用 QScrollArea 包外層，避免 v3 4 個新區塊撐爆視窗（Codex review Major fix）
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        inner = QWidget(self)
        scroll.setWidget(inner)
        root_layout.addWidget(scroll)
        outer = QVBoxLayout(inner)

        # 專案目錄選擇
        dir_row = QHBoxLayout()
        dir_row.addWidget(QLabel("專案目錄："))
        dir_row.addWidget(self.dir_label, 1)
        dir_row.addWidget(self.choose_dir_btn)
        dir_row.addWidget(self.load_btn)
        outer.addLayout(dir_row)

        # 基本欄位 form
        form = QFormLayout()
        form.addRow("Project name", self.project_name_edit)
        form.addRow("Brand name *", self.brand_name_edit)
        form.addRow("Industry", self.industry_edit)
        form.addRow("Audience", self.audience_edit)
        form.addRow("Tone of voice", self.tone_edit)
        outer.addLayout(form)

        # color table
        color_label = QLabel("Color Tokens（oklch / HEX）", self)
        color_label.setStyleSheet("color: #facc15; font-weight: bold;")
        outer.addWidget(color_label)
        outer.addWidget(self.color_table)
        color_btn_row = QHBoxLayout()
        color_btn_row.addWidget(self.add_color_btn)
        color_btn_row.addWidget(self.del_color_btn)
        color_btn_row.addStretch(1)
        outer.addLayout(color_btn_row)

        # 三個 multiline 區塊
        outer.addWidget(QLabel("Typography（key: value）"))
        outer.addWidget(self.typography_edit)
        outer.addWidget(QLabel("Visual Rules（每行一條）"))
        outer.addWidget(self.visual_rules_edit)
        outer.addWidget(QLabel("Prompt Defaults（key: value）"))
        outer.addWidget(self.prompt_defaults_edit)
        outer.addWidget(QLabel("Negative Constraints（每行一條）"))
        outer.addWidget(self.negative_edit)

        # v3.0 optional sections：用 QGroupBox 視覺分隔，不撐高 widget tree
        # （collapsible 在 PyQt6 沒原生 widget；以 GroupBox + ScrollArea 折衷）
        v3_label = QLabel("── v3.0 Optional Sections（不填可省略）──", self)
        v3_label.setStyleSheet("color: #facc15; font-weight: bold; margin-top: 8px;")
        outer.addWidget(v3_label)

        spacing_box = QGroupBox("Spacing & Layout", self)
        sb_lay = QVBoxLayout(spacing_box)
        sb_lay.addWidget(self.spacing_table)
        sb_btn = QHBoxLayout()
        sb_btn.addWidget(self.add_spacing_btn)
        sb_btn.addWidget(self.del_spacing_btn)
        sb_btn.addStretch(1)
        sb_lay.addLayout(sb_btn)
        outer.addWidget(spacing_box)

        components_box = QGroupBox("Components（每行一條 spec）", self)
        cb_lay = QVBoxLayout(components_box)
        cb_lay.addWidget(self.components_edit)
        outer.addWidget(components_box)

        motion_box = QGroupBox("Motion（key: value）", self)
        mb_lay = QVBoxLayout(motion_box)
        mb_lay.addWidget(self.motion_edit)
        outer.addWidget(motion_box)

        voice_box = QGroupBox("Voice & Copy（每行一條）", self)
        vb_lay = QVBoxLayout(voice_box)
        vb_lay.addWidget(self.voice_edit)
        outer.addWidget(voice_box)

        # save row
        save_row = QHBoxLayout()
        save_row.addWidget(self.status_label, 1)
        save_row.addWidget(self.save_btn)
        outer.addLayout(save_row)

    def _connect_signals(self) -> None:
        self.choose_dir_btn.clicked.connect(self._choose_dir)
        self.load_btn.clicked.connect(self._on_load_clicked)
        self.save_btn.clicked.connect(self.save_to_project)
        self.add_color_btn.clicked.connect(self._add_color_row)
        self.del_color_btn.clicked.connect(self._del_color_row)
        # v3.0 spacing
        self.add_spacing_btn.clicked.connect(self._add_spacing_row)
        self.del_spacing_btn.clicked.connect(self._del_spacing_row)

    # ── public API ──────────────────────────────────────
    def load_from_project(self, project_dir: Path) -> None:
        self._project_dir = project_dir
        self.dir_label.setText(str(project_dir))
        memory = load_design_memory(project_dir)
        if memory is None:
            self.status_label.setText(f"{DESIGN_FILENAME} 不存在，可填寫後儲存建立")
            self.status_label.setStyleSheet("color: #94a3b8;")
            self.set_memory(DesignMemory())
            self.memory_changed.emit(None)
        else:
            self.set_memory(memory)
            self.status_label.setText(f"已載入 {DESIGN_FILENAME}")
            self.status_label.setStyleSheet("color: #34d399;")
            self.memory_changed.emit(memory)

    def save_to_project(self) -> None:
        memory = self.current_memory()
        warnings = validate_design_memory(memory)
        if warnings:
            QMessageBox.warning(
                self, "DESIGN.md 驗證", "\n".join(f"- {w}" for w in warnings)
            )
            # 仍允許儲存，只警告
        try:
            path = save_design_memory(self._project_dir, memory)
        except OSError as exc:
            self.status_label.setText(f"⚠️ 寫入失敗：{exc}")
            self.status_label.setStyleSheet("color: #f87171;")
            QMessageBox.warning(
                self,
                "DESIGN.md 寫入失敗",
                f"無法寫入 {self._project_dir}：{exc}\n\n"
                "請檢查目錄寫入權限或選擇其他路徑。",
            )
            return
        self.status_label.setText(f"已寫入：{path}")
        self.status_label.setStyleSheet("color: #34d399;")
        self.memory_changed.emit(memory)

    def current_memory(self) -> DesignMemory:
        memory = DesignMemory()
        memory.project_name = self.project_name_edit.text().strip()
        memory.brand_name = self.brand_name_edit.text().strip()
        memory.industry = self.industry_edit.text().strip()
        memory.audience = [
            a.strip()
            for a in self.audience_edit.text().split(",")
            if a.strip()
        ]
        memory.tone_of_voice = self.tone_edit.text().strip()
        memory.color_tokens = self._color_table_to_dict()
        memory.typography = _text_to_kv(self.typography_edit.toPlainText())
        memory.visual_rules = _text_to_list(
            self.visual_rules_edit.toPlainText()
        )
        memory.prompt_defaults = _text_to_kv(
            self.prompt_defaults_edit.toPlainText()
        )
        memory.negative_constraints = _text_to_list(
            self.negative_edit.toPlainText()
        )
        # v3.0 optional 欄位
        memory.spacing_tokens = self._spacing_table_to_dict()
        memory.components = _text_to_list(self.components_edit.toPlainText())
        memory.motion = _text_to_kv(self.motion_edit.toPlainText())
        memory.voice_signals = _text_to_list(self.voice_edit.toPlainText())
        return memory

    def set_memory(self, memory: DesignMemory) -> None:
        self.project_name_edit.setText(memory.project_name)
        self.brand_name_edit.setText(memory.brand_name)
        self.industry_edit.setText(memory.industry)
        self.audience_edit.setText(", ".join(memory.audience))
        self.tone_edit.setText(memory.tone_of_voice)
        self.typography_edit.setPlainText(_kv_to_text(memory.typography))
        self.visual_rules_edit.setPlainText(_list_to_text(memory.visual_rules))
        self.prompt_defaults_edit.setPlainText(
            _kv_to_text(memory.prompt_defaults)
        )
        self.negative_edit.setPlainText(
            _list_to_text(memory.negative_constraints)
        )
        self._dict_to_color_table(memory.color_tokens)
        # v3.0 optional 欄位
        self._dict_to_spacing_table(memory.spacing_tokens)
        self.components_edit.setPlainText(_list_to_text(memory.components))
        self.motion_edit.setPlainText(_kv_to_text(memory.motion))
        self.voice_edit.setPlainText(_list_to_text(memory.voice_signals))

    # ── helpers ─────────────────────────────────────────
    def _choose_dir(self) -> None:
        chosen = QFileDialog.getExistingDirectory(
            self, "選擇專案目錄", str(self._project_dir)
        )
        if chosen:
            self.load_from_project(Path(chosen))

    def _on_load_clicked(self) -> None:
        self.load_from_project(self._project_dir)

    def _add_color_row(self, token: str = "", value: str = "") -> None:
        row = self.color_table.rowCount()
        self.color_table.insertRow(row)
        self.color_table.setItem(row, 0, QTableWidgetItem(token))
        self.color_table.setItem(row, 1, QTableWidgetItem(value))

    def _del_color_row(self) -> None:
        rows = sorted(
            {idx.row() for idx in self.color_table.selectedIndexes()},
            reverse=True,
        )
        for r in rows:
            self.color_table.removeRow(r)

    def _color_table_to_dict(self) -> dict[str, str]:
        out: dict[str, str] = {}
        for r in range(self.color_table.rowCount()):
            tok_item = self.color_table.item(r, 0)
            val_item = self.color_table.item(r, 1)
            tok = tok_item.text().strip() if tok_item else ""
            val = val_item.text().strip() if val_item else ""
            if tok:
                out[tok] = val
        return out

    def _dict_to_color_table(self, tokens: dict[str, str]) -> None:
        self.color_table.setRowCount(0)
        for tok, val in tokens.items():
            self._add_color_row(tok, val)

    # ── v3.0 spacing table helpers（與 color_table 同模式）──
    def _add_spacing_row(self, token: str = "", value: str = "") -> None:
        row = self.spacing_table.rowCount()
        self.spacing_table.insertRow(row)
        self.spacing_table.setItem(row, 0, QTableWidgetItem(token))
        self.spacing_table.setItem(row, 1, QTableWidgetItem(value))

    def _del_spacing_row(self) -> None:
        rows = sorted(
            {idx.row() for idx in self.spacing_table.selectedIndexes()},
            reverse=True,
        )
        for r in rows:
            self.spacing_table.removeRow(r)

    def _spacing_table_to_dict(self) -> dict[str, str]:
        out: dict[str, str] = {}
        for r in range(self.spacing_table.rowCount()):
            tok_item = self.spacing_table.item(r, 0)
            val_item = self.spacing_table.item(r, 1)
            tok = tok_item.text().strip() if tok_item else ""
            val = val_item.text().strip() if val_item else ""
            if tok:
                out[tok] = val
        return out

    def _dict_to_spacing_table(self, tokens: dict[str, str]) -> None:
        self.spacing_table.setRowCount(0)
        for tok, val in tokens.items():
            self._add_spacing_row(tok, val)
