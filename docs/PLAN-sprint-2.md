# Forma Studio v2.5 · Sprint 2 實作計劃書

**版本**：v2.5 Sprint 2  
**日期**：2026-04-29  
**工作目錄**：`/Users/jeyengjau/Desktop/APP/forma-studio-v2.5`  
**輸出檔案**：`docs/PLAN-sprint-2.md`  
**基準狀態**：Web 版 Tier 1 + Tier 1.5 已完成，tag `v2.5-sprint-1.5`；桌面版目前只有 `desktop/README.md` placeholder，`desktop/main.py` 尚未建立。  

讀檔紀錄：

| 檔案 | 狀態 | 本 PLAN 採用方式 |
|---|---|---|
| `CLAUDE.md` | 已讀 | keyring service/account、Python 3.12 + PyQt6 + httpx、API Key 不落檔 |
| `docs/SDD-v2.5-integration-upgrade.md` §四 | 已讀 | Sprint 2 主要規格來源，引用 `SDD §4.1` / `§4.2` / `§4.3` |
| `docs/SDD-desktop-v2.0.md` | 本 repo 缺檔 | `desktop/README.md` 指向 frozen repo；Sprint 2A 前置檢查需補回或人工對照 |
| `docs/PLAN-sprint-1.5.md` §七 7.1 | 已讀 | Tier 2 子任務順序與目錄草圖 |
| `web/forma-studio.html` | 已讀 | `ApiCtx`、`EnhanceBtn`、`enhancePromptWithOpenAI()` 移植參考 |
| `web/prompt-library/gallery-index.json` | 已讀 | 116 條 gallery index schema，桌面版讀同份 JSON |
| `HANDOFF.md`, `DEVLOG.md` | 已讀 | Sprint 1.5 最新狀態與 Tier 2 待辦 |

---

## 一、Sprint 2 範圍與分期

### 1.1 為什麼需要 Sprint 2

Sprint 1 + 1.5 已把 Web 單檔版補到可用狀態，但桌面版仍停在規劃階段。Sprint 2 的目標不是複製 Web 4 區塊 glow UI，而是依 `docs/SDD-v2.5-integration-upgrade.md` §四補齊 PyQt6 Tier 2 能力：

| 層 | Sprint 1.5 現況 | Sprint 2 缺口 | Sprint 2 處理 |
|---|---|---|---|
| App 入口 | `desktop/main.py` 不存在 | 桌面版無法啟動 | 2A 建立 PyQt6 bootstrap |
| API Key | Web 只存記憶體 | Desktop 需系統鑰匙圈 | 2A `key_store.py` |
| Image API | Web 主要是 prompt 生成與增強 | Desktop 需 `generations` + `edits` | 2A `openai_client.py`，2B 接 UI |
| Quality 成本 | Web prompt 有 quality 字串 | Desktop 需 low/medium/high 成本撥盤 | 2A `quality_dial.py`，對應 SDD §4.2 |
| Edit endpoint | Gallery 已有 edit showcase | Desktop 無 reference/mask workflow | 2B widgets，對應 SDD §4.1 |
| DESIGN.md | SDD 已定 schema | Desktop 無 parser / GUI / prompt 注入 | 2C，對應 SDD §4.3 |

可執行檢查：

```bash
cd /Users/jeyengjau/Desktop/APP/forma-studio-v2.5
test -f desktop/main.py || echo "desktop/main.py missing: Sprint 2A starts here"
test -f docs/SDD-desktop-v2.0.md || echo "docs/SDD-desktop-v2.0.md missing in this repo"
```

預期 stdout：

```text
desktop/main.py missing: Sprint 2A starts here
docs/SDD-desktop-v2.0.md missing in this repo
```

### 1.2 範圍 vs scope-out

| 優先序 | 項目 | Sprint 2 狀態 | 主要檔案 | 說明 |
|---:|---|---|---|---|
| 1 | PyQt6 app shell | 必做 | `desktop/main.py`, `desktop/app/main_window.py` | 能啟動 4 tab 主視窗 |
| 2 | keyring API Key | 必做 | `desktop/app/api/key_store.py` | service `"Forma Studio"`、account `"openai_api_key"` |
| 3 | OpenAI client | 必做 | `desktop/app/api/openai_client.py` | `generate_image()`、`edit_image()`、`enhance_prompt()` |
| 4 | Quality 成本撥盤 | 必做 | `desktop/app/widgets/quality_dial.py` | low/medium/high 與估價 |
| 5 | Edit endpoint UI | 必做 | `reference_drop_zone.py`, `mask_uploader.py`, `image_edit_panel.py` | 最多 4 張 reference，PNG alpha mask |
| 6 | DESIGN.md 記憶 | 必做 | `design_memory.py`, `brand_settings_tab.py` | parse/validate/save + system prompt 注入 |
| - | Web 版 glow 改版 | Scope out | `web/forma-studio.html` | Sprint 2 不修改 Web |
| - | Comment mode | Scope out | TBD | v3.0 backlog |
| - | 多格式匯出 | Scope out | TBD | v3.0 backlog |
| - | PyInstaller 發佈 | Outline only | `desktop/packaging/**` | Sprint 2D backlog |

Sprint 2 預期改動樹：

```text
forma-studio-v2.5/
└── desktop/
    ├── main.py
    ├── requirements.txt
    ├── app/
    │   ├── __init__.py
    │   ├── main_window.py
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── key_store.py
    │   │   └── openai_client.py
    │   ├── pages/
    │   │   ├── __init__.py
    │   │   └── brand_settings_tab.py
    │   ├── utils/
    │   │   ├── __init__.py
    │   │   ├── design_memory.py
    │   │   └── gallery_loader.py
    │   └── widgets/
    │       ├── __init__.py
    │       ├── quality_dial.py
    │       ├── reference_drop_zone.py
    │       ├── mask_uploader.py
    │       └── image_edit_panel.py
    └── tests/
        ├── test_main_window.py
        ├── test_openai_client.py
        ├── test_quality_dial.py
        ├── test_image_edit_panel.py
        └── test_design_memory.py
```

