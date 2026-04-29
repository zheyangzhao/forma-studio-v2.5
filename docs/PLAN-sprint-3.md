# Forma Studio v3.0 · Sprint 3 實作計劃書

**版本**：v3.0 Sprint 3  
**日期**：2026-04-29  
**工作目錄**：`/Users/jeyengjau/Desktop/APP/forma-studio-v2.5`  
**輸出檔案**：`docs/PLAN-sprint-3.md`  
**基準狀態**：v2.5 Web Tier 1 + 1.5 完成；Desktop Tier 2 完成；gallery 116 條；桌面版 4 tab；最新 DEVLOG 紀錄 pytest 40 PASS。  

讀檔紀錄：

| 檔案 | 狀態 | 本 PLAN 採用方式 |
|---|---|---|
| `docs/research/v3.0-backlog-evaluation.md` | 已讀 | 依 §五推薦路線，M1 + M2 作為 Sprint 3 主線 |
| `docs/PLAN-sprint-2.md` §二/§三/§四 | 已讀 | 沿用章節密度、sample code、驗收表格格式 |
| `desktop/app/utils/design_memory.py` | 已讀 | v2.5 6 區塊 dataclass/parser/serializer/prompt injection 為相容基線 |
| `desktop/app/pages/brand_settings_tab.py` | 已讀 | v2.5 GUI 使用 `QFormLayout`、`QPlainTextEdit`、`QTableWidget` |
| `desktop/app/widgets/image_edit_panel.py` | 已讀 | export 入口從 prompt + `_last_result` + `_memory` 取資料 |
| `web/forma-studio.html` | 已讀 | Tier 1.6 `EnhanceBtn` / `OutBox` 模式作為 web export 入口參考 |
| `CLAUDE.md` | 已讀 | v2.5 技術棧、API Key、gallery source attribution、跨行業定位 |

與評估報告對照：

| 評估報告章節 | 本 PLAN 章節 | Sprint 3 立場 |
|---|---|---|
| §1.2 v3.0 路線 | §一 Sprint 3 範圍 | 採「低破壞、高交付價值」 |
| M1 schema 擴充 | §二 Sprint 3A | 詳細規格 + sample code |
| M2 Markdown/PDF export | §三 Sprint 3B + §四 Sprint 3C | 詳細規格 + sample code |
| M3 Comment mode | §五 Sprint 3D | outline only |
| M4 PPTX export | §六 Sprint 3E | outline only |

---

## 一、Sprint 3 範圍與分期

### 1.1 為什麼啟動 v3.0

v2.5 已完成跨行業 prompt gallery、OpenAI image generate/edit、Quality 撥盤、DESIGN.md 共享記憶與桌面版基礎 GUI。v3.0 的目標不是重寫產品，而是把 v2.5 已能產生的內容變成更穩定、可保存、可交付的工作成果。

主要缺口：

| 缺口 | v2.5 現況 | v3.0 處理 |
|---|---|---|
| 品牌記憶 | 6 區塊，涵蓋 identity/color/type/rules/defaults/negative | 擴充 spacing/components/motion/voice，但全部 optional |
| Markdown 交付 | Web 可複製文字，Desktop 可生成圖 | 匯出 prompt + metadata + 圖片 reference + attribution |
| PDF 交付 | 沒有正式報告/附件格式 | Desktop 優先提供 PDF export |
| 局部修改 | 圖片 edit + 手動 mask | Comment mode 只列 prototype，不搶主線 |
| PPTX | 無 | 後續 spike，不承諾 1:1 視覺還原 |

v3.0 的成功指標：

```text
v3.0 success
├── v2.5 專案資料仍可讀
├── 40 pytest 不退步
├── 116 gallery 不改 schema
├── Markdown export 可 diff、可交接
└── PDF export 可作為律師/教師/行銷交付附件
```

**決策摘要：Sprint 3 啟動原因是補齊品牌 schema 與交付格式，不做平台級重構。**

### 1.2 範圍 vs scope-out

| 優先序 | 項目 | Sprint 3 狀態 | 主要檔案 | 說明 |
|---:|---|---|---|---|
| 1 | DESIGN.md v3 optional sections | 必做 | `desktop/app/utils/design_memory.py` | v2.5 10 欄位不刪，新 4 欄位 optional |
| 2 | BrandSettingsTab v3 widgets | 必做 | `desktop/app/pages/brand_settings_tab.py` | 推薦 collapsible `QGroupBox` |
| 3 | Markdown export | 必做 | `desktop/app/utils/exporters/markdown_exporter.py` | 零重依賴，先 desktop |
| 4 | PDF export | 必做 | `desktop/app/utils/exporters/pdf_exporter.py` | 推薦 reportlab + Noto Sans TC |
| 5 | ImageEditPanel export buttons | 必做 | `desktop/app/widgets/image_edit_panel.py` | 從 prompt / last_result / memory 組 export |
| 6 | Web export | 延後 | `web/forma-studio.html` | 3C 後評估，不納入 3B gate |
| - | Web Comment mode | Outline only | TBD | 只做技術輪廓與 feature flag |
| - | PPTX export | Outline only | TBD | `python-pptx` spike |
| - | nexu-io 71 systems 匯入 | Scope out | 無 | 不導入品牌資料庫作核心依賴 |
| - | ZIP / HTML export | Scope out | 無 | export model 穩定後另案 |
| - | Figma / Sketch 整合 | Scope out | 無 | 不在 v3.0 |

Sprint 3 預期改動樹：

```text
forma-studio-v2.5/
└── desktop/
    ├── app/
    │   ├── pages/
    │   │   └── brand_settings_tab.py       # 3A 修改
    │   ├── utils/
    │   │   ├── design_memory.py            # 3A 修改
    │   │   └── exporters/                  # 3B/3C 新增
    │   │       ├── __init__.py
    │   │       ├── markdown_exporter.py
    │   │       └── pdf_exporter.py
    │   └── widgets/
    │       └── image_edit_panel.py         # 3B/3C 修改
    ├── assets/
    │   └── fonts/
    │       └── NotoSansTC-Regular.otf      # 3C 新增，需授權確認
    └── tests/
        ├── test_design_memory.py           # 3A 擴充
        ├── test_brand_settings_tab.py      # 3A/3B/3C 擴充或新增
        └── test_exporters.py               # 3B/3C 新增
```

**決策摘要：Scope 只包含 v3 schema、Markdown、PDF；Comment/PPTX 只寫 outline，不進入本 sprint 必做 gate。**

### 1.3 分期策略：3A / 3B / 3C 詳細，3D / 3E outline

| 分期 | 對應評估報告 | 目標 | 預估 | 可獨立發布 |
|---|---|---|---:|---|
| Sprint 3A | M1 | DESIGN.md schema 擴充，parser/GUI/prompt injection/test | 18-28h | 可 |
| Sprint 3B | M2 Phase 1 | Export model + Markdown exporter + GUI button | ~12h | 可 |
| Sprint 3C | M2 Phase 2 | PDF exporter + 中文字型 + GUI button | 16-34h | 可 |
| Sprint 3D | M3 | Web Comment mode prototype | 36-58h | 否，需使用者回饋 |
| Sprint 3E | M4 | PPTX export spike | 20-34h | 否，需 spike 結論 |

順序不得調換：

```text
3A DESIGN.md v3
  -> 3B Markdown export
      -> 3C PDF export
          -> 3D / 3E 評估點
```

原因：

| 順序 | 原因 |
|---|---|
| 3A before 3B | Markdown export 需要穩定的 memory serialization 與 metadata |
| 3B before 3C | PDF 可重用 export model 與 metadata helper |
| 3D after 3C | Comment mode 會引入 artifact/version model，不應干擾 export 主線 |
| 3E after 3C | PPTX layout 需沿用 PDF 的交付內容模型 |

**決策摘要：3A → 3B → 3C 是必做主線；3D/3E 在主線穩定後再排。**

### 1.4 預估工時與里程碑

| 里程碑 | 範圍 | 工時 | 驗收標準 |
|---|---|---:|---|
| M1 | DESIGN.md schema 擴充與 backward-compatible parser | 18-28h | 舊 6 區塊可讀；新 4 欄位可 roundtrip；既有 40 pytest 不退步 |
| M2a | Markdown export MVP | ~12h | 可匯出 frontmatter、prompt、metadata、圖片 reference、attribution |
| M2b | PDF export MVP | 16-34h | PDF 可含 cover、prompt、圖片、metadata、footer；中文字型可控 |
| M3 | Web Comment mode prototype | 36-58h | iframe pin/comment/patch flow；feature flag 預設關 |
| M4 | PPTX export spike | 20-34h | 3-5 種 layout 可編輯；不承諾視覺 1:1 |

Gate 命令：

```bash
cd /Users/jeyengjau/Desktop/APP/forma-studio-v2.5
QT_QPA_PLATFORM=offscreen pytest desktop/tests -q
```

預期 stdout：

```text
40+ passed
```

**決策摘要：Sprint 3 的 release gate 是「v2.5 全部測試不退步 + 新增測試通過」。**

---

## 二、Sprint 3A：DESIGN.md schema 擴充（M1，18-28h）

### 2.1 nexu-io 9-section schema 對照

評估報告指出 nexu-io/open-design 的 9 section 對 LLM 友善，但不是 deterministic parser schema。Forma Studio v3.0 只借鑑可控子集。