### 1.3 分期策略（Sprint 2A / 2B / 2C）

| 分期 | 目標 | 建議 session | Gate |
|---|---|---:|---|
| Sprint 2A | 桌面版基礎設施 | 1-1.5 | `python desktop/main.py` 可啟動，pytest-qt smoke test PASS |
| Sprint 2B | edit endpoint UI | 1 | Reference/mask/endpoint 切換可測，multipart body mock PASS |
| Sprint 2C | DESIGN.md 共享記憶 | 1 | parser + GUI + system prompt 注入測試 PASS |
| Sprint 2D | 打包與發佈 | backlog | PyInstaller `.app`、簽名、notarize，不在本 PLAN 實作 |

分期順序不得調換。`image_edit_panel.py` 需要 2A 的 `OpenAIClient` 與 `QualityDial`，`brand_settings_tab.py` 需要 2A 的主視窗 tab 架構。

### 1.4 預估工時與里程碑

| 里程碑 | 範圍 | 預估 | 產出 | 驗收命令 |
|---|---|---:|---|---|
| M1 | 2A app shell | 0.5 天 | `main.py`, `main_window.py` | `python desktop/main.py` |
| M2 | 2A keyring + client | 0.5-1 天 | `key_store.py`, `openai_client.py` | `pytest desktop/tests/test_openai_client.py -q` |
| M3 | 2A quality + smoke | 0.5 天 | `quality_dial.py`, `requirements.txt` | `pytest desktop/tests/test_quality_dial.py -q` |
| M4 | 2B edit UI | 1 天 | drop zone、mask、edit panel | `pytest desktop/tests/test_image_edit_panel.py -q` |
| M5 | 2C DESIGN.md | 1 天 | parser、brand tab、prompt 注入 | `pytest desktop/tests/test_design_memory.py -q` |
| M6 | 收尾 | 0.5 天 | DEVLOG/HANDOFF 更新、tag | `pytest desktop/tests -q` |

---

## 二、Sprint 2A：桌面版基礎設施（必先做）

### 2.1 main.py 入口

檔案：`desktop/main.py`  
預估：10-30 行  
對應：`CLAUDE.md` Desktop 技術棧、`desktop/README.md` 待實作清單。

完整 sample code：

```python
from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from app.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Forma Studio")
    app.setOrganizationName("Forma Studio")

    icon_path = Path(__file__).resolve().parent / "assets" / "forma-studio.icns"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow(project_root=Path(__file__).resolve().parents[1])
    window.resize(1180, 820)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
```

Actionable items：

| 項目 | 指令 / 簽名 | 驗收 |
|---|---|---|
| 建立入口 | `desktop/main.py` | `python desktop/main.py` 不 import error |
| app root | `Path(__file__).resolve().parents[1]` | 可定位 repo root 讀 `web/prompt-library` |
| icon | `desktop/assets/forma-studio.icns` optional | 檔案不存在不 crash |

命令：

```bash
cd /Users/jeyengjau/Desktop/APP/forma-studio-v2.5
python desktop/main.py
```

預期 stdout：

```text
# 無 stdout；顯示 Forma Studio 主視窗
```

### 2.2 主視窗 main_window.py（4 tab + ApiKeyBar）

檔案：`desktop/app/main_window.py`  
預估：200-400 行  
目的：建立可測的主視窗骨架，2B/2C 後續只替換 placeholder，不改 app shell。

Tab 規格：

| Tab | class / widget | Sprint 2A 狀態 | Sprint 2B/2C 接線 |
|---|---|---|---|
| Prompt Gallery | `GalleryTab` placeholder | 讀 `gallery-index.json` 顯示總數 | 後續可選 prompt 注入 image tab |
| Image Generate | `ImageEditPanel` placeholder | 先放 prompt textarea + quality | 2B 替換成完整 edit panel |
| Brand Memory | `BrandSettingsTab` placeholder | 顯示 DESIGN.md 尚未載入 | 2C 替換成 GUI |
| Settings | `SettingsTab` placeholder | API Key 狀態 + runtime info | 2A 完成 keyring |

完整 class 框架：

```python
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTabWidget,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from app.api import key_store
from app.widgets.quality_dial import QualityDial


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
    def __init__(self, title: str, body: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        heading = QLabel(title, self)
        heading.setObjectName("PageHeading")
        note = QLabel(body, self)
        note.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(note)
        layout.addStretch(1)


class MainWindow(QMainWindow):
    prompt_selected = pyqtSignal(str)
    api_key_changed = pyqtSignal(str)

    def __init__(self, project_root: Path, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.project_root = project_root
        self.api_key_bar = ApiKeyBar(self)
        self.tabs = QTabWidget(self)
        self.quality_dial = QualityDial(self)
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
        return PlaceholderTab(
            "Prompt Gallery",
            "Sprint 2A 先讀 web/prompt-library/gallery-index.json；Sprint 2B 後可套用到 prompt。",
            self,
        )

    def _build_image_tab(self) -> QWidget:
        page = QWidget(self)
        layout = QVBoxLayout(page)
        prompt = QTextEdit(page)
        prompt.setPlaceholderText("輸入圖像 prompt；Sprint 2B 會接 ImageEditPanel")
        layout.addWidget(prompt, 1)
        layout.addWidget(self.quality_dial)
        return page

    def _build_brand_tab(self) -> QWidget:
        return PlaceholderTab(
            "DESIGN.md",
            "Sprint 2C 實作 DESIGN.md parse / validate / save 與 system prompt 注入。",
            self,
        )

    def _build_settings_tab(self) -> QWidget:
        return PlaceholderTab(
            "Settings",
            "API Key 使用 keyring；service=Forma Studio，account=openai_api_key。",
            self,
        )

    def _connect_signals(self) -> None:
        self.api_key_bar.key_changed.connect(self._on_api_key_changed)
        self.api_key_bar.key_cleared.connect(self._on_api_key_cleared)
        self.quality_dial.quality_changed.connect(self._on_quality_changed)

    def _apply_theme(self) -> None:
        self.setStyleSheet("""
            QMainWindow { background: #101418; color: #eef2f6; }
            QWidget { font-size: 14px; }
            QTabWidget::pane { border: 1px solid #26313a; }
            QTabBar::tab { padding: 10px 14px; }
            QLineEdit, QTextEdit { background: #151b22; color: #eef2f6; border: 1px solid #2c3945; }
            QPushButton { padding: 8px 12px; border: 1px solid #3a4754; background: #202a33; }
        """)

    def _on_api_key_changed(self, key: str) -> None:
        self.api_key_changed.emit(key)
        self.statusBar().showMessage("API Key 已更新", 3000)

    def _on_api_key_cleared(self) -> None:
        self.statusBar().showMessage("API Key 已清除", 3000)

    def _on_quality_changed(self, quality: str) -> None:
        self.statusBar().showMessage(f"Quality: {quality}", 2000)
```