| nexu-io section | v3.0 採用 | Forma 欄位 | 說明 |
|---|---|---|---|
| Visual Theme & Atmosphere | 部分 | `visual_rules` | 仍用 v2.5 list，避免新增大段自然語言 |
| Color System | 已有 | `color_tokens` | 保留 v2.5 table |
| Typography | 已有 | `typography` | 保留 v2.5 kv |
| Spacing & Layout | 新增 | `spacing_tokens` | kv table / bullet kv |
| Components | 新增 | `components` | list，先不做 component schema object |
| Motion | 新增 | `motion` | kv |
| Voice & Tone | 擴充 | `voice_signals` | list；保留既有 `tone_of_voice` |
| Brand Signals | 不獨立 | `visual_rules` / `voice_signals` | 合併，不新增欄位 |
| Anti-patterns | 已有 | `negative_constraints` | 保留 v2.5 list |

v3.0 目標 schema：

```text
DESIGN.md v3
├── v2.5 stable
│   ├── Brand Identity
│   ├── Color Tokens
│   ├── Typography
│   ├── Visual Rules
│   ├── Prompt Defaults
│   └── Negative Constraints
└── v3 optional
    ├── Spacing & Layout
    ├── Components
    ├── Motion
    └── Voice & Copy
```

**決策摘要：採 v2.5 + 4 optional sections，不採完整 nexu-io 9-section。**

### 2.2 v2.5 6 區塊 → v3.0 9 區塊 mapping（向後相容）

| v2.5 區塊 | v2.5 欄位 | v3.0 行為 |
|---|---|---|
| `## Brand Identity` | `project_name`, `brand_name`, `industry`, `audience`, `tone_of_voice` | 原樣保留 |
| `## Color Tokens` | `color_tokens` | 原樣保留，table parser 不退步 |
| `## Typography` | `typography` | 原樣保留 |
| `## Visual Rules` | `visual_rules` | 原樣保留；可吸收 brand signals |
| `## Prompt Defaults` | `prompt_defaults` | 原樣保留 |
| `## Negative Constraints` | `negative_constraints` | 原樣保留 |
| `## Spacing & Layout` | `spacing_tokens` | 新增 optional；缺失回 `{}` |
| `## Components` | `components` | 新增 optional；缺失回 `[]` |
| `## Motion` | `motion` | 新增 optional；缺失回 `{}` |
| `## Voice & Copy` | `voice_signals` | 新增 optional；缺失回 `[]` |

新區塊 Markdown 範例：

```markdown
## Spacing & Layout
| token | value |
|---|---|
| spacing_base | 4px |
| container_max | 1120px |
| grid | 12 columns |

## Components
- Button: 8px radius, icon-only when symbol is familiar
- Card: only for repeated items, not full page sections
- Toolbar: fixed height, no layout shift on hover

## Motion
- duration_fast: 120ms
- duration_standard: 220ms
- easing_standard: cubic-bezier(0.2, 0, 0, 1)

## Voice & Copy
- 直接、克制、可驗證
- 避免空泛口號與未驗證承諾
- CTA 用清楚動詞，不用誇大形容
```

相容規則：

| 情境 | 預期 |
|---|---|
| v2.5 只含 6 區塊 | parse 成功，新欄位 default |
| v3.0 含 10 欄位 | parse 成功，roundtrip 不丟資料 |
| 新區塊欄位 typo | 回 warning，不 crash |
| 未知 section | 忽略或 warning，不阻擋儲存 |
| serializer 寫 v3 | 新欄位有值才 emit section |

**決策摘要：v3.0 DESIGN.md 是 v2.5 的超集；空的新欄位不得寫出空 section。**

### 2.3 design_memory.py 升級：dataclass 新增 tokens / components / motion / voice

檔案：`desktop/app/utils/design_memory.py`  
預估：4-6h  
限制：既有 10 欄位不刪、不改語意；只加 optional 欄位。

完整 dataclass：

```python
from dataclasses import asdict, dataclass, field


@dataclass
class DesignMemory:
    # v2.5 既有 10 欄位（向後相容，不刪）
    project_name: str = ""
    brand_name: str = ""
    industry: str = ""
    audience: list[str] = field(default_factory=list)
    tone_of_voice: str = ""
    color_tokens: dict[str, str] = field(default_factory=dict)
    typography: dict[str, str] = field(default_factory=dict)
    visual_rules: list[str] = field(default_factory=list)
    prompt_defaults: dict[str, str] = field(default_factory=dict)
    negative_constraints: list[str] = field(default_factory=list)

    # v3.0 新增 4 欄位（all optional）
    spacing_tokens: dict[str, str] = field(default_factory=dict)
    components: list[str] = field(default_factory=list)
    motion: dict[str, str] = field(default_factory=dict)
    voice_signals: list[str] = field(default_factory=list)

    def is_empty(self) -> bool:
        return not any(asdict(self).values())
```

新區塊解析規則：

| Section | parser | 欄位 | Typo policy |
|---|---|---|---|
| `## Spacing & Layout` | table first，fallback bullet kv | `spacing_tokens` | 非 kv/list 行 warning |
| `## Components` | list lines；`- Name: rule` 仍存整行字串 | `components` | 空行忽略 |
| `## Motion` | bullet kv | `motion` | 未知 key 接受，但空值 warning |
| `## Voice & Copy` | list lines | `voice_signals` | bullet kv 也可作 list 字串 |

建議常數：

```python
V3_OPTIONAL_SECTIONS = {
    "Spacing & Layout",
    "Components",
    "Motion",
    "Voice & Copy",
}
```

**決策摘要：dataclass 只做 additive change，確保舊 `DesignMemory(...)` 呼叫仍可運作。**

### 2.4 parser 升級：保留舊 6 區塊讀取，新區塊 optional

檔案：`desktop/app/utils/design_memory.py`  
預估：5-8h  
目標：維持現有 `_split_sections()`、`_parse_kv_lines()`、`_parse_list_lines()`、`_parse_table_lines()` 模式，不重寫 parser。

建議新增 warning collector：

```python
@dataclass
class ParseResult:
    memory: DesignMemory
    warnings: list[str] = field(default_factory=list)


def parse_design_memory_with_warnings(text: str) -> ParseResult:
    sections = _split_sections(text)
    memory = DesignMemory()
    warnings: list[str] = []

    # v2.5 區塊照舊解析
    if "Brand Identity" in sections:
        kv = _parse_kv_lines(sections["Brand Identity"])
        memory.project_name = kv.get("project_name", "")
        memory.brand_name = kv.get("brand_name", "")
        memory.industry = kv.get("industry", "")
        memory.tone_of_voice = kv.get("tone_of_voice", "")
        memory.audience = _parse_audience(kv.get("audience", ""))

    if "Color Tokens" in sections:
        memory.color_tokens = _parse_table_lines(sections["Color Tokens"])

    if "Typography" in sections:
        memory.typography = _parse_kv_lines(sections["Typography"])

    if "Visual Rules" in sections:
        memory.visual_rules = _parse_list_lines(sections["Visual Rules"])

    if "Prompt Defaults" in sections:
        memory.prompt_defaults = _parse_kv_lines(sections["Prompt Defaults"])

    if "Negative Constraints" in sections:
        memory.negative_constraints = _parse_list_lines(
            sections["Negative Constraints"]
        )

    # v3.0 optional 區塊：缺失時維持 default_factory
    if "Spacing & Layout" in sections:
        table_values = _parse_table_lines(sections["Spacing & Layout"])
        bullet_values = _parse_kv_lines(sections["Spacing & Layout"])
        memory.spacing_tokens = table_values or bullet_values
        warnings.extend(
            _warn_unparsed_lines(
                "Spacing & Layout",
                sections["Spacing & Layout"],
                allowed=("table", "kv"),
            )
        )

    if "Components" in sections:
        memory.components = _parse_component_lines(sections["Components"])

    if "Motion" in sections:
        memory.motion = _parse_kv_lines(sections["Motion"])
        for key, value in memory.motion.items():
            if not value:
                warnings.append(f"Motion 欄位 '{key}' 沒值")

    if "Voice & Copy" in sections:
        memory.voice_signals = _parse_voice_lines(sections["Voice & Copy"])

    typo_candidates = {
        "Spacing Layout": "Spacing & Layout",
        "Voice and Copy": "Voice & Copy",
        "Voice & Tone": "Voice & Copy",
        "Component": "Components",
    }
    for seen, expected in typo_candidates.items():
        if seen in sections:
            warnings.append(f"疑似 section typo：'{seen}'，是否要寫成 '{expected}'")

    return ParseResult(memory=memory, warnings=warnings)


def parse_design_memory(text: str) -> DesignMemory:
    # 保留 v2.5 public API；呼叫者不需要處理 warnings
    return parse_design_memory_with_warnings(text).memory
```

新 helper：

```python
def _parse_component_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        m = _BULLET_LIST_RE.match(line)
        if m:
            item = m.group(1).strip()
            if item:
                out.append(item)
    return out


def _parse_voice_lines(lines: list[str]) -> list[str]:
    return _parse_component_lines(lines)


def _warn_unparsed_lines(
    section: str,
    lines: list[str],
    *,
    allowed: tuple[str, ...],
) -> list[str]:
    warnings: list[str] = []
    for line in lines:
        text = line.strip()
        if not text or text.startswith("|") or text.startswith("-"):
            continue
        warnings.append(f"{section} 無法解析行：{text[:80]}")
    return warnings
```

Serializer 規則：