Signal / slot 清單：

| Signal | 發出者 | Slot | 行為 |
|---|---|---|---|
| `ApiKeyBar.key_changed(str)` | `ApiKeyBar.save_key()` | `MainWindow._on_api_key_changed()` | 更新 status bar，後續更新 client |
| `ApiKeyBar.key_cleared()` | `ApiKeyBar.clear_key()` | `MainWindow._on_api_key_cleared()` | 清除狀態 |
| `QualityDial.quality_changed(str)` | `QualityDial._on_selected()` | `MainWindow._on_quality_changed()` | 顯示目前 quality |
| `MainWindow.prompt_selected(str)` | gallery tab | image tab handler | Sprint 2B 接 prompt 注入 |

驗收：

```bash
pytest desktop/tests/test_main_window.py -q
```

預期 stdout：

```text
1 passed
```

### 2.3 keyring 整合 key_store.py

檔案：`desktop/app/api/key_store.py`  
預估：30-50 行  
對應：`CLAUDE.md` API Key 規範。

完整函數簽名：

```python
from __future__ import annotations

import keyring

SERVICE_NAME = "Forma Studio"
OPENAI_ACCOUNT = "openai_api_key"


def get_key() -> str | None:
    # 對應 CLAUDE.md：桌面版 API Key 存系統鑰匙圈，不寫檔
    value = keyring.get_password(SERVICE_NAME, OPENAI_ACCOUNT)
    return value.strip() if value else None


def set_key(api_key: str) -> None:
    api_key = api_key.strip()
    if not api_key:
        raise ValueError("api_key is empty")
    keyring.set_password(SERVICE_NAME, OPENAI_ACCOUNT, api_key)


def clear_key() -> None:
    try:
        keyring.delete_password(SERVICE_NAME, OPENAI_ACCOUNT)
    except keyring.errors.PasswordDeleteError:
        return
```

Actionable items：

| 項目 | 檢查 |
|---|---|
| 常數 | `SERVICE_NAME == "Forma Studio"`、`OPENAI_ACCOUNT == "openai_api_key"` |
| 空值 | `set_key("")` raises `ValueError` |
| 清除 | key 不存在時 `clear_key()` 不 crash |
| 測試 | 使用 monkeypatch，不碰使用者真實 Keychain |

pytest 範例：

```python
def test_key_store_roundtrip(monkeypatch):
    store = {}
    monkeypatch.setattr(keyring, "get_password", lambda s, a: store.get((s, a)))
    monkeypatch.setattr(keyring, "set_password", lambda s, a, v: store.__setitem__((s, a), v))
    monkeypatch.setattr(keyring, "delete_password", lambda s, a: store.pop((s, a), None))

    set_key(" sk-test ")
    assert get_key() == "sk-test"
    clear_key()
    assert get_key() is None
```

### 2.4 openai_client.py（generations + edits 兩 endpoint）

檔案：`desktop/app/api/openai_client.py`  
預估：80-150 行  
對應：`SDD §4.1 edit endpoint`、`web/forma-studio.html` Tier 1.6 `enhancePromptWithOpenAI()`。

完整 class / method 簽名：