```python
def memory_to_markdown(memory: DesignMemory) -> str:
    out: list[str] = ["# Forma Studio · DESIGN.md", ""]

    # v2.5 sections 仍照舊輸出，保護既有 GUI roundtrip
    out.append("## Brand Identity")
    out.append(f"- project_name: {memory.project_name}")
    out.append(f"- brand_name: {memory.brand_name}")
    out.append(f"- industry: {memory.industry}")
    out.append(f"- audience: {', '.join(memory.audience)}")
    out.append(f"- tone_of_voice: {memory.tone_of_voice}")
    out.append("")

    # 省略：Color / Typography / Visual / Prompt / Negative 既有邏輯

    # v3.0 sections：有值才 emit，避免空 section
    if memory.spacing_tokens:
        out.append("## Spacing & Layout")
        out.append("")
        out.append("| token | value |")
        out.append("|---|---|")
        for token, value in memory.spacing_tokens.items():
            out.append(f"| {token} | {value} |")
        out.append("")

    if memory.components:
        out.append("## Components")
        for item in memory.components:
            out.append(f"- {item}")
        out.append("")

    if memory.motion:
        out.append("## Motion")
        _emit_kv(out, memory.motion)
        out.append("")

    if memory.voice_signals:
        out.append("## Voice & Copy")
        for item in memory.voice_signals:
            out.append(f"- {item}")
        out.append("")

    return "\n".join(out)
```

向後相容測試資料：

```python
V25_DESIGN_MD = """# Forma Studio · DESIGN.md

## Brand Identity
- project_name: 舊專案
- brand_name: ACME
- industry: legal
- audience: 律師, 企業客戶
- tone_of_voice: 嚴肅高端

## Color Tokens
| token | value |
|---|---|
| primary | #123456 |

## Typography
- heading: Noto Serif TC
- body: Noto Sans TC

## Visual Rules
- 不用 emoji 圖標

## Prompt Defaults
- quality: high

## Negative Constraints
- watermark
"""


def test_v25_defaults():
    memory = parse_design_memory(V25_DESIGN_MD)
    assert memory.spacing_tokens == {}
    assert memory.components == []
    assert memory.motion == {}
    assert memory.voice_signals == []
```

**決策摘要：新增 `parse_design_memory_with_warnings()`，但保留舊 `parse_design_memory()` 回傳型別。**

### 2.5 brand_settings_tab.py GUI 增加 collapsible sections

檔案：`desktop/app/pages/brand_settings_tab.py`  
預估：5-8h  
方案比較：

| 方案 | 作法 | 優點 | 缺點 | 判斷 |
|---|---|---|---|---|
| a | collapsible `QGroupBox` | 保持單頁可滾；不切斷使用流程 | 需注意高度 | 推薦 |
| b | `QTabWidget` 內再放 `QTabWidget` | 分類清楚 | 過度切割；使用者要切太多層 | 不推薦 |

Widget 新增：

```python
from PyQt6.QtWidgets import QGroupBox


class BrandSettingsTab(QWidget):
    def __init__(self, project_root: Path, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # v2.5 existing widgets...
        self.project_name_edit = QLineEdit(self)
        self.brand_name_edit = QLineEdit(self)
        self.industry_edit = QLineEdit(self)
        self.audience_edit = QLineEdit(self)
        self.tone_edit = QLineEdit(self)

        # v3.0 optional widgets
        self.spacing_edit = QPlainTextEdit(self)
        self.spacing_edit.setPlaceholderText(
            "key: value，每行一筆\n例如：\nspacing_base: 4px\ncontainer_max: 1120px"
        )

        self.components_edit = QPlainTextEdit(self)
        self.components_edit.setPlaceholderText(
            "每行一個 component rule\n例如：\nButton: 8px radius, no emoji icon"
        )

        self.motion_edit = QPlainTextEdit(self)
        self.motion_edit.setPlaceholderText(
            "key: value，每行一筆\n例如：\nduration_fast: 120ms\neasing_standard: cubic-bezier(0.2, 0, 0, 1)"
        )

        self.voice_signals_edit = QPlainTextEdit(self)
        self.voice_signals_edit.setPlaceholderText(
            "每行一條 copy / voice rule\n例如：\n直接、克制、可驗證"
        )
```

Collapsible group helper：

```python
def _make_group(self, title: str, widget: QWidget) -> QGroupBox:
    group = QGroupBox(title, self)
    group.setCheckable(True)
    group.setChecked(False)
    layout = QVBoxLayout(group)
    layout.addWidget(widget)
    widget.setVisible(False)
    group.toggled.connect(widget.setVisible)
    return group
```

`_build_ui()` 新增位置：放在 v2.5 `Negative Constraints` 後、save row 前。

```python
def _build_ui(self) -> None:
    outer = QVBoxLayout(self)

    # v2.5 existing layout...
    outer.addWidget(QLabel("Negative Constraints（每行一條）"))
    outer.addWidget(self.negative_edit)

    # v3.0 advanced sections
    outer.addWidget(self._make_group("Spacing & Layout（v3 optional）", self.spacing_edit))
    outer.addWidget(self._make_group("Components（v3 optional）", self.components_edit))
    outer.addWidget(self._make_group("Motion（v3 optional）", self.motion_edit))
    outer.addWidget(self._make_group("Voice & Copy（v3 optional）", self.voice_signals_edit))

    # save row...
```

`current_memory()` 改動：

```python
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
    memory.visual_rules = _text_to_list(self.visual_rules_edit.toPlainText())
    memory.prompt_defaults = _text_to_kv(self.prompt_defaults_edit.toPlainText())
    memory.negative_constraints = _text_to_list(self.negative_edit.toPlainText())

    # v3.0 optional
    memory.spacing_tokens = _text_to_kv(self.spacing_edit.toPlainText())
    memory.components = _text_to_list(self.components_edit.toPlainText())
    memory.motion = _text_to_kv(self.motion_edit.toPlainText())
    memory.voice_signals = _text_to_list(self.voice_signals_edit.toPlainText())
    return memory
```

`set_memory()` 改動：

```python
def set_memory(self, memory: DesignMemory) -> None:
    self.project_name_edit.setText(memory.project_name)
    self.brand_name_edit.setText(memory.brand_name)
    self.industry_edit.setText(memory.industry)
    self.audience_edit.setText(", ".join(memory.audience))
    self.tone_edit.setText(memory.tone_of_voice)
    self.typography_edit.setPlainText(_kv_to_text(memory.typography))
    self.visual_rules_edit.setPlainText(_list_to_text(memory.visual_rules))
    self.prompt_defaults_edit.setPlainText(_kv_to_text(memory.prompt_defaults))
    self.negative_edit.setPlainText(_list_to_text(memory.negative_constraints))
    self._dict_to_color_table(memory.color_tokens)

    # v3.0 optional
    self.spacing_edit.setPlainText(_kv_to_text(memory.spacing_tokens))
    self.components_edit.setPlainText(_list_to_text(memory.components))
    self.motion_edit.setPlainText(_kv_to_text(memory.motion))
    self.voice_signals_edit.setPlainText(_list_to_text(memory.voice_signals))
```

GUI 驗收：

| Gate | 預期 |
|---|---|
| 開啟品牌記憶 tab | 既有欄位仍在 |
| 4 個 v3 group | 預設收合，可展開 |
| 空 v3 欄位儲存 | `DESIGN.md` 不出現空 v3 sections |
| v3 欄位填值儲存 | save/load 後一致 |

**決策摘要：GUI 採 collapsible group boxes；新增欄位可見但不干擾 v2.5 基本填寫。**

### 2.6 build_system_prompt 注入新欄位

檔案：`desktop/app/utils/design_memory.py`  
預估：2-3h  
限制：prompt 注入必須摘要化，不能把完整 DESIGN.md 原文塞進 image prompt。

建議改動：

```python
def build_system_prompt(base: str, memory: DesignMemory | None) -> str:
    if memory is None or memory.is_empty():
        return base

    lines = ["[Project DESIGN.md memory]"]
    if memory.brand_name:
        lines.append(f"- Brand: {memory.brand_name}")
    if memory.industry:
        lines.append(f"- Industry: {memory.industry}")
    if memory.audience:
        lines.append(f"- Audience: {', '.join(memory.audience)}")
    if memory.tone_of_voice:
        lines.append(f"- Tone: {memory.tone_of_voice}")
    if memory.color_tokens:
        cols = ", ".join(f"{k}={v}" for k, v in memory.color_tokens.items())
        lines.append(f"- Colors: {cols}")
    if memory.typography:
        typ = ", ".join(f"{k}={v}" for k, v in memory.typography.items())
        lines.append(f"- Typography: {typ}")
    if memory.spacing_tokens:
        spacing = ", ".join(f"{k}={v}" for k, v in memory.spacing_tokens.items())
        lines.append(f"- Spacing/Layout: {spacing}")
    if memory.components:
        lines.append("- Components: " + "; ".join(memory.components[:12]))
    if memory.motion:
        motion = ", ".join(f"{k}={v}" for k, v in memory.motion.items())
        lines.append(f"- Motion: {motion}")
    if memory.voice_signals:
        lines.append("- Voice/Copy: " + "; ".join(memory.voice_signals[:8]))
    if memory.visual_rules:
        lines.append("- Visual rules: " + "; ".join(memory.visual_rules))
    if memory.negative_constraints:
        lines.append("- Negative: " + "; ".join(memory.negative_constraints))

    return "\n".join(lines) + "\n\n" + base
```

注入順序：

```text
Brand / Industry / Audience
  -> Tone / Voice
  -> Colors / Typography / Spacing / Components / Motion
  -> Visual rules
  -> Negative constraints
  -> User prompt
```