```python
from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx


class OpenAIClientError(RuntimeError):
    pass


@dataclass(frozen=True)
class ImageResult:
    data: bytes
    mime_type: str = "image/png"


class OpenAIClient:
    BASE_URL = "https://api.openai.com/v1"
    IMAGE_MODEL = "gpt-image-2"
    TEXT_MODEL = "gpt-4o-mini"

    def __init__(
        self,
        api_key: str,
        *,
        timeout: float = 120.0,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not api_key.strip():
            raise ValueError("api_key is required")
        self._key = api_key.strip()
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(timeout=timeout)

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._key}"}

    async def generate_image(
        self,
        prompt: str,
        *,
        size: str = "1024x1024",
        quality: str = "medium",
        n: int = 1,
    ) -> list[ImageResult]:
        # 對應 SDD §4.1：generations endpoint 與 edits endpoint 分開
        payload = {
            "model": self.IMAGE_MODEL,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "n": n,
            "response_format": "b64_json",
        }
        resp = await self._client.post(
            f"{self.BASE_URL}/images/generations",
            headers=self._headers(),
            json=payload,
        )
        return self._decode_image_response(resp)

    async def edit_image(
        self,
        prompt: str,
        images: list[Path],
        mask: Path | None = None,
        *,
        size: str = "1024x1024",
        quality: str = "medium",
    ) -> ImageResult:
        # 對應 SDD §4.1 edit endpoint：最多 4 張 reference images，mask 為 PNG alpha
        if not images:
            raise ValueError("edit_image requires at least one reference image")
        if len(images) > 4:
            raise ValueError("edit_image supports at most 4 reference images")

        files: list[tuple[str, tuple[str, bytes, str]]] = []
        for image_path in images:
            files.append(("image[]", (image_path.name, image_path.read_bytes(), _guess_mime(image_path))))
        if mask:
            files.append(("mask", (mask.name, mask.read_bytes(), "image/png")))

        data = {
            "model": self.IMAGE_MODEL,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "response_format": "b64_json",
        }
        resp = await self._client.post(
            f"{self.BASE_URL}/images/edits",
            headers=self._headers(),
            data=data,
            files=files,
        )
        return self._decode_image_response(resp)[0]

    async def enhance_prompt(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float = 0.2,
    ) -> str:
        # 對應 Tier 1.6 enhancePromptWithOpenAI()：移植到 Desktop client
        payload = {
            "model": self.TEXT_MODEL,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system_prompt or ENHANCE_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        }
        resp = await self._client.post(
            f"{self.BASE_URL}/chat/completions",
            headers=self._headers(),
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()

    def _decode_image_response(self, resp: httpx.Response) -> list[ImageResult]:
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise OpenAIClientError(_format_api_error(exc.response)) from exc
        payload = resp.json()
        return [
            ImageResult(data=base64.b64decode(item["b64_json"]))
            for item in payload.get("data", [])
            if item.get("b64_json")
        ]


ENHANCE_SYSTEM_PROMPT = """你是 Forma Studio 的 prompt reviewer。
請把使用者 prompt 改寫成可直接送 GPT Image 2 的高品質 prompt。
保留 source attribution，不新增未提供的具體品牌、人物、日期、法規或產品版本。
"""


def _guess_mime(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".webp":
        return "image/webp"
    return "image/png"


def _format_api_error(resp: httpx.Response) -> str:
    body = resp.text[:300]
    if resp.status_code == 401:
        return "API Key 無效或已過期"
    if resp.status_code == 413:
        return "圖片太大，請縮小到 2048px 內再試"
    return f"OpenAI API error {resp.status_code}: {body}"
```

Mock 測試重點：

| 測試 | 檔案 | Assertion |
|---|---|---|
| generations JSON body | `desktop/tests/test_openai_client.py` | URL ending `/images/generations`、`quality=medium` |
| edits multipart body | 同上 | URL ending `/images/edits`、`image[]` <= 4、`mask` optional |
| enhance prompt | 同上 | URL ending `/chat/completions`、model `gpt-4o-mini` |
| 401 | 同上 | raise `OpenAIClientError("API Key 無效或已過期")` |
| 413 | 同上 | raise `OpenAIClientError("圖片太大...")` |

### 2.5 quality_dial.py（成本撥盤）

檔案：`desktop/app/widgets/quality_dial.py`  
預估：80-120 行  
對應：`SDD §4.2 quality 預算撥盤`、`PLAN-sprint-1.5 §4.2 cost 表格`。

完整 widget 框架：

```python
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


QUALITY_OPTIONS = [
    QualityOption("low", "草稿 low", 0.005, "快速構圖與方向測試"),
    QualityOption("medium", "探索 medium", 0.04, "一般 prompt 測試與方向比較"),
    QualityOption("high", "交付 high", 0.17, "中文文字、海報、資訊圖與客戶交付圖"),
]

HIGH_QUALITY_TRIGGERS = [
    "中文", "繁體", "海報", "poster", "infographic",
    "資訊圖", "報表", "圖表", "文字清晰", "可讀文字",
]


def estimate_image_cost(n: int, quality: str) -> float:
    unit = {item.key: item.usd_per_image for item in QUALITY_OPTIONS}[quality]
    return round(n * unit, 3)


def suggest_quality(prompt: str, current: str) -> tuple[str, str]:
    text = prompt.lower()
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
            button = QRadioButton(f"{option.label} · ${option.usd_per_image:.3f}/張", self)
            button.setToolTip(option.description)
            self._buttons[option.key] = button
            self._group.addButton(button)
            layout.addWidget(button)
            button.toggled.connect(lambda checked, key=option.key: self._on_toggled(key, checked))
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
        self._buttons[quality].setChecked(True)
        self._update_cost_label()

    def set_image_count(self, count: int) -> None:
        self._image_count = max(1, count)
        self._update_cost_label()

    def _update_cost_label(self) -> None:
        quality = self.quality()
        total = estimate_image_cost(self._image_count, quality)
        self._cost_label.setText(f"Estimated cost: {self._image_count} × {quality} = ${total:.3f}")
```

pytest-qt 驗收：

```python
def test_quality_dial_defaults_to_medium(qtbot):
    widget = QualityDial()
    qtbot.addWidget(widget)
    assert widget.quality() == "medium"
    assert estimate_image_cost(3, "medium") == 0.12
```

### 2.6 requirements.txt 與 venv 設定

檔案：`desktop/requirements.txt`  
依賴 pin 以 2026-04-29 PyPI release history 為準；避免使用 pre-release。

```text
PyQt6==6.11.0
httpx==0.28.1
keyring==25.7.0
pytest==9.0.3
pytest-qt==4.5.0
pytest-asyncio==1.3.0
pytest-mock==3.15.1
respx==0.23.1
```

venv 建議：

```bash
cd /Users/jeyengjau/Desktop/APP/forma-studio-v2.5
python3.12 -m venv .venv-desktop
source .venv-desktop/bin/activate
python -m pip install --upgrade pip
python -m pip install -r desktop/requirements.txt
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"
```

預期 stdout：

```text
PyQt6 OK
```

### 2.7 pytest-qt smoke test

檔案：`desktop/tests/test_main_window.py`

```python
from pathlib import Path

from app.main_window import MainWindow


def test_main_window_smoke(qtbot):
    window = MainWindow(project_root=Path(__file__).resolve().parents[2])
    qtbot.addWidget(window)
    window.show()
    assert window.windowTitle() == "Forma Studio v2.5"
    assert window.tabs.count() == 4
```

執行：

```bash
QT_QPA_PLATFORM=offscreen pytest desktop/tests/test_main_window.py -q
```

預期 stdout：

```text
1 passed
```

### 2.8 驗收

Sprint 2A done criteria：

| Gate | 命令 | 預期 |
|---|---|---|
| App 啟動 | `python desktop/main.py` | 主視窗顯示 4 tab |
| Keyring mock | `pytest desktop/tests/test_key_store.py -q` | PASS，不碰真實 Keychain |
| Client mock | `pytest desktop/tests/test_openai_client.py -q` | generations / edits / enhance body PASS |
| Quality widget | `pytest desktop/tests/test_quality_dial.py -q` | default medium、cost formula PASS |
| 全部 2A | `QT_QPA_PLATFORM=offscreen pytest desktop/tests -q` | 2A tests PASS |

不允許通過條件：

| 問題 | 處理 |
|---|---|
| API Key 寫入 `.env` / json / local file | 退回重做，只准 keyring |
| `main.py` hardcode 絕對路徑 | 退回改 `Path(__file__)` |
| Python 注釋使用 `/* */` | 退回改 `#` |
| widget 初始化時呼叫真 OpenAI API | 退回，API 只在使用者按送出後呼叫 |

---

## 三、Sprint 2B：edit endpoint UI

### 3.1 reference_drop_zone.py（最多 4 張，drag-drop）

檔案：`desktop/app/widgets/reference_drop_zone.py`  
對應：`SDD §4.1 多參考圖`。

Class / function：

```python
class ReferenceDropZone(QWidget):
    images_changed = pyqtSignal(list)

    def image_paths(self) -> list[Path]: ...
    def add_paths(self, paths: list[Path]) -> None: ...
    def clear(self) -> None: ...
    def dragEnterEvent(self, event: QDragEnterEvent) -> None: ...
    def dropEvent(self, event: QDropEvent) -> None: ...
```

驗收規則：

| 規則 | UI 顯示 | 測試 |
|---|---|---|
| 最少 1 張 | edit submit 前檢查 | `edit_image` 無圖 raises |
| 最多 4 張 | `最多 4 張，請移除多餘圖片` | drop 5 張只保留前 4 或阻擋 |
| 副檔名 | PNG/JPEG/WebP | `.gif` 阻擋 |
| 讀檔 | `Path.exists()` | missing path 顯示錯誤 |

### 3.2 mask_uploader.py（PNG alpha 驗證）

檔案：`desktop/app/widgets/mask_uploader.py`  
對應：`SDD §4.1 mask 可選 PNG alpha`。

Class / function：

```python
class MaskUploader(QWidget):
    mask_changed = pyqtSignal(object)

    def mask_path(self) -> Path | None: ...
    def set_mask(self, path: Path) -> None: ...
    def clear_mask(self) -> None: ...


def validate_png_alpha(path: Path) -> tuple[bool, str]: ...
```

PNG alpha 檢查建議使用 `QImage`，不新增 Pillow 依賴：

```python
image = QImage(str(path))
if image.isNull():
    return False, "mask 無法讀取"
if not image.hasAlphaChannel():
    return False, "mask 必須是 PNG alpha"
```

### 3.3 image_edit_panel.py（整合 endpoint 切換 + Quality + 送出）

檔案：`desktop/app/widgets/image_edit_panel.py`  
對應：`SDD §4.1 按鈕分開`。

UI 草圖：

```text
┌─ 圖像生成 / 修改 ───────────────────────────────────────────┐
│ Prompt                                                      │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ 請把這張既有海報改成深色版本，保留標題階層與品牌 Logo... │  │
│ └────────────────────────────────────────────────────────┘  │
│ Reference Images（最多 4 張）                              │
│ [drop #1] [drop #2] [drop #3] [drop #4]                    │
│ Mask（選填，PNG alpha） [上傳 mask] [清除]                 │
│ Quality  [草稿 low] [探索 medium] [交付 high]              │
│                                        [生成新圖] [修改既有圖]│
└────────────────────────────────────────────────────────────┘
```

Class / function：

```python
class ImageEditPanel(QWidget):
    image_generated = pyqtSignal(bytes)
    error_raised = pyqtSignal(str)

    def __init__(self, client_factory: Callable[[], OpenAIClient], parent=None) -> None: ...
    def set_prompt(self, prompt: str) -> None: ...
    def prompt(self) -> str: ...
    def _on_generate_clicked(self) -> None: ...
    def _on_edit_clicked(self) -> None: ...
    async def _generate(self) -> None: ...
    async def _edit(self) -> None: ...
```

送出前檢查：

| Endpoint | 必要條件 | 錯誤訊息 |
|---|---|---|
| generations | prompt 非空 | `請先輸入 prompt` |
| edits | prompt 非空 + reference >= 1 | `修改既有圖需要至少 1 張參考圖` |
| edits | reference <= 4 | `最多 4 張，請移除多餘圖片` |
| edits | mask 為 PNG alpha 或 None | `mask 必須是 PNG alpha` |

### 3.4 與 main_window 接線

改動點：

| 檔案 | 變更 |
|---|---|
| `desktop/app/main_window.py` | `_build_image_tab()` 改回傳 `ImageEditPanel` |
| `desktop/app/api/key_store.py` | `MainWindow._create_client()` 從 keyring 取 key |
| `desktop/app/widgets/image_edit_panel.py` | 接 `QualityDial.quality()` |

接線簽名：

```python
def _create_openai_client(self) -> OpenAIClient:
    key = key_store.get_key()
    if not key:
        raise RuntimeError("請先設定 API Key")
    return OpenAIClient(key)
```

### 3.5 pytest-qt 測試

測試清單：