**決策摘要：新欄位注入 system prompt，但使用摘要與數量上限，避免 prompt 過長。**

### 2.7 pytest 規格（既有 9 test + 新 8 test）

既有 v2.5 test 必須保留。新增測試：

| Test | 目的 |
|---|---|
| `test_v25_design_md_still_parses` | 用 v2.5 寫的 DESIGN.md 內容，v3.0 parser 應正確讀，新欄位回 default |
| `test_v3_full_schema_parse` | 9 區塊全填，parse 正確 |
| `test_v3_full_schema_roundtrip` | save → load 後新欄位仍一致 |
| `test_build_system_prompt_includes_v3_fields` | system prompt 含 spacing / components / motion |
| `test_apply_design_memory_to_prompt_v3` | apply 含新欄位 |
| `test_brand_settings_tab_v3_widgets` | qtbot 開頁，4 個新 widget 都建好 |
| `test_brand_settings_tab_v3_save_load` | 4 個新欄位 save/load roundtrip |
| `test_validate_design_memory_warns_typo` | 新欄位 typo 應 warn 不 crash |

Sample tests：

```python
def test_v3_full_schema_parse() -> None:
    memory = parse_design_memory(V3_DESIGN_MD)
    assert memory.spacing_tokens["spacing_base"] == "4px"
    assert "Button: 8px radius" in memory.components[0]
    assert memory.motion["duration_fast"] == "120ms"
    assert memory.voice_signals == ["直接、克制、可驗證"]


def test_v3_full_schema_roundtrip(tmp_path: Path) -> None:
    original = parse_design_memory(V3_DESIGN_MD)
    save_design_memory(tmp_path, original)
    reloaded = load_design_memory(tmp_path)
    assert reloaded == original


def test_validate_design_memory_warns_typo() -> None:
    result = parse_design_memory_with_warnings("## Voice and Copy\n- keep it short")
    assert result.memory.voice_signals == []
    assert any("Voice & Copy" in item for item in result.warnings)
```

pytest 命令：

```bash
QT_QPA_PLATFORM=offscreen pytest desktop/tests/test_design_memory.py desktop/tests/test_smoke.py -q
QT_QPA_PLATFORM=offscreen pytest desktop/tests -q
```

預期 stdout：

```text
48+ passed
```

**決策摘要：3A 至少新增 8 test；v2.5 既有 test 一條都不能刪。**

### 2.8 驗收與回滾

驗收：

| Gate | 命令 / 操作 | 預期 |
|---|---|---|
| Parser | `pytest desktop/tests/test_design_memory.py -q` | v2.5 + v3 schema 全通過 |
| GUI | `QT_QPA_PLATFORM=offscreen pytest desktop/tests/test_smoke.py -q` | BrandSettingsTab 建立成功 |
| Prompt injection | unit test | `Spacing/Layout`, `Components`, `Motion`, `Voice/Copy` 出現在 prompt |
| Manual | 開桌面版品牌記憶 tab | 4 個 optional group 可收合 |

回滾策略：

| 風險 | 回滾 |
|---|---|
| parser warning 太吵 | 保留 parse，暫時不在 GUI 顯示 warnings |
| GUI 太長 | 4 個 v3 group 預設收合 |
| prompt 過長 | 限制 components/voice 最大注入數量 |
| serializer 汙染 v2.5 DESIGN.md | 空欄位不 emit；必要時 feature flag 關閉 GUI v3 group |

**決策摘要：3A 可獨立發布；失敗時回滾 GUI 顯示即可，dataclass optional change 可保留。**

---

## 三、Sprint 3B：Markdown export（M2 Phase 1，~12h）

### 3.1 use case：律師提案附件、教師教材交付、行銷素材清單

| 使用者 | Markdown 用途 | 必含內容 |
|---|---|---|
| 律師 | 將生成圖與 prompt 放進提案附件或案件內部紀錄 | prompt、日期、品牌記憶摘要、source attribution |
| 教師 | 教材生成紀錄、課程講義素材清單 | prompt、圖片 reference、授課情境 metadata |
| 行銷 | 素材交接、A/B prompt diff、客戶 review | prompt、quality、圖片檔名、負面限制 |

Markdown 是 Sprint 3B 的第一個 export，原因：

```text
Markdown
├── 零重依賴
├── 可用 pytest snapshot 驗證
├── 可 diff / code review
├── 可貼到 Claude / NotebookLM / Google Docs
└── 可被 PDF/PPTX 後續流程重用
```

**決策摘要：Markdown export 先服務交接與審閱，不追求視覺排版。**

### 3.2 export 內容（Frontmatter YAML + prompt + metadata + 圖片 reference + source attribution）

輸出格式：

```markdown
---
schema_version: 1
export_type: markdown
created_at: "2026-04-29T10:00:00+08:00"
project_name: "ACME 提案"
brand_name: "ACME"
industry: "legal"
quality: "high"
image_file: "acme-proposal.png"
---

# ACME 提案

## Prompt

...

## Design Memory

- Brand: ACME
- Industry: legal
- Colors: primary=#123456

## Generated Image

![Generated image](acme-proposal.png)

## Source Attribution

- wuyoscar/gpt_image_2_skill, CC BY 4.0
- EvoLinkAI/awesome-gpt-image-2-prompts, CC BY 4.0
```

Metadata 欄位：

| 欄位 | 來源 | 必填 |
|---|---|---|
| `schema_version` | exporter constant | 是 |
| `export_type` | `"markdown"` | 是 |
| `created_at` | `datetime.now().astimezone().isoformat()` | 是 |
| `project_name` | `memory.project_name` | 否 |
| `brand_name` | `memory.brand_name` | 否 |
| `industry` | `memory.industry` | 否 |
| `quality` | `ImageEditPanel.quality_dial.quality()` | 否 |
| `image_file` | image sidecar filename | 有圖片時必填 |
| `source_attribution` | gallery prompt / manual metadata | 否 |

**決策摘要：Markdown 採 YAML frontmatter + Markdown body；圖片以 sidecar file reference，不 base64 inline。**

### 3.3 模組設計

新增：

```text
desktop/app/utils/exporters/
├── __init__.py
├── markdown_exporter.py
└── common.py              # 可選；3B 若 helper 多於 2 個再拆
```

對外 API：

```python
from pathlib import Path

from app.utils.design_memory import DesignMemory


def export_markdown(
    memory: DesignMemory | None,
    prompt: str,
    image_bytes: bytes | None,
    out_path: Path,
    *,
    quality: str | None = None,
    source_attribution: list[str] | None = None,
) -> Path:
    exporter = MarkdownExporter()
    return exporter.export(
        memory=memory,
        prompt=prompt,
        image_bytes=image_bytes,
        out_path=out_path,
        quality=quality,
        source_attribution=source_attribution,
    )
```

完整 `MarkdownExporter` class：

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from app.utils.design_memory import DesignMemory


SCHEMA_VERSION = 1


@dataclass(frozen=True)
class ExportMetadata:
    export_type: str = "markdown"
    created_at: str = field(
        default_factory=lambda: datetime.now(ZoneInfo("Asia/Taipei")).isoformat()
    )
    quality: str | None = None
    source_attribution: list[str] = field(default_factory=list)


class MarkdownExporter:
    def export(
        self,
        *,
        memory: DesignMemory | None,
        prompt: str,
        image_bytes: bytes | None,
        out_path: Path,
        quality: str | None = None,
        source_attribution: list[str] | None = None,
    ) -> Path:
        if not prompt.strip():
            raise ValueError("prompt is required")
        if out_path.suffix.lower() != ".md":
            raise ValueError("out_path must end with .md")

        out_path.parent.mkdir(parents=True, exist_ok=True)
        image_name = self._write_image_sidecar(out_path, image_bytes)
        meta = ExportMetadata(
            quality=quality,
            source_attribution=source_attribution or [],
        )
        text = self.render_markdown(
            memory=memory,
            prompt=prompt.strip(),
            image_name=image_name,
            meta=meta,
        )
        out_path.write_text(text, encoding="utf-8")
        return out_path

    def render_markdown(
        self,
        *,
        memory: DesignMemory | None,
        prompt: str,
        image_name: str | None,
        meta: ExportMetadata,
    ) -> str:
        title = memory.project_name if memory and memory.project_name else "Forma Studio Export"
        lines: list[str] = []
        lines.extend(self._frontmatter(memory, image_name, meta))
        lines.append(f"# {title}")
        lines.append("")
        lines.append("## Prompt")
        lines.append("")
        lines.append(prompt)
        lines.append("")
        lines.extend(self._memory_section(memory))
        lines.extend(self._image_section(image_name))
        lines.extend(self._attribution_section(meta.source_attribution))
        return "\n".join(lines).rstrip() + "\n"

    def _frontmatter(
        self,
        memory: DesignMemory | None,
        image_name: str | None,
        meta: ExportMetadata,
    ) -> list[str]:
        lines = [
            "---",
            f"schema_version: {SCHEMA_VERSION}",
            f'export_type: "{meta.export_type}"',
            f'created_at: "{meta.created_at}"',
        ]
        if memory and memory.project_name:
            lines.append(f'project_name: "{_yaml_escape(memory.project_name)}"')
        if memory and memory.brand_name:
            lines.append(f'brand_name: "{_yaml_escape(memory.brand_name)}"')
        if memory and memory.industry:
            lines.append(f'industry: "{_yaml_escape(memory.industry)}"')
        if meta.quality:
            lines.append(f'quality: "{_yaml_escape(meta.quality)}"')
        if image_name:
            lines.append(f'image_file: "{_yaml_escape(image_name)}"')
        lines.append("---")
        lines.append("")
        return lines

    def _memory_section(self, memory: DesignMemory | None) -> list[str]:
        if memory is None or memory.is_empty():
            return []
        lines = ["## Design Memory", ""]
        if memory.brand_name:
            lines.append(f"- Brand: {memory.brand_name}")
        if memory.industry:
            lines.append(f"- Industry: {memory.industry}")
        if memory.audience:
            lines.append(f"- Audience: {', '.join(memory.audience)}")
        if memory.color_tokens:
            lines.append("- Colors: " + ", ".join(f"{k}={v}" for k, v in memory.color_tokens.items()))
        if memory.spacing_tokens:
            lines.append("- Spacing/Layout: " + ", ".join(f"{k}={v}" for k, v in memory.spacing_tokens.items()))
        if memory.components:
            lines.append("- Components: " + "; ".join(memory.components))
        if memory.motion:
            lines.append("- Motion: " + ", ".join(f"{k}={v}" for k, v in memory.motion.items()))
        if memory.voice_signals:
            lines.append("- Voice/Copy: " + "; ".join(memory.voice_signals))
        lines.append("")
        return lines

    def _image_section(self, image_name: str | None) -> list[str]:
        if not image_name:
            return []
        return ["## Generated Image", "", f"![Generated image]({image_name})", ""]

    def _attribution_section(self, items: list[str]) -> list[str]:
        if not items:
            return []
        lines = ["## Source Attribution", ""]
        lines.extend(f"- {item}" for item in items)
        lines.append("")
        return lines

    def _write_image_sidecar(
        self,
        out_path: Path,
        image_bytes: bytes | None,
    ) -> str | None:
        if not image_bytes:
            return None
        image_path = out_path.with_suffix(".png")
        image_path.write_bytes(image_bytes)
        return image_path.name