| 測試 | 內容 |
|---|---|
| `test_reference_drop_zone_limits_to_four` | drop 5 張會阻擋或只留 4 張 |
| `test_mask_uploader_rejects_non_png` | `.jpg` mask 拒絕 |
| `test_mask_uploader_requires_alpha` | PNG 無 alpha 拒絕 |
| `test_image_edit_requires_reference` | 按 `修改既有圖` 無 reference 會 emit error |
| `test_image_generate_uses_quality` | `generate_image(... quality="high")` |

命令：

```bash
QT_QPA_PLATFORM=offscreen pytest desktop/tests/test_image_edit_panel.py -q
```

預期 stdout：

```text
5 passed
```

### 3.6 驗收

Sprint 2B done criteria：

| Gate | 驗收 |
|---|---|
| UI | image tab 同時可見 prompt、reference、mask、quality、兩個送出按鈕 |
| API | `生成新圖` 呼叫 `/images/generations`，`修改既有圖` 呼叫 `/images/edits` |
| 防呆 | 無 reference 時不送 API |
| cache | 回傳 PNG bytes 只進 session cache，不覆蓋原檔 |
| 測試 | `pytest desktop/tests/test_image_edit_panel.py -q` PASS |

---

## 四、Sprint 2C：DESIGN.md 共享記憶

### 4.1 design_memory.py parser

檔案：`desktop/app/utils/design_memory.py`  
對應：`SDD §4.3 DESIGN.md 共享記憶`。

Dataclass：

```python
@dataclass
class DesignMemory:
    project_name: str
    brand_name: str
    industry: str
    audience: list[str]
    tone_of_voice: str
    color_tokens: dict[str, str]
    typography: dict[str, str]
    visual_rules: list[str]
    prompt_defaults: dict[str, str]
    negative_constraints: list[str]
```

Function：

```python
def load_design_memory(project_dir: Path) -> DesignMemory | None: ...
def parse_design_memory(text: str) -> DesignMemory: ...
def validate_design_memory(memory: DesignMemory) -> list[str]: ...
def save_design_memory(project_dir: Path, memory: DesignMemory) -> Path: ...
def build_system_prompt(base: str, memory: DesignMemory | None) -> str: ...
```

解析策略：

| 區塊 | 解析方式 |
|---|---|
| `## Brand Identity` | bullet key-value |
| `## Color Tokens` | markdown table |
| `## Typography` | bullet key-value |
| `## Visual Rules` | bullet list |
| `## Prompt Defaults` | bullet key-value |
| `## Negative Constraints` | bullet list |

### 4.2 brand_settings_tab.py GUI

檔案：`desktop/app/pages/brand_settings_tab.py`

Class / signal：

```python
class BrandSettingsTab(QWidget):
    memory_changed = pyqtSignal(object)

    def __init__(self, project_root: Path, parent=None) -> None: ...
    def load_from_project(self, project_dir: Path) -> None: ...
    def save_to_project(self) -> None: ...
    def current_memory(self) -> DesignMemory: ...
    def set_memory(self, memory: DesignMemory) -> None: ...
```

欄位：

| UI 欄位 | Mapping |
|---|---|
| Project name | `DesignMemory.project_name` |
| Brand name | `brand_name` |
| Industry | `industry` |
| Audience | `audience`，每行一個 |
| Tone of voice | `tone_of_voice` |
| Color tokens | table，`token/value` |
| Typography | `heading/body/mono` |
| Visual rules | 每行一條 |
| Negative constraints | 每行一條 |

### 4.3 system prompt 注入流程

流程：

```text
BrandSettingsTab.save_to_project()
  -> design_memory.save_design_memory()
  -> MainWindow receives memory_changed
  -> ImageEditPanel stores DesignMemory
  -> OpenAIClient.enhance_prompt(system_prompt=build_system_prompt(...))
  -> OpenAIClient.generate_image(prompt=prompt_with_memory)
```

系統 prompt 範例：

```python
BASE_IMAGE_SYSTEM_PROMPT = "You are Forma Studio. Generate precise, production-ready image prompts."

system_prompt = build_system_prompt(BASE_IMAGE_SYSTEM_PROMPT, memory)
```

### 4.4 與 openai_client 整合

整合點：

| Method | 整合方式 |
|---|---|
| `enhance_prompt()` | 直接傳 `system_prompt` |
| `generate_image()` | 若 API 不接受 system role，先將 memory 摘要 prepend 到 prompt |
| `edit_image()` | 同 `generate_image()`，但保留使用者原 prompt 最後優先 |

Prompt prepend 範例：

```python
def apply_design_memory_to_prompt(prompt: str, memory: DesignMemory | None) -> str:
    if not memory:
        return prompt
    return f"""Project DESIGN.md memory:
- Brand: {memory.brand_name}
- Industry: {memory.industry}
- Tone: {memory.tone_of_voice}
- Colors: {memory.color_tokens}
- Typography: {memory.typography}
- Visual rules: {memory.visual_rules}
- Negative constraints: {memory.negative_constraints}

User prompt:
{prompt}
"""
```

### 4.5 pytest-qt 測試

測試清單：

| 測試 | 內容 |
|---|---|
| `test_parse_design_memory_minimal` | `Brand Identity` + `Color Tokens` 可 parse |
| `test_validate_design_memory_requires_brand_name` | 缺 brand name 回 warning |
| `test_save_design_memory_roundtrip` | save 後 load 結構一致 |
| `test_brand_settings_tab_smoke` | qtbot 開頁不 crash |
| `test_build_system_prompt_injects_negative_constraints` | system prompt 含 constraints |

命令：

```bash
QT_QPA_PLATFORM=offscreen pytest desktop/tests/test_design_memory.py -q
```

預期 stdout：

```text
5 passed
```

### 4.6 驗收

Sprint 2C done criteria：

| Gate | 驗收 |
|---|---|
| parser | 可讀 SDD §4.3 schema |
| GUI | 可建立、修改、儲存 `DESIGN.md` |
| 注入 | enhance/generate/edit 都可套用 memory |
| fallback | 沒有 `DESIGN.md` 時 app 正常運作 |
| 測試 | `pytest desktop/tests/test_design_memory.py -q` PASS |