def _yaml_escape(value: str) -> str:
    # YAML frontmatter 僅用雙引號字串，最小 escape 即可
    return value.replace("\\", "\\\\").replace('"', '\\"')
```

`__init__.py`：

```python
from app.utils.exporters.markdown_exporter import MarkdownExporter, export_markdown

__all__ = ["MarkdownExporter", "export_markdown"]
```

**決策摘要：3B exporter 提供 class + function 兩種入口；GUI 用 function，測試可直接測 class render。**

### 3.4 GUI 整合：image_edit_panel 加「匯出 Markdown」按鈕

檔案：`desktop/app/widgets/image_edit_panel.py`  
預估：2-3h  
資料來源：

| 資料 | v2.5 位置 |
|---|---|
| prompt | `self.prompt()` |
| image bytes | `self._last_result` / `last_result()` |
| design memory | `self._memory` |
| quality | `self.quality_dial.quality()` |
| parent path | file picker 由使用者選 |

新增 import：

```python
from PyQt6.QtWidgets import QFileDialog
from app.utils.exporters import export_markdown
```

新增 widget：

```python
self.export_md_btn = QPushButton("匯出 Markdown", self)
self.export_md_btn.setEnabled(False)
```

接線：

```python
def _connect_signals(self) -> None:
    self.generate_btn.clicked.connect(self._on_generate_clicked)
    self.edit_btn.clicked.connect(self._on_edit_clicked)
    self.export_md_btn.clicked.connect(self._on_export_markdown_clicked)
```

加入 button row：

```python
button_row.addWidget(self.export_md_btn)
button_row.addWidget(self.generate_btn)
button_row.addWidget(self.edit_btn)
```

生成完成後啟用：

```python
def _on_worker_finished(self, result: Any) -> None:
    if isinstance(result, ImageResult):
        self._last_result = result.data
        self.export_md_btn.setEnabled(True)
        self.status_label.setText(f"完成（{len(result.data)} bytes，session cache）")
        self.image_generated.emit(result.data)
```

Export handler：

```python
def _on_export_markdown_clicked(self) -> None:
    prompt = self.prompt()
    if not prompt:
        self._show_error("請先輸入 prompt", modal=False)
        return
    path_str, _ = QFileDialog.getSaveFileName(
        self,
        "匯出 Markdown",
        "forma-export.md",
        "Markdown (*.md)",
    )
    if not path_str:
        return
    try:
        out = export_markdown(
            self._memory,
            prompt,
            self._last_result,
            Path(path_str),
            quality=self.quality_dial.quality(),
            source_attribution=[
                "wuyoscar/gpt_image_2_skill, CC BY 4.0",
                "EvoLinkAI/awesome-gpt-image-2-prompts, CC BY 4.0",
            ],
        )
    except (OSError, ValueError) as exc:
        self._show_error(f"Markdown 匯出失敗：{exc}", modal=True)
        return
    self.status_label.setText(f"已匯出 Markdown：{out}")
```

注意：button label 不使用 emoji，避免 PyQt 字型 fallback 造成測試環境差異。

**決策摘要：Markdown export 入口放在 ImageEditPanel，先匯出目前 session 的 prompt + last image。**

### 3.5 pytest 規格（5 test）

| Test | 目的 |
|---|---|
| `test_markdown_export_requires_prompt` | 空 prompt raises `ValueError` |
| `test_markdown_export_writes_frontmatter` | frontmatter 含 schema/export_type/created_at |
| `test_markdown_export_writes_image_sidecar` | 有 image bytes 時寫同名 `.png` |
| `test_markdown_export_includes_v3_memory` | spacing/components/motion/voice 出現在 Design Memory |
| `test_image_edit_panel_export_md_button_state` | 生成前 disabled，`_last_result` 後 enabled |

Sample：

```python
def test_markdown_export_writes_image_sidecar(tmp_path: Path) -> None:
    memory = DesignMemory(project_name="ACME", brand_name="ACME")
    out = export_markdown(
        memory,
        "create a legal proposal cover",
        b"fake-png",
        tmp_path / "proposal.md",
    )
    assert out.exists()
    assert (tmp_path / "proposal.png").read_bytes() == b"fake-png"
    text = out.read_text(encoding="utf-8")
    assert 'image_file: "proposal.png"' in text
    assert "![Generated image](proposal.png)" in text
```

命令：

```bash
QT_QPA_PLATFORM=offscreen pytest desktop/tests/test_exporters.py desktop/tests/test_image_edit_panel.py -q
```

**決策摘要：Markdown exporter 以 pure function/class 測試為主，GUI 只測接線與 button state。**

### 3.6 web 版同步策略（先延後，3C 後評估）

Web 版 `OutBox` 已有 `EnhanceBtn` + `CopyBtn` 模式，可作為後續 export 入口參考：

```text
OutBox
├── label
├── hint
├── EnhanceBtn
└── CopyBtn
```

未納入 3B 的原因：

| 原因 | 說明 |
|---|---|
| Web 無本機檔案寫入 | browser download 需 Blob + anchor，與 Desktop exporter 不共用 |
| attribution 來源分散 | Web gallery prompt 已 inline JSON，但 OutBox 不一定知道 prompt source |
| v3.0 主線是 Desktop export | ImageEditPanel 已有 image bytes，較適合先落地 |

後續策略：

```text
3C 後評估
├── 是否需要 web Markdown download
├── 是否要讓 OutBox 加 ExportBtn
└── 是否抽共用 metadata schema 到 docs
```

**決策摘要：Web 版 Markdown export 延後，不阻塞 Desktop 3B。**

### 3.7 驗收與回滾

驗收：

| Gate | 預期 |
|---|---|
| 無圖片匯出 | 只寫 `.md`，不寫 `.png` |
| 有圖片匯出 | `.md` + 同名 `.png` |
| v3 memory | Markdown 包含新欄位摘要 |
| attribution | CC BY 4.0 source 出現在輸出 |
| 測試 | 5 個新增 test PASS，全部 desktop tests 不退步 |

回滾：

| 風險 | 回滾 |
|---|---|
| GUI file picker 測試不穩 | exporter 保留，暫時隱藏 button |
| Markdown 格式需調整 | 保持 `schema_version: 1`，新增欄位不破壞既有 |
| attribution 不完整 | 允許 `source_attribution=[]`，但 gallery 匯入時補齊 |

**決策摘要：3B 可在 exporter 完成後獨立發布；GUI button 可用 feature flag 控制。**

---

## 四、Sprint 3C：PDF export（M2 Phase 2，16-34h）

### 4.1 工具選擇對比

| 工具 | 優點 | 缺點 | 判斷 |
|---|---|---|---|
| reportlab | 純 Python；可控 page/layout/font；適合測試 | 學習曲線較高；需自己處理 line break | 推薦 |
| WeasyPrint | HTML→PDF；CSS 能力強 | 相依多；macOS 打包與系統 lib 風險高 | 不作首選 |
| QtPrintSupport | Qt 內建；macOS 字型原生 | 測試與 headless 穩定性較差；layout 可控性有限 | 備選 |
| browser print | 可重用 HTML | 需 Chrome/Playwright/runtime；打包重 | 不做 |

推薦：`reportlab + 中文字型（Noto Sans TC）`。

依賴策略：

```text
desktop/requirements.txt
└── reportlab==<啟動 sprint 時確認版本>

desktop/assets/fonts/
└── NotoSansTC-Regular.otf
```

注意：實作時需確認 Noto Sans TC 授權與檔案來源；若字型未放入 repo，PDF exporter 必須回友善錯誤或使用系統 fallback。

**決策摘要：PDF 採 reportlab；WeasyPrint/Chrome 不進 v3.0 MVP。**

### 4.2 layout：cover page + prompt + image + metadata + footer

PDF MVP layout：

```text
Page 1
├── Header: Forma Studio Export
├── Title: project_name or Forma Studio Export
├── Metadata table
│   ├── brand_name
│   ├── industry
│   ├── created_at
│   └── quality
├── Generated image
└── Footer: schema_version + page number

Page 2+
├── Prompt
├── Design Memory Summary
├── Source Attribution
└── Footer
```

版面規格：

| 項目 | 設定 |
|---|---|
| Page size | A4 |
| Margin | 18mm |
| Font | Noto Sans TC Regular |
| Title | 18pt |
| Heading | 12pt bold fallback，不做字重檔則用 regular |
| Body | 9.5pt |
| Prompt block | light gray background 或縮排文字 |
| Image | max width page content，max height 110mm |
| Footer | 8pt，頁碼與 export timestamp |

**決策摘要：PDF MVP 是報告附件，不是設計稿還原工具。**

### 4.3 模組設計

新增：

```text
desktop/app/utils/exporters/pdf_exporter.py
```

對外 API：

```python
def export_pdf(
    memory: DesignMemory | None,
    prompt: str,
    image_bytes: bytes | None,
    out_path: Path,
    *,
    quality: str | None = None,
    source_attribution: list[str] | None = None,
) -> Path:
    exporter = PDFExporter()
    return exporter.export(
        memory=memory,
        prompt=prompt,
        image_bytes=image_bytes,
        out_path=out_path,
        quality=quality,
        source_attribution=source_attribution,
    )
```

完整 `PDFExporter` class 樣板：

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from io import BytesIO
from pathlib import Path
from zoneinfo import ZoneInfo

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.utils.design_memory import DesignMemory


SCHEMA_VERSION = 1
FONT_NAME = "NotoSansTC"


@dataclass(frozen=True)
class PDFExportMetadata:
    created_at: str = field(
        default_factory=lambda: datetime.now(ZoneInfo("Asia/Taipei")).isoformat()
    )
    quality: str | None = None
    source_attribution: list[str] = field(default_factory=list)


class PDFExporter:
    def __init__(self, font_path: Path | None = None) -> None:
        self.font_path = font_path or _default_font_path()
        self._font_registered = False

    def export(
        self,
        *,
        memory: DesignMemory | None,
        prompt: str,
        image_bytes: bytes | None,
        out_path: Path,
        quality: str | None = None,
        source_attribution: list[str] | None = None,
    ) -> Path:
        if not prompt.strip():
            raise ValueError("prompt is required")
        if out_path.suffix.lower() != ".pdf":
            raise ValueError("out_path must end with .pdf")

        out_path.parent.mkdir(parents=True, exist_ok=True)
        self._register_font()
        meta = PDFExportMetadata(
            quality=quality,
            source_attribution=source_attribution or [],
        )

        doc = SimpleDocTemplate(
            str(out_path),
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=16 * mm,
            title=_safe_title(memory),
            author="Forma Studio",
        )
        story = self._build_story(memory, prompt.strip(), image_bytes, meta)
        doc.build(
            story,
            onFirstPage=self._draw_footer(meta),
            onLaterPages=self._draw_footer(meta),
        )
        return out_path

    def _register_font(self) -> None:
        if self._font_registered:
            return
        if not self.font_path.exists():
            raise FileNotFoundError(
                f"PDF font missing: {self.font_path}. "
                "Install or bundle NotoSansTC-Regular.otf."
            )
        pdfmetrics.registerFont(TTFont(FONT_NAME, str(self.font_path)))
        self._font_registered = True

    def _styles(self) -> dict[str, ParagraphStyle]:
        base = getSampleStyleSheet()
        return {
            "title": ParagraphStyle(
                "FormaTitle",
                parent=base["Title"],
                fontName=FONT_NAME,
                fontSize=18,
                leading=24,
                spaceAfter=10,
            ),
            "heading": ParagraphStyle(
                "FormaHeading",
                parent=base["Heading2"],
                fontName=FONT_NAME,
                fontSize=12,
                leading=16,
                spaceBefore=10,
                spaceAfter=6,
            ),
            "body": ParagraphStyle(
                "FormaBody",
                parent=base["BodyText"],
                fontName=FONT_NAME,
                fontSize=9.5,
                leading=14,
            ),
            "mono": ParagraphStyle(
                "FormaPrompt",
                parent=base["BodyText"],
                fontName=FONT_NAME,
                fontSize=9,
                leading=13,
                backColor=colors.HexColor("#f3f4f6"),
                borderPadding=6,
            ),
        }

    def _build_story(
        self,
        memory: DesignMemory | None,
        prompt: str,
        image_bytes: bytes | None,
        meta: PDFExportMetadata,
    ) -> list:
        styles = self._styles()
        story: list = []
        story.append(Paragraph(_escape(_safe_title(memory)), styles["title"]))
        story.append(self._metadata_table(memory, meta))
        story.append(Spacer(1, 8 * mm))

        if image_bytes:
            story.append(self._image_flowable(image_bytes))
            story.append(Spacer(1, 8 * mm))

        story.append(Paragraph("Prompt", styles["heading"]))
        story.append(Paragraph(_escape(prompt).replace("\n", "<br/>"), styles["mono"]))

        memory_lines = self._memory_lines(memory)
        if memory_lines:
            story.append(Paragraph("Design Memory", styles["heading"]))
            for line in memory_lines:
                story.append(Paragraph(_escape(line), styles["body"]))

        if meta.source_attribution:
            story.append(Paragraph("Source Attribution", styles["heading"]))
            for item in meta.source_attribution:
                story.append(Paragraph(_escape(f"- {item}"), styles["body"]))

        return story

    def _metadata_table(
        self,
        memory: DesignMemory | None,
        meta: PDFExportMetadata,
    ) -> Table:
        rows = [
            ["Created at", meta.created_at],
            ["Schema", f"export.v{SCHEMA_VERSION}"],
        ]
        if meta.quality:
            rows.append(["Quality", meta.quality])
        if memory and memory.brand_name:
            rows.append(["Brand", memory.brand_name])
        if memory and memory.industry:
            rows.append(["Industry", memory.industry])

        table = Table(rows, colWidths=[32 * mm, 120 * mm])
        table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#475569")),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cbd5e1")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f8fafc")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        return table

    def _image_flowable(self, image_bytes: bytes) -> Image:
        image = Image(BytesIO(image_bytes))
        max_width = A4[0] - 36 * mm
        max_height = 110 * mm
        scale = min(max_width / image.imageWidth, max_height / image.imageHeight, 1)
        image.drawWidth = image.imageWidth * scale
        image.drawHeight = image.imageHeight * scale
        return image

    def _memory_lines(self, memory: DesignMemory | None) -> list[str]:
        if memory is None or memory.is_empty():
            return []
        lines: list[str] = []
        if memory.brand_name:
            lines.append(f"Brand: {memory.brand_name}")
        if memory.color_tokens:
            lines.append("Colors: " + ", ".join(f"{k}={v}" for k, v in memory.color_tokens.items()))
        if memory.spacing_tokens:
            lines.append("Spacing/Layout: " + ", ".join(f"{k}={v}" for k, v in memory.spacing_tokens.items()))
        if memory.components:
            lines.append("Components: " + "; ".join(memory.components))
        if memory.motion:
            lines.append("Motion: " + ", ".join(f"{k}={v}" for k, v in memory.motion.items()))
        if memory.voice_signals:
            lines.append("Voice/Copy: " + "; ".join(memory.voice_signals))
        return lines

    def _draw_footer(self, meta: PDFExportMetadata):
        def draw(canvas, doc) -> None:
            canvas.saveState()
            canvas.setFont(FONT_NAME, 8)
            canvas.setFillColor(colors.HexColor("#64748b"))
            text = f"Forma Studio export.v{SCHEMA_VERSION} · {meta.created_at} · page {doc.page}"
            canvas.drawRightString(A4[0] - 18 * mm, 9 * mm, text)
            canvas.restoreState()
        return draw


def _default_font_path() -> Path:
    return Path(__file__).resolve().parents[3] / "assets" / "fonts" / "NotoSansTC-Regular.otf"


def _safe_title(memory: DesignMemory | None) -> str:
    if memory and memory.project_name:
        return memory.project_name
    return "Forma Studio Export"


def _escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
```

**決策摘要：PDF exporter 直接吃 `DesignMemory + prompt + image_bytes`，與 Markdown API 對齊。**

### 4.4 中文字型 bundling（assets/fonts/NotoSansTC-Regular.otf）

新增路徑：

```text
desktop/assets/fonts/NotoSansTC-Regular.otf
```

規則：

| 項目 | 要求 |
|---|---|
| 授權 | 實作前確認 Noto Sans TC 可隨 app bundle 散布 |
| 檔案大小 | 記錄對 `.app` 體積影響 |
| fallback | 檔案不存在時 `FileNotFoundError` 友善提示 |
| 測試 | 測試可用臨時 mock font path 或 skip font integration |

不做：

| 不做項 | 理由 |
|---|---|
| 自動下載字型 | 避免測試與 build 依賴網路 |
| 使用系統字型硬編路徑 | macOS/Windows/Linux 差異大 |
| 多字重 | MVP 只需 regular，字重用版面層級處理 |