---

## 五、跨 sprint 通用元件

### 5.1 主題（QSS 沿用 v2.0 SDD）

`docs/SDD-desktop-v2.0.md` 不在本 repo；Sprint 2A 開工前需從 frozen repo 或備份補回 QSS 規格。補回前使用保守 dark QSS，不做 Web glow。

建議檔案：

```text
desktop/app/theme.py
```

簽名：

```python
def load_app_qss() -> str:
    # 先回傳 inline fallback；v2.0 QSS 補回後改讀 desktop/app/styles/app.qss
    return "QMainWindow { background: #101418; color: #eef2f6; }"
```

### 5.2 共用 helpers（檔案讀取、錯誤處理、toast）

建議集中：

```text
desktop/app/utils/files.py
desktop/app/utils/errors.py
desktop/app/widgets/toast.py
```

最小簽名：

```python
def repo_path(project_root: Path, *parts: str) -> Path: ...
def read_json(path: Path) -> dict: ...
def show_error(parent: QWidget, title: str, message: str) -> None: ...
def show_toast(parent: QWidget, message: str, timeout_ms: int = 3000) -> None: ...
```

### 5.3 i18n 預留（zh_TW 為主）

Sprint 2 不導入完整翻譯系統，只保留字串集中化空間：

```python
APP_LANGUAGE = "zh_TW"

TEXT = {
    "api_key_missing": "請先設定 API Key",
    "edit_requires_reference": "修改既有圖需要至少 1 張參考圖",
    "mask_requires_png_alpha": "mask 必須是 PNG alpha",
}
```

---

## 六、測試策略

### 6.1 pytest-qt 單元測試

範圍：

| 元件 | 測試檔 |
|---|---|
| `MainWindow` | `desktop/tests/test_main_window.py` |
| `QualityDial` | `desktop/tests/test_quality_dial.py` |
| `ReferenceDropZone` | `desktop/tests/test_image_edit_panel.py` |
| `MaskUploader` | `desktop/tests/test_image_edit_panel.py` |
| `BrandSettingsTab` | `desktop/tests/test_design_memory.py` |

命令：

```bash
QT_QPA_PLATFORM=offscreen pytest desktop/tests -q
```

### 6.2 整合測試（mock OpenAI）

使用 `respx` mock `httpx.AsyncClient`。

```python
@pytest.mark.asyncio
async def test_edit_image_posts_multipart(respx_mock, tmp_path):
    route = respx_mock.post("https://api.openai.com/v1/images/edits").mock(
        return_value=httpx.Response(200, json={"data": [{"b64_json": "iVBORw0KGgo="}]})
    )
    client = OpenAIClient("sk-test")
    await client.edit_image("edit", [tmp_path / "a.png"])
    assert route.called
```

### 6.3 手動 smoke test（macOS）

```bash
cd /Users/jeyengjau/Desktop/APP/forma-studio-v2.5
source .venv-desktop/bin/activate
python desktop/main.py
```

手動 checklist：

| 步驟 | 預期 |
|---|---|
| 啟動 | 4 tab 可切換 |
| 輸入 API Key | Keychain 儲存，重開仍顯示已設定 |
| Quality | 切 low/medium/high 成本 label 更新 |
| Drop reference | 1-4 張接受，第 5 張阻擋 |
| Mask | PNG alpha 接受，JPG 拒絕 |
| DESIGN.md | 可讀寫，不影響無檔專案 |

### 6.4 為什麼不用 Playwright（PyQt6 不適用）

Playwright 驗證瀏覽器 DOM、console error、網頁互動；PyQt6 是 native desktop widget，沒有 DOM。Sprint 2 改用：

| Web Sprint 1.5 | Desktop Sprint 2 |
|---|---|
| Playwright browser steps | pytest-qt widget interaction |
| console error | Qt signal / exception assertion |
| DOM selector | widget objectName / direct instance |
| network fetch mock | `respx` / injected `httpx.AsyncClient` |

---

## 七、打包與發佈（Sprint 2D backlog，本 PLAN 只先 outline）

### 7.1 PyInstaller .app

Backlog 檔案：

```text
desktop/packaging/forma-studio.spec
desktop/packaging/build_macos_app.sh
```

命令草案：

```bash
pyinstaller desktop/packaging/forma-studio.spec --clean --noconfirm
open dist/Forma\ Studio.app
```

### 7.2 簽名 + notarize

Backlog checklist：

| 項目 | 命令 |
|---|---|
| Developer ID | `codesign --deep --force --options runtime --sign "$APPLE_SIGN_ID" dist/Forma\ Studio.app` |
| Notary submit | `xcrun notarytool submit dist/FormaStudio.zip --keychain-profile "$NOTARY_PROFILE" --wait` |
| Staple | `xcrun stapler staple dist/Forma\ Studio.app` |

### 7.3 Windows .exe（後續）

Windows 不在 Sprint 2 實作；2D 後再開專章處理 Credential Manager、路徑、HiDPI、installer。

---

## 八、風險與回滾

### 8.1 風險清單（每個 Sprint 至少 3 個）

Sprint 2A：

| 風險 | 影響 | 對策 |
|---|---|---|
| `docs/SDD-desktop-v2.0.md` 缺檔 | QSS / v1.x skeleton 參考不足 | 先用 `desktop/README.md` + SDD §四；補回 frozen SDD 後再對齊 QSS |
| macOS keyring 權限彈窗 | 測試卡住或使用者困惑 | 測試全部 monkeypatch；手動 smoke 才碰真 Keychain |
| PyQt6 6.11.0 與本機 Python 不合 | app 無法安裝或啟動 | 固定 Python 3.12；必要時降 pin 到 6.10.2 |
| async client 與 Qt event loop 衝突 | 按鈕送出卡 UI | Sprint 2A 先只寫 client；2B 再決定 `asyncio.create_task` 或 `QThread` |