**決策摘要：字型檔作為 app asset 管理，不在 runtime 下載。**

### 4.5 GUI 整合：image_edit_panel 加「匯出 PDF」按鈕

新增 import：

```python
from app.utils.exporters.pdf_exporter import export_pdf
```

新增 widget：

```python
self.export_pdf_btn = QPushButton("匯出 PDF", self)
self.export_pdf_btn.setEnabled(False)
```

接線：

```python
self.export_pdf_btn.clicked.connect(self._on_export_pdf_clicked)
```

生成完成後啟用：

```python
if isinstance(result, ImageResult):
    self._last_result = result.data
    self.export_md_btn.setEnabled(True)
    self.export_pdf_btn.setEnabled(True)
```

Export handler：

```python
def _on_export_pdf_clicked(self) -> None:
    prompt = self.prompt()
    if not prompt:
        self._show_error("請先輸入 prompt", modal=False)
        return
    path_str, _ = QFileDialog.getSaveFileName(
        self,
        "匯出 PDF",
        "forma-export.pdf",
        "PDF (*.pdf)",
    )
    if not path_str:
        return
    try:
        out = export_pdf(
            self._memory,
            prompt,
            self._last_result,
            Path(path_str),
            quality=self.quality_dial.quality(),
            source_attribution=[
                "wuyoscar/gpt_image_2_skill, CC BY 4.0",
                "EvoLinkAI/awesome-gpt-image-2-prompts, CC BY 4.0",
            ],
        )
    except (OSError, ValueError, FileNotFoundError) as exc:
        self._show_error(f"PDF 匯出失敗：{exc}", modal=True)
        return
    self.status_label.setText(f"已匯出 PDF：{out}")
```

建議 button row 順序：

```text
status label | 匯出 Markdown | 匯出 PDF | 生成新圖 | 修改既有圖
```

**決策摘要：PDF 與 Markdown 共用 ImageEditPanel 入口，避免另開 export page。**

### 4.6 pytest 規格（4-6 test）

| Test | 目的 |
|---|---|
| `test_pdf_export_requires_prompt` | 空 prompt raises |
| `test_pdf_export_requires_pdf_suffix` | 非 `.pdf` raises |
| `test_pdf_export_missing_font_friendly_error` | 字型缺失時友善 error |
| `test_pdf_export_writes_file` | 用測試字型或 skip 條件產出 PDF |
| `test_pdf_export_includes_v3_memory` | 透過 monkeypatch `_build_story` 或文字抽取檢查 memory lines |
| `test_image_edit_panel_export_pdf_button_state` | 生成前 disabled，完成後 enabled |

Sample：

```python
def test_pdf_export_missing_font_friendly_error(tmp_path: Path) -> None:
    exporter = PDFExporter(font_path=tmp_path / "missing.otf")
    with pytest.raises(FileNotFoundError, match="NotoSansTC-Regular.otf"):
        exporter.export(
            memory=DesignMemory(brand_name="ACME"),
            prompt="hello",
            image_bytes=None,
            out_path=tmp_path / "out.pdf",
        )
```

PDF 內容測試策略：

| 層級 | 作法 |
|---|---|
| Unit | `_memory_lines()`、`_metadata_table()` 可直接 assert |
| Integration | 有字型時實際產 PDF，assert file size > 1KB |
| Visual | 不列 v3.0 必做；若後續要做，再用 render to PNG |

命令：

```bash
QT_QPA_PLATFORM=offscreen pytest desktop/tests/test_exporters.py desktop/tests/test_image_edit_panel.py -q
```

**決策摘要：PDF 測試先驗資料與檔案產出，不做 pixel-perfect visual test。**

### 4.7 風險清單（字型授權 / PDF fidelity / 中文 line-break）

| 風險 | 等級 | 緩解 |
|---|---:|---|
| 字型授權不清 | 高 | 3C 開工第一步確認 Noto Sans TC license；不清楚則不 bundle |
| 中文 line-break 不自然 | 中 | 先接受 MVP；長 prompt 以 `<br/>` 與固定 leading 處理 |
| PDF fidelity 被誤解為設計稿還原 | 中 | UI label 與文件稱「匯出報告附件」，不稱「還原設計稿」 |
| reportlab 打包缺字型 | 中 | PyInstaller spec 加 assets/fonts；測試 missing font |
| 圖片太大記憶體壓力 | 中 | 限制 max draw size；不重編碼原圖 |

**決策摘要：PDF MVP 先把內容可靠輸出，fidelity 問題留給後續排版 sprint。**

### 4.8 驗收與回滾

驗收：

| Gate | 預期 |
|---|---|
| 無圖片 PDF | 仍可輸出 prompt + metadata |
| 有圖片 PDF | 圖片縮放在 A4 頁面內 |
| 中文 | 繁中不亂碼 |
| v3 memory | spacing/components/motion/voice 出現在 PDF |
| 測試 | PDF tests + 全部 desktop tests PASS |

回滾：

| 風險 | 回滾 |
|---|---|
| reportlab 依賴打包失敗 | 保留 Markdown，隱藏 PDF button |
| 字型檔授權未確認 | PDF exporter 暫時 raises missing font，不發正式功能 |
| 中文換行品質不足 | 降級為 Markdown-only release，PDF 留 beta flag |

**決策摘要：3C 可用 feature flag 發 beta；Markdown 不受 PDF 風險影響。**

---

## 五、Sprint 3D：Web Comment mode prototype（outline only）

### 5.1 範圍與限制（只 web HTML preview，不桌面）

範圍：

| 項目 | 狀態 |
|---|---|
| Web HTML preview pin/comment | Prototype |
| Desktop QGraphicsView pin | 不做 |
| 圖片自動 mask | 不做 |
| 多人協作 thread | 不做 |
| accept/reject snapshot | Prototype 需要 |

資料模型草案：

```json
{
  "id": "comment-001",
  "artifact_id": "draft-001",
  "target": {
    "type": "dom-element",
    "selector": "[data-fs-id='hero-cta']",
    "bbox": { "x": 0.42, "y": 0.66, "w": 0.18, "h": 0.07 }
  },
  "body": "CTA 太像廣告，改成專業語氣。",
  "status": "open"
}
```

**決策摘要：3D 只允許 Web artifact comment，不碰 Desktop image mask。**

### 5.2 技術選項

| 技術 | 作法 | 風險 |
|---|---|---|
| iframe + element picker | preview iframe 內加 `data-fs-id`，pointer events 取 bbox | 需要 artifact id 穩定 |
| 局部 prompt patch flow | comment 轉成 patch prompt，不直接覆蓋全文 | 模型可能越界 |
| feature flag | `ENABLE_COMMENT_MODE=false` 預設關閉 | 需確保關閉時零影響 |

流程：

```text
使用者點 preview element
  -> 建立 comment pin
  -> 輸入 comment
  -> buildPatchPrompt(comment, selectedHtml)
  -> model 回傳局部 patch
  -> before/after preview
  -> accept / reject / resolve
```

**決策摘要：3D 的核心驗證是「comment 能否可靠轉為局部 patch prompt」。**

### 5.3 工時估計與排期建議

| 工作 | 工時 |
|---|---:|
| preview target model | 6-10h |
| element picker | 8-12h |
| pin store + resolve state | 5-8h |
| patch prompt builder | 6-10h |
| before/after diff | 8-12h |
| tests + feature flag | 3-6h |
| 合計 | 36-58h |

啟動條件：

```text
至少 3 個實際使用者回饋：
"我知道要改哪一塊，但用文字描述太慢。"
```

**決策摘要：Comment mode 排在 3A-3C 後，需使用者回饋觸發。**

---

## 六、Sprint 3E：PPTX export spike（outline only）

### 6.1 工具選擇：python-pptx

推薦工具：`python-pptx`。

| 工具 | 優點 | 缺點 |
|---|---|---|
| python-pptx | Python 生態常用；可建立可編輯 slide | 版面 fidelity 有限 |
| browser screenshot to PPTX | 視覺接近 | 不可編輯，且依賴瀏覽器 |
| Keynote automation | macOS 友善 | 跨平台差，不適合核心 |

**決策摘要：PPTX spike 以可編輯性優先，不以截圖還原優先。**

### 6.2 3-5 種 layout 不承諾 1:1 視覺還原

Spike layout：

| Layout | 內容 |
|---|---|
| Cover | title + subtitle + brand |
| Image + Prompt | 左圖右 prompt |
| Metadata | table |
| Design Memory | token/rules summary |
| Attribution | source/license |

不承諾：

| 不承諾項 | 原因 |
|---|---|
| 1:1 PDF 視覺還原 | PowerPoint layout engine 不同 |
| 完整中文字型一致 | 使用者環境字型不可控 |
| 任意 artifact 轉 PPTX | v3.0 沒有 artifact model |

**決策摘要：PPTX 只做可編輯交付骨架，不做設計稿轉檔。**

### 6.3 工時估計與排期建議

| 工作 | 工時 |
|---|---:|
| python-pptx spike | 4-6h |
| 3-5 layout template | 8-12h |
| image fitting / crop | 3-5h |
| font/theme | 2-4h |
| tests | 3-5h |
| 合計 | 20-34h |

啟動條件：

```text
PDF/Markdown 穩定
  + 教師/行銷/顧問使用者明確要求可編輯簡報
```

**決策摘要：PPTX 是 3E spike，不阻塞 v3.0 第一版。**

---

## 七、實作順序與里程碑

### 7.1 必做順序：3A → 3B → 3C