Sprint 2B：

| 風險 | 影響 | 對策 |
|---|---|---|
| multipart 欄位名稱與 API 行為變動 | edits endpoint 失敗 | client 隔離在 `openai_client.py`，mock body 測試 |
| 大圖造成 413 | 使用者無結果 | UI 顯示 `圖片太大...`，不重試 |
| mask alpha 判斷誤放行 | API 或輸出不符合預期 | `QImage.hasAlphaChannel()` + fixture 測試 |
| reference 第 5 張 UX 不明確 | 使用者不知道哪張被送出 | 明確阻擋並顯示錯誤，不自動吞掉 |

Sprint 2C：

| 風險 | 影響 | 對策 |
|---|---|---|
| DESIGN.md markdown 格式漂移 | parser 讀不到 tokens | parser 寬鬆，validate 給 warning |
| system prompt 太長 | 成本與效果不穩 | 注入摘要，不貼完整 Markdown |
| GUI save 覆蓋使用者註解 | 使用者資料流失 | 先讀 parse 後重寫標準 schema；儲存前提示 |
| 無 DESIGN.md 專案 | app 不能使用品牌記憶 | `load_design_memory()` 回 `None`，所有流程 fallback |

### 8.2 回滾策略（feature flag 同 web 版）

新增 feature flags：

```python
ENABLE_IMAGE_EDITS = True
ENABLE_DESIGN_MEMORY = True
ENABLE_PROMPT_ENHANCE = True
```

回滾表：

| 故障 | 回滾 |
|---|---|
| edits endpoint 不穩 | `ENABLE_IMAGE_EDITS=False`，隱藏 `修改既有圖`，保留 generations |
| DESIGN.md parser crash | `ENABLE_DESIGN_MEMORY=False`，品牌 tab 顯示維護中 |
| enhance prompt API 失敗 | `ENABLE_PROMPT_ENHANCE=False`，按鈕停用 |
| PyQt6 widget crash | lazy import，失敗時回 placeholder tab |

---

## 九、與 Web 版的同步策略

### 9.1 共用 prompt-library/*.json（讀同一份）

桌面版不複製 gallery 資料，直接讀：

```text
web/prompt-library/gallery-index.json
web/prompt-library/*.json
```

Loader 簽名：

```python
def load_gallery_index(project_root: Path) -> dict:
    path = project_root / "web" / "prompt-library" / "gallery-index.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_gallery_category(project_root: Path, file_name: str) -> dict:
    path = project_root / "web" / "prompt-library" / file_name
    return json.loads(path.read_text(encoding="utf-8"))
```

驗收：

```bash
python - <<'PY'
import json
from pathlib import Path
p = Path("web/prompt-library/gallery-index.json")
data = json.loads(p.read_text(encoding="utf-8"))
print(data["total_count"], len(data["categories"]))
PY
```

預期 stdout：

```text
116 17
```

### 9.2 craft.md / SKILL.md 共用

桌面版 enhance prompt 的 system prompt 不另開新規格，來源順序：

| 來源 | 用途 |
|---|---|
| `skills/forma-studio/references/craft.md` | 19 節 prompt 品質檢查 |
| `skills/forma-studio/SKILL.md` | 跨行業定位、使用限制 |
| `web/forma-studio.html` `ENHANCE_SYSTEM_PROMPT` | Sprint 1.6 已驗證的精簡版 |

Sprint 2A 先內建精簡 `ENHANCE_SYSTEM_PROMPT`；Sprint 2C 可改為讀檔 + fallback。

### 9.3 系統 prompt 同源（Tier 1.6 enhancePromptWithOpenAI 邏輯移植）

Web 版：

```javascript
async function enhancePromptWithOpenAI(promptText, apiKey) {
  const resp = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${apiKey}` },
    body: JSON.stringify({
      model: 'gpt-4o-mini',
      temperature: 0.2,
      messages: [
        { role: 'system', content: ENHANCE_SYSTEM_PROMPT },
        { role: 'user', content: promptText },
      ],
    }),
  });
}
```

Desktop 對應：

```python
await client.enhance_prompt(
    prompt,
    system_prompt=build_system_prompt(ENHANCE_SYSTEM_PROMPT, design_memory),
    temperature=0.2,
)
```

---

## 十、本 Sprint 不做的事（明確 scope-out）

### 10.1 不做 Web 版的 4 區塊 glow（桌面版用 tab + form 較簡）

桌面版採 `QTabWidget` + form layout。原因：

| Web | Desktop |
|---|---|
| 4 區塊 glow 適合單頁導引 | tab 適合長時間工作與設定 |
| Tailwind / CSS animation | QSS / native widgets |
| browser clipboard / DOM | native file dialog / drag-drop |

### 10.2 不做 Comment mode（v3.0 backlog）

Comment mode 需要 preview hit-test、pin storage、region prompt patch。這些不屬於 `SDD §4.1-4.3`。

### 10.3 不做多格式匯出（v3.0 backlog）

Sprint 2 只處理 PNG bytes session cache，不做 HTML / PDF / PPTX / ZIP / Markdown 匯出。

### 10.4 不做即時協作（v4.0+）

不做多人游標、共享 session、雲端同步。Sprint 2 的共享記憶只限本機 `DESIGN.md`。

---

## 十一、Sprint 2 最終驗收命令

完整流程：

```bash
cd /Users/jeyengjau/Desktop/APP/forma-studio-v2.5
source .venv-desktop/bin/activate
QT_QPA_PLATFORM=offscreen pytest desktop/tests -q
python desktop/main.py
```

預期 stdout：

```text
# pytest
18 passed

# python desktop/main.py
# 無 stdout；顯示 Forma Studio 主視窗
```

完成後建議更新：

```text
DEVLOG.md
HANDOFF.md
git tag v2.5-sprint-2
```

本 PLAN 不執行上述更新與 tag，只列 Sprint 2 完成後收尾建議。