```text
Sprint 3A
├── dataclass additive fields
├── parser/serializer warnings
├── BrandSettingsTab optional groups
├── prompt injection
└── tests

Sprint 3B
├── exporters package
├── MarkdownExporter
├── ImageEditPanel Markdown button
└── tests

Sprint 3C
├── PDFExporter
├── Noto Sans TC asset
├── ImageEditPanel PDF button
└── tests
```

**決策摘要：先穩資料模型，再做文字交付，最後做 PDF。**

### 7.2 條件做：3D 看用戶反饋

3D 不在本 sprint 必做 scope。評估點放在 3C release 後：

| 指標 | 門檻 |
|---|---|
| 局部修改抱怨 | >= 3 個真實案例 |
| PDF/Markdown 使用成功 | 無 critical bug |
| artifact preview model | 已有穩定 HTML preview 可定位 |

**決策摘要：沒有真實局部修改痛點前，不啟動 Comment mode。**

### 7.3 排程：3A (Sprint 3A) → 3B+3C (Sprint 3B) → 3D 評估點

建議排程：

| 時段 | 範圍 | 產出 |
|---|---|---|
| Sprint 3A | M1 | v3 DESIGN.md schema |
| Sprint 3B | M2 Phase 1 + 2 | Markdown + PDF export |
| Sprint 3C review | 評估 | 是否開 3D / 3E |

**決策摘要：命名上可把 3B+3C 合為 export sprint，但實作 gate 分開。**

---

## 八、共用基礎建設

### 8.1 desktop/app/utils/exporters/ 套件設計

套件：

```text
desktop/app/utils/exporters/
├── __init__.py
├── markdown_exporter.py
├── pdf_exporter.py
└── common.py
```

`common.py` 可放：

```python
def safe_export_stem(memory: DesignMemory | None, fallback: str = "forma-export") -> str: ...
def default_attribution() -> list[str]: ...
def summarize_memory(memory: DesignMemory | None) -> list[str]: ...
def ensure_suffix(path: Path, suffix: str) -> Path: ...
```

**決策摘要：先讓 Markdown/PDF API 對齊；helper 超過兩處重用才抽 common。**

### 8.2 共用 helper：file naming、image embedding、metadata 序列化

檔名規則：

```python
def safe_export_stem(memory: DesignMemory | None, fallback: str = "forma-export") -> str:
    raw = memory.project_name if memory and memory.project_name else fallback
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", raw).strip("-")
    return cleaned or fallback
```

Attribution 預設：

```python
DEFAULT_ATTRIBUTION = [
    "wuyoscar/gpt_image_2_skill, CC BY 4.0",
    "EvoLinkAI/awesome-gpt-image-2-prompts, CC BY 4.0",
]
```

**決策摘要：metadata 先用小型 helper，不新增大型 ExportModel class 除非 3E 需要。**

### 8.3 i18n 預留（zh_TW 為主）

v3.0 不導入完整 i18n。Export UI 字串集中在 widget 或 exporter 常數：

```python
TEXT_EXPORT_MARKDOWN = "匯出 Markdown"
TEXT_EXPORT_PDF = "匯出 PDF"
TEXT_EXPORT_PROMPT_REQUIRED = "請先輸入 prompt"
```

**決策摘要：zh_TW 為主，先保留集中化空間，不引入翻譯框架。**

---

## 九、與 v2.5 的相容性

### 9.1 不能破壞既有 116 條 gallery

規則：

| 項目 | 要求 |
|---|---|
| gallery JSON | 不改 schema |
| source attribution | 必須保留 |
| Web loader | 不動 `ENABLE_PROMPT_GALLERY` 行為 |
| export | 只讀 prompt/source，不回寫 gallery |

**決策摘要：Sprint 3 不改 gallery schema，只把 attribution 帶入 export。**

### 9.2 不能破壞既有 40 pytest

基線：

```bash
QT_QPA_PLATFORM=offscreen pytest desktop/tests -q
```

要求：

| 狀態 | 處理 |
|---|---|
| 既有 test fail | 先修相容性，不新增功能 |
| 新 test fail | 不合併 Sprint 3 |
| GUI test flaky | 降低 GUI assertion，保留 exporter unit test |

**決策摘要：40 PASS 是最低門檻，不用新功能換掉舊穩定性。**

### 9.3 既有 v2.5 寫的 DESIGN.md 必須能被 v3.0 parser 讀

強制測試：

```python
def test_v25_design_md_still_parses() -> None:
    memory = parse_design_memory(V25_DESIGN_MD)
    assert memory.brand_name == "ACME"
    assert memory.spacing_tokens == {}
    assert memory.components == []
    assert memory.motion == {}
    assert memory.voice_signals == []
```

**決策摘要：新欄位一律 default_factory，不得讓舊 DESIGN.md 需要 migration。**

### 9.4 feature flag 策略

建議 flags：

```text
ENABLE_DESIGN_MD_V3=true
ENABLE_EXPORT_MARKDOWN=true
ENABLE_EXPORT_PDF=false  # 3C beta 完成前維持 false
ENABLE_EXPORT_PPTX=false
ENABLE_COMMENT_MODE=false
```

實作位置可先用 module constants，不急著建立設定頁。

**決策摘要：高風險功能用 flag；schema parser 可常開，GUI/PDF 可控。**

---

## 十、風險與回滾

### 10.1 風險清單（每個 sprint 至少 3 個）

Sprint 3A：

| 風險 | 等級 | 緩解 |
|---|---:|---|
| parser 誤判 typo | 中 | warning-only，不 crash |
| GUI 過長 | 中 | collapsible group 預設收合 |
| prompt 過長 | 中 | components/voice 注入數量上限 |

Sprint 3B：

| 風險 | 等級 | 緩解 |
|---|---:|---|
| Markdown 格式後續要改 | 低 | frontmatter `schema_version` |
| 圖片 sidecar 遺失 | 中 | 同名同目錄寫入；輸出成功後 status 顯示路徑 |
| attribution 不完整 | 中 | 預設 attribution + 呼叫端可覆蓋 |

Sprint 3C：

| 風險 | 等級 | 緩解 |
|---|---:|---|
| 字型授權 | 高 | 開工第一步確認，不確認不 bundle |
| 中文 line break | 中 | MVP 接受，後續排版 sprint 再細修 |
| reportlab 打包 | 中 | PDF flag 可關，Markdown 不受影響 |

Sprint 3D：

| 風險 | 等級 | 緩解 |
|---|---:|---|
| element id 不穩 | 高 | 只支援帶 `data-fs-id` artifact |
| patch 越界 | 高 | accept 前 preview，不自動覆蓋 |
| E2E flaky | 中 | feature flag 預設關 |

Sprint 3E：

| 風險 | 等級 | 緩解 |
|---|---:|---|
| PPTX fidelity 不足 | 高 | 明確稱 spike，不承諾 1:1 |
| 字型跨平台 | 中 | 使用常見 fallback |
| layout 爆版 | 中 | 只做 3-5 固定模板 |

**決策摘要：主要風險集中在 PDF 字型與 Comment/PPTX fidelity；主線用 flag 與分期隔離。**

### 10.2 回滾策略

| 功能 | 回滾方式 |
|---|---|
| DESIGN.md v3 GUI | 隱藏 4 個 optional group，parser 保留 |
| DESIGN.md v3 parser | 回到只讀 6 區塊；v3 sections 忽略 |
| Markdown export | 隱藏 button，保留 exporter 檔案不接 UI |
| PDF export | `ENABLE_EXPORT_PDF=false`，保留 Markdown |
| Comment mode | `ENABLE_COMMENT_MODE=false` |
| PPTX | spike branch 不合併 |

回滾原則：

```text
資料相容優先
├── 不刪使用者 DESIGN.md 欄位
├── 不改 gallery
├── 不碰 API key / keyring
└── 不影響 generate/edit 主流程
```

**決策摘要：所有回滾都以不破壞 v2.5 generate/edit 與 DESIGN.md 讀取為前提。**

---

## 十一、本 PLAN 不做的事（明確 scope-out）

### 11.1 不做 nexu-io 71 systems 完整匯入

理由：

| 理由 | 說明 |
|---|---|
| 維護成本高 | 需要追上游資料與授權 |
| 品牌真實性風險 | 跨行業工具不應內建大量第三方品牌假設 |
| 與 v2.5 不同型 | Forma 目前是 prompt + image workflow，不是 design system catalog |

**決策摘要：只借 schema 子集，不搬 71 systems。**

### 11.2 不做桌面版 Comment mode（v3.0.5+）

桌面版 image comment 需要 QGraphicsView、pin layer、bbox to mask、mask preview。v2.5 已有手動 mask；自動 mask 不列 v3.0。

**決策摘要：Desktop comment/mask automation 留 v3.0.5+ 或客製案。**

### 11.3 不做 ZIP / HTML export

ZIP/HTML 需要 asset packaging 與 artifact model。v3.0 先把 Markdown/PDF 做穩。

**決策摘要：ZIP/HTML 等 export model 與 artifact preview 穩定後另案。**

### 11.4 不做 collaborative editing

多人協作需要 identity、permission、thread sync、conflict resolution，不符合 v3.0 低破壞策略。

**決策摘要：v3.0 不碰多人協作。**

### 11.5 不做 Figma / Sketch 整合

Figma/Sketch 需要外部 API、檔案格式與授權；與本 sprint 的 schema/export 主線無關。

**決策摘要：v3.0 不做設計工具整合。**
