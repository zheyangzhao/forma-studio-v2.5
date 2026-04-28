# Forma Studio · SDD v2.5 整合升級規格書

**專案名稱**：Forma Studio
**版本**：v2.5 Integration Upgrade
**基準**：Web `v1.0-stable` + Desktop `SDD v2.0`
**日期**：2026-04-27
**平台**：Web 單檔版 + PyQt6 Desktop（macOS / Windows）
**技術棧**：React 18 + Tailwind CDN · Python 3.12 + PyQt6 + keyring + httpx · OpenAI GPT-4o-mini + GPT Image 2
**原則**：跨行業通用、BYOK、保留既有 4 區塊 glow 流程、只新增能力不移除既有設計哲學與品牌參考

---

## 一、整合升級概覽

### 1.1 為什麼做這次升級

Forma Studio 已從 O2Win Prompt Studio 通用化，定位改為跨行業 AI prompt 生成工具。v1.0-stable 已完成 Web 版 4 區塊 glow 流程，但目前 prompt gallery、Skill 安裝格式、圖像 edit endpoint、成本控制與品牌記憶仍缺少系統化規格。

本次 v2.5 整合兩個來源的可落地能力：

| 來源 | 可吸收能力 | 放入版本 | 原因 |
|---|---|---:|---|
| `gpt_image_2_skill` | 162 條結構化 prompt、SKILL.md、craft.md、OpenAI image endpoint 包裝、quality 預算撥盤 | Tier 1 / Tier 2 | 可直接補齊 Web prompt library 與 Skill 版安裝格式 |
| `open-codesign` | 多 Provider BYOK、Comment mode、AI sliders、DESIGN.md、匯出管線 | Tier 2 / Tier 3 | DESIGN.md 與 edit workflow 可先落地；Comment mode 與匯出先評估 |

核心目標：
- Web 版新增跨行業 prompt gallery，不替換既有「20 種設計哲學」與「12 個設計品牌」。
- 將 Forma Studio 封裝成 Claude Code / Codex 可安裝的 `SKILL.md`。
- 桌面版補齊 GPT Image 2 edits endpoint、quality 成本撥盤、`DESIGN.md` 專案記憶。
- 保持 API Key BYOK，不 hardcode，不寫入 repo。

### 1.2 目標差異表（現況 v1.0 → 升級後 v2.5）

| 面向 | 現況 v1.0-stable | v2.5 目標 | 主要檔案 |
|---|---|---|---|
| Prompt 來源 | Web 內建 chips / styles / philosophies | 新增 50-80 條通用商務 gallery | `web/prompt-library/*.json` |
| Skill 格式 | 無正式 `skills/forma-studio/SKILL.md` | Claude Code / Codex 雙相容 | `skills/forma-studio/SKILL.md` |
| Prompt 品質檢查 | 反 AI Slop、#0 事實驗證、5-10-2-8 分散在 Huashu 內容 | 合併成 Prompt 品質檢查層 | `skills/forma-studio/references/craft.md` |
| Web 圖像 API | generations 為主 | Web 保持 generations；edit 規劃進桌面版 | `web/forma-studio.html` |
| Desktop 圖像 API | 規劃中，純文字生圖 | generations + edits / inpaint | `desktop/app/api/openai_client.py` |
| 成本控制 | `standard/high` 顯示不完整 | `low/medium/high` 三段式成本估算 | `desktop/app/widgets/quality_dial.py` |
| 品牌記憶 | 每次輸入 chips / textarea | 專案層 `DESIGN.md` | `<project>/DESIGN.md` |
| Comment mode | 無 | v3.0 backlog 評估 | 不在 v2.5 實作 |
| 多格式匯出 | 複製 prompt 文字 | v3.0 backlog 評估 HTML/PDF/PPTX/ZIP/MD | 不在 v2.5 實作 |

### 1.3 不做哪些事（明確 scope out）

| 項目 | 狀態 | 原因 |
|---|---|---|
| 不改 Web 主流程 | Scope out | v1.0 的 4 區塊 glow 流程已穩定，本次只擴充資料與 Skill 格式 |
| 不導入 Electron | Scope out | Desktop 既定方向是 PyQt6，不切換技術棧 |
| 不做多 Provider BYOK | Scope out | v2.5 仍以 OpenAI 為唯一實作 Provider；多 Provider 可列 v3.x |
| 不做 Comment mode | Backlog | 需要 DOM hit-test、局部 prompt patch、preview selection，實作量高 |
| 不做多格式匯出 | Backlog | 需要 HTML render、local Chrome、PPTX 產生、ZIP packaging |
| 不收 Anime / Tattoo / Gaming HUD | Scope out | 不適合企業客戶主場景，且人物與風格權利風險較高 |
| 不實作 prompt library 實際內容於本規格階段 | Scope out | 本文件只定義結構、篩選規則與驗收標準 |

---

## 二、整合來源與授權

### 2.1 gpt_image_2_skill (CC BY 4.0) 對照

| 來源能力 | 原專案資訊 | Forma Studio 對應 | Tier |
|---|---|---|---|
| 162 條 prompt | 28 類結構化 prompt | 篩出 50-80 條跨行業通用商務子集 | Tier 1 |
| `references/gallery.md` | gallery 路由索引 | 拆為 Web JSON 與 Skill markdown 索引 | Tier 1 |
| `references/craft.md` | 19 節 prompt 寫作清單 | 合併反 AI Slop、#0、5-10-2-8 | Tier 1 |
| `references/openai-cookbook.md` | OpenAI 官方範例整理 | 僅保留 endpoint 與 multipart 範例引用 | Tier 2 |
| CLI generations | `POST /v1/images/generations` | Web 與 Desktop 純文字生圖 | Tier 1 / 2 |
| CLI edits | `POST /v1/images/edits` | Desktop edit / inpaint | Tier 2 |
| `--quality` | `low` / `medium` / `high` | Desktop quality 預算撥盤 | Tier 2 |
| size shortcut | `1k` / `2k` / `4k` / `portrait` / `landscape` / `square` / `wide` / `tall` | Web gallery metadata + Desktop dropdown | Tier 1 / 2 |
| SKILL.md 標準格式 | Claude Code / Codex 可安裝 | `skills/forma-studio/SKILL.md` | Tier 1 |

授權處理：

```text
Source: gpt_image_2_skill
License: CC BY 4.0
URL: https://github.com/wuyoscar/gpt_image_2_skill
Adaptation: Prompt examples filtered and rewritten for Forma Studio cross-industry business use.
```

### 2.2 open-codesign (MIT) 對照

| 來源能力 | 原專案資訊 | Forma Studio 對應 | Tier |
|---|---|---|---|
| Electron 桌面 App | 多 Provider BYOK | 暫不採 Electron；保留 BYOK 原則 | Scope out |
| 12 design skill modules | design workflow 模組化 | 參考 `SKILL.md` 任務分流，不直接搬程式碼 | Tier 1 |
| 15 demos | 可視化 demo | 可轉成 gallery metadata 的 future sample | Backlog |
| Comment mode | 點 preview 元素留 pin，模型只重寫該區域 | v3.0 評估 | Tier 3 |
| AI-tuned sliders | 模型 emit color / spacing / font controls | 可在 Desktop v3.0 做 prompt tuning panel | Tier 3 |
| `DESIGN.md` | 品牌 tokens 可編輯共享記憶 | Desktop 專案記憶 | Tier 2 |
| 5 種匯出 | HTML / PDF / PPTX / ZIP / Markdown | v3.0 評估 | Tier 3 |
| Agentic Design | workspace + permissioned loop | 不列 v2.5 | Scope out |

授權處理：

```text
Source: open-codesign
License: MIT
URL: https://github.com/OpenCoworkAI/open-codesign
Adaptation: DESIGN.md memory pattern and UX concepts referenced in Forma Studio SDD.
```

### 2.3 attribution 與 license 標註方式

所有從 `gpt_image_2_skill` 改寫的 prompt gallery 條目必須保留 attribution。Web JSON 與 Skill markdown 使用同一組欄位，避免兩邊不同步。

```json
{
  "id": "ui-dashboard-executive-001",
  "category": "UI/UX Mockups",
  "title": "Executive Dashboard Mockup",
  "industry_fit": ["law", "accounting", "education", "marketing", "product", "consulting"],
  "prompt_template": "Create a production-quality executive dashboard...",
  "size_shortcut": "wide",
  "recommended_quality": "high",
  "source": {
    "name": "gpt_image_2_skill",
    "license": "CC BY 4.0",
    "url": "https://github.com/wuyoscar/gpt_image_2_skill",
    "adaptation": "Filtered and rewritten for Forma Studio cross-industry business use."
  }
}
```

Skill markdown 範例：

```markdown
## Executive Dashboard Mockup

- Category: UI/UX Mockups
- Recommended quality: high
- Size: wide
- Source: gpt_image_2_skill (CC BY 4.0)

Prompt:
Create a production-quality executive dashboard...
```

---

## 三、Tier 1：Web 版立即升級

### 3.1 prompt gallery 通用商務子集（含篩選清單表）

Web v1.0 的既有資料繼續保留：

| 既有能力 | 狀態 | v2.5 處理 |
|---|---|---|
| 20 種設計哲學 | 保留 | gallery 可引用 `philosophy_hint`，不覆蓋 |
| 12 個設計品牌 | 保留 | gallery 可引用 `brand_reference_hint`，不覆蓋 |
| 4 區塊 glow 流程 | 保留 | gallery 作為 Section 3 / Section 4 的補充入口 |
| 圖像風格 chips | 保留 | gallery 條目可預填 style chips |

篩選規則：

| 類別 | v2.5 處理 | 建議數量 | 用途 |
|---|---|---:|---|
| UI/UX Mockups | 保留 | 8-12 | SaaS、內部系統、客戶入口、報表頁 |
| Typography & Posters | 保留 | 6-8 | 活動海報、公告、課程宣傳 |
| Infographics & Field Guides | 保留 | 8-10 | 教學圖、流程圖、產業解釋 |
| Brand Systems & Identity | 保留 | 6-8 | 品牌準則、識別延展、名片/社群素材 |
| Edit Endpoint Showcase | 保留 | 6-8 | 換色、換字、多圖融合、局部修改案例 |
| Photography | 保留 | 4-6 | 專業人物外的場景攝影、空間、產品 |
| Product & Food | 保留 | 4-6 | 商品展示、包裝、菜單、型錄 |
| Data Visualization | 保留 | 5-7 | 商業指標、研究結果、年度報告 |
| Architecture & Interior | 保留 | 3-5 | 空間提案、辦公室、展場 |
| Technical Illustration | 保留 | 4-6 | 架構圖、零件圖、流程機制 |
| Cinematic & Animation | 保留但限非名人 | 3-4 | 品牌影片分鏡、動態視覺概念 |
| Anime & Manga | 排除 | 0 | 企業客戶使用率低 |
| Tattoo Design | 排除 | 0 | 主產品定位不涵蓋 |
| Gaming HUD | 排除 | 0 | 與通用商務 prompt 不匹配 |
| Cinematic Film References | 排除 | 0 | 人物肖像權、導演風格與 IP 風險 |

建議檔案切分：

```
web/prompt-library/
├── gallery-index.json
├── ui-ux-mockups.json
├── typography-posters.json
├── infographics-field-guides.json
├── brand-systems-identity.json
├── edit-endpoint-showcase.json
├── photography.json
├── product-food.json
├── data-visualization.json
├── architecture-interior.json
├── technical-illustration.json
└── cinematic-animation.json
```

Web 讀取策略：

```javascript
const GALLERY_BASE = './prompt-library/';

async function loadPromptGallery(categoryId) {
  const index = await fetch(`${GALLERY_BASE}gallery-index.json`).then(r => r.json());
  const item = index.categories.find(c => c.id === categoryId);
  if (!item) throw new Error(`Unknown gallery category: ${categoryId}`);
  return fetch(`${GALLERY_BASE}${item.file}`).then(r => r.json());
}
```

資料 schema：

```typescript
type GalleryPrompt = {
  id: string;
  category: string;
  title: string;
  business_use: string;
  industry_fit: string[];
  prompt_template: string;
  variables: Array<{ name: string; label: string; required: boolean; default?: string }>;
  recommended_size: '1k' | '2k' | '4k' | 'portrait' | 'landscape' | 'square' | 'wide' | 'tall';
  recommended_quality: 'low' | 'medium' | 'high';
  source: {
    name: 'gpt_image_2_skill';
    license: 'CC BY 4.0';
    url: string;
    adaptation: string;
  };
};
```

### 3.2 SKILL.md 化（含 frontmatter 範例）

新 Skill 目錄規格：

```
skills/forma-studio/
├── SKILL.md
└── references/
    ├── gallery.md
    ├── gallery-ui-ux.md
    ├── gallery-infographics.md
    ├── gallery-brand-systems.md
    ├── gallery-edit-endpoint.md
    └── craft.md
```

`SKILL.md` frontmatter：

```markdown
---
name: forma-studio
description: 跨行業 AI prompt 生成工具。用於律師、會計師、教師、設計師、商業企劃、行銷與產品經理的圖像生成、設計稿、資訊圖表、品牌資產整理與反 AI Slop prompt 品質檢查。
metadata:
  short-description: Cross-industry prompt studio for image, design, infographic, and brand prompt generation.
---
```

Skill 主體必須提供 4 區塊 agent workflow：

| Web 區塊 | Skill 章節 | Agent 行為 |
|---|---|---|
| Section 1 描述需求 | `## Step 1 · 需求描述` | 要求使用者提供任務、素材、輸出格式、限制 |
| Section 2 受眾基調 | `## Step 2 · 受眾與基調` | 提取受眾、情緒、品牌限制、素材狀態 |
| Section 3 製圖方式 | `## Step 3 · 製圖方式` | 在圖像生成、原型、資訊圖表、品牌資產中選一個 workflow |
| Section 4 風格生成 | `## Step 4 · 風格與輸出` | 套用品牌、哲學、quality、size、平台參數 |

安裝指令範例：

```bash
# Claude Code plugin flow
/plugin marketplace add <user>/forma-studio
/plugin install forma-studio@<user>

# Codex skill-installer flow
$skill-installer install https://github.com/<user>/forma-studio/tree/main/skills/forma-studio
```

Skill 內 reference 路由：

```markdown
## References

- Use `references/gallery.md` when the user asks for prompt examples or category routing.
- Use `references/craft.md` before final prompt output.
- Use `references/gallery-edit-endpoint.md` only when the task involves existing images, reference images, or masks.
```

### 3.3 craft.md 19 節整合（含合併後章節清單）

`craft.md` 不是單純搬運，必須合併三層規則：

| 規則來源 | 合併位置 | 優先級 |
|---|---|---:|
| gpt_image_2_skill `craft.md` 19 節 | Prompt 寫作清單主體 | P2 |
| Huashu Design #0 事實驗證 | 第 0 節，所有具體產品/人物/版本前置 | P0 |
| 反 AI Slop | 視覺品質與風格約束 | P1 |
| 5-10-2-8 品質門檻 | 素材採集與品牌資產 | P1 |

合併後章節清單：

| # | 章節 | 必填輸出 |
|---:|---|---|
| 0 | 事實驗證先於假設 | 是否需要 WebSearch、待驗證項目 |
| 1 | 任務意圖 | image / edit / infographic / prototype / brand |
| 2 | 受眾與使用場景 | audience、channel、decision context |
| 3 | 核心訊息 | one-sentence message |
| 4 | 內容素材 | user-provided assets / missing assets |
| 5 | 品牌資產優先級 | Logo / product / UI / color / font |
| 6 | 5-10-2-8 門檻 | search count、candidate count、selected assets |
| 7 | 構圖與版面 | grid、hierarchy、negative space |
| 8 | typography | font role、scale、line-height |
| 9 | color system | oklch / HEX / contrast |
| 10 | material and lighting | photography / 3D / illustration constraints |
| 11 | image endpoint | generations / edits / mask |
| 12 | reference images | image count、role、priority |
| 13 | text rendering | 中文文字、海報、infographic 品質提高 |
| 14 | anti AI Slop | 禁紫漸變、emoji 圖標、generic card wall |
| 15 | accessibility | contrast、readability、mobile crop |
| 16 | output size | size shortcut + pixel target |
| 17 | quality and budget | low / medium / high |
| 18 | negative constraints | watermark、fake UI、unreadable text |
| 19 | final prompt audit | 檢查缺漏、輸出最終 prompt |

`craft.md` gate 範例：

```markdown
## Final Prompt Audit

Before output, check:
- [ ] If specific brand/product/version is mentioned, verification step is explicit.
- [ ] Logo/product/UI asset priority is stated.
- [ ] Anti AI Slop constraints are concrete, not generic.
- [ ] Quality level and estimated cost are visible.
- [ ] Size shortcut maps to a real API size.
- [ ] Source attribution is preserved for gallery-derived prompts.
```

---

## 四、Tier 2：PyQt6 桌面版功能擴充

### 4.1 edit / inpaint endpoint（含 UI 草圖 ASCII + API 範例）

功能範圍：

| 能力 | 規格 |
|---|---|
| 多參考圖 | 最多 4 張，PNG/JPEG/WebP，送出前轉 multipart |
| mask | 可選 PNG alpha mask；透明區域代表要修改的區域 |
| 按鈕 | `生成新圖` 與 `修改既有圖` 分開，避免誤送 endpoint |
| 使用情境 | 換色、換文字、多圖融合、品牌 logo 套產品圖、局部重繪 |
| 儲存 | 輸出 PNG bytes，先存 session cache，不自動覆蓋原檔 |

PyQt6 元件新增：

```
desktop/app/widgets/
├── reference_drop_zone.py    # 最多 4 張 reference images
├── mask_uploader.py          # 可選 PNG alpha mask
└── image_edit_panel.py       # endpoint 切換與送出按鈕
```

UI 草圖：

```
┌─ 圖像生成 / 修改 ───────────────────────────────────────────┐
│ Prompt                                                      │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ 請把這張既有海報改成深色版本，保留標題階層與品牌 Logo... │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                            │
│ Reference Images（最多 4 張）                              │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│ │ drop #1  │ │ drop #2  │ │ drop #3  │ │ drop #4  │        │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
│                                                            │
│ Mask（選填，PNG alpha）                                    │
│ ┌────────────────────────────┐ [上傳 mask] [清除]          │
│ │ no mask: whole image edit  │                            │
│ └────────────────────────────┘                            │
│                                                            │
│ Quality  [草稿 low] [探索 medium] [交付 high]              │
│                                                            │
│                         [生成新圖] [修改既有圖]             │
└────────────────────────────────────────────────────────────┘
```

API client 規格：

```python
# desktop/app/api/openai_client.py
async def edit_image(
    self,
    prompt: str,
    images: list[Path],
    mask: Path | None = None,
    size: str = "1024x1024",
    quality: str = "medium",
) -> bytes:
    files = []
    for idx, image_path in enumerate(images[:4]):
        files.append(("image[]", (image_path.name, image_path.read_bytes(), "image/png")))
    if mask:
        files.append(("mask", (mask.name, mask.read_bytes(), "image/png")))

    data = {
        "model": "gpt-image-2",
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "response_format": "b64_json",
    }

    resp = await self._client.post(
        f"{self.BASE_URL}/images/edits",
        headers={"Authorization": f"Bearer {self._key}"},
        data=data,
        files=files,
    )
    resp.raise_for_status()
    payload = resp.json()
    return base64.b64decode(payload["data"][0]["b64_json"])
```

錯誤處理：

| 錯誤 | UI 顯示 | 行為 |
|---|---|---|
| 無 reference image | `修改既有圖需要至少 1 張參考圖` | 阻擋送出 |
| 超過 4 張 | `最多 4 張，請移除多餘圖片` | 阻擋送出 |
| mask 非 PNG | `mask 必須是 PNG alpha` | 阻擋送出 |
| API 413 | `圖片太大，請縮小到 2048px 內再試` | 不重試 |
| API 401 | `API Key 無效或已過期` | 開啟 Key 設定 |

### 4.2 quality 預算撥盤（含成本表）

三段式 quality：

| UI Label | API quality | 單張估算成本 | 用途 | 預設 |
|---|---|---:|---|---|
| 草稿 | `low` | `$0.005` | 快速草圖、構圖探索 | 否 |
| 探索 | `medium` | `$0.04` | 一般 prompt 測試、方向比較 | 是 |
| 交付 | `high` | `$0.17` | 中文文字、海報、infographic、客戶交付圖 | 條件自動 |

PyQt6 元件：

```python
# desktop/app/widgets/quality_dial.py
from dataclasses import dataclass

@dataclass(frozen=True)
class QualityOption:
    key: str
    label: str
    usd_per_image: float
    description: str

QUALITY_OPTIONS = [
    QualityOption("low", "草稿", 0.005, "快速構圖與方向測試"),
    QualityOption("medium", "探索", 0.04, "一般品質與成本平衡"),
    QualityOption("high", "交付", 0.17, "文字、海報、資訊圖與交付圖"),
]
```

成本顯示公式：

```python
def estimate_image_cost(n: int, quality: str) -> float:
    unit = {
        "low": 0.005,
        "medium": 0.04,
        "high": 0.17,
    }[quality]
    return round(n * unit, 3)
```

UI 顯示：

```
Quality: 探索 medium
Images: 3
Estimated cost: 3 × $0.04 = $0.12
```

自動升級規則：

```python
HIGH_QUALITY_TRIGGERS = [
    "中文", "繁體", "海報", "poster", "infographic",
    "資訊圖", "報表", "圖表", "文字清晰", "可讀文字"
]

def suggest_quality(prompt: str, current: str) -> tuple[str, str]:
    text = prompt.lower()
    if current != "high" and any(k.lower() in text for k in HIGH_QUALITY_TRIGGERS):
        return "high", "偵測到中文文字、海報或資訊圖需求，建議改用交付 high。"
    return current, ""
```

### 4.3 DESIGN.md 共享記憶（含 schema 範例）

每個專案資料夾可有一份 `DESIGN.md`。Desktop 讀取該檔，將品牌 tokens 注入 system prompt，不依賴模型記憶。

新增檔案規格：

```
desktop/app/pages/
└── brand_settings_tab.py      # DESIGN.md GUI 編輯器

desktop/app/utils/
└── design_memory.py           # parse / validate / save DESIGN.md
```

`DESIGN.md` schema：

```markdown
# <Project Name> · DESIGN.md
> Updated: 2026-04-27
> Owner: <name/team>
> Source of truth: user editable file

## Brand Identity
- Brand name: Forma Studio
- Industry: Cross-industry AI prompt generation
- Audience: lawyers, accountants, teachers, designers, marketers, PMs
- Tone of voice: precise, practical, calm, no marketing fluff

## Color Tokens
| Token | Value | Usage |
|---|---|---|
| --brand-bg | oklch(20% 0.04 260) | app background |
| --brand-surface | oklch(28% 0.04 260) | cards and panels |
| --brand-accent | oklch(86% 0.16 95) | active glow and CTA |
| --brand-text | oklch(96% 0.01 260) | primary text |

## Typography
- Display: Noto Serif TC
- Body: Noto Sans TC
- Mono: JetBrains Mono

## Visual Rules
- Keep information hierarchy visible before decoration.
- Use real brand assets when available.
- Avoid purple-blue gradient, generic emoji icons, fake SaaS cards, unreadable microtext.

## Prompt Defaults
- Default language: zh-TW
- Default size: 1024x1024
- Default quality: medium
- Escalate to high when prompt includes Chinese text, poster, or infographic.

## Negative Constraints
- no watermark
- no fake logo
- no unreadable UI text
- no generic AI slop composition
```

解析後 Python 結構：

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

注入 system prompt：

```python
def build_system_prompt(base: str, memory: DesignMemory | None) -> str:
    if not memory:
        return base
    return f"""{base}

Project DESIGN.md memory:
- Brand: {memory.brand_name}
- Industry: {memory.industry}
- Tone: {memory.tone_of_voice}
- Colors: {memory.color_tokens}
- Typography: {memory.typography}
- Visual rules: {memory.visual_rules}
- Negative constraints: {memory.negative_constraints}
"""
```

---

## 五、Tier 3：觀望項目（v3.0 評估）

### 5.1 Comment mode 評估

Comment mode 目標：使用者點 preview 任一元素，留下 pin 與修改指令，模型只重寫該區域。

v3.0 前置需求：

| 能力 | 需要元件 | 風險 |
|---|---|---|
| Preview hit-test | WebView / Canvas / DOM mapping | PyQt6 原生 preview 不一定有 DOM |
| Pin storage | `comments.json` 或專案 metadata | 需和輸出版本綁定 |
| 局部 prompt patch | region prompt builder | 模型可能改到非指定區域 |
| 差異比對 | before / after screenshot | 需額外 render pipeline |

建議 v3.0 schema：

```json
{
  "id": "pin-001",
  "target": {
    "type": "image-region",
    "x": 0.24,
    "y": 0.31,
    "width": 0.18,
    "height": 0.12
  },
  "comment": "把這個 CTA 改成更克制的專業語氣，保留位置。",
  "status": "open",
  "created_at": "2026-04-27T10:00:00+08:00"
}
```

### 5.2 多格式匯出評估

目前 v1.0 只有複製 prompt。v3.0 可評估輸出：

| 格式 | 用途 | 可能工具 | 風險 |
|---|---|---|---|
| HTML（內聯 CSS） | 可分享原型與單頁設計 | Jinja2 / template builder | 需要 CSS sanitizer |
| PDF | 客戶交付、提案 | local Chrome / Playwright | 打包體積與跨平台 |
| PPTX | 簡報交付 | python-pptx | 圖文排版 fidelity |
| ZIP | 完整素材包 | stdlib `zipfile` | 路徑與授權 metadata |
| Markdown | 文件與 prompt handoff | plain text writer | 格式最穩，價值較低 |

v2.5 只預留 export interface，不實作：

```python
class Exporter(Protocol):
    def export(self, project: ProjectState, output: Path) -> Path:
        ...
```

---

## 六、目錄結構變動

### 6.1 before（v1.0）

現有 repo 主要結構：

```
Design-prompt/
├── CLAUDE.md
├── HANDOFF.md
├── DEVLOG.md
├── docs/
│   ├── SDD-web-v6.md
│   ├── SDD-desktop-v1.1.md
│   ├── SDD-desktop-v2.0.md
│   └── huashu-design-SKILL.md
├── web/
│   ├── forma-studio.html
│   ├── manifest.json
│   └── service-worker.js
└── desktop/
    ├── main.py
    └── requirements.txt
```

### 6.2 after（v2.5）

v2.5 規劃後結構：

```
Design-prompt/
├── docs/
│   └── SDD-v2.5-integration-upgrade.md
├── web/
│   ├── forma-studio.html
│   └── prompt-library/
│       ├── gallery-index.json
│       ├── ui-ux-mockups.json
│       ├── typography-posters.json
│       ├── infographics-field-guides.json
│       ├── brand-systems-identity.json
│       ├── edit-endpoint-showcase.json
│       ├── photography.json
│       ├── product-food.json
│       ├── data-visualization.json
│       ├── architecture-interior.json
│       ├── technical-illustration.json
│       └── cinematic-animation.json
├── skills/
│   └── forma-studio/
│       ├── SKILL.md
│       └── references/
│           ├── gallery.md
│           ├── gallery-ui-ux.md
│           ├── gallery-infographics.md
│           ├── gallery-brand-systems.md
│           ├── gallery-edit-endpoint.md
│           └── craft.md
└── desktop/
    └── app/
        ├── api/
        │   └── openai_client.py
        ├── pages/
        │   └── brand_settings_tab.py
        ├── utils/
        │   └── design_memory.py
        └── widgets/
            ├── reference_drop_zone.py
            ├── mask_uploader.py
            ├── image_edit_panel.py
            └── quality_dial.py
```

### 6.3 新增資料夾與檔案清單

| 路徑 | Tier | 類型 | 說明 |
|---|---:|---|---|
| `docs/SDD-v2.5-integration-upgrade.md` | Spec | Markdown | 本規格書 |
| `web/prompt-library/` | 1 | JSON data | Web prompt gallery |
| `skills/forma-studio/SKILL.md` | 1 | Skill | Claude Code / Codex 安裝入口 |
| `skills/forma-studio/references/gallery*.md` | 1 | Skill refs | Skill prompt gallery |
| `skills/forma-studio/references/craft.md` | 1 | Skill refs | Prompt 品質檢查層 |
| `desktop/app/widgets/reference_drop_zone.py` | 2 | PyQt6 widget | 參考圖拖放 |
| `desktop/app/widgets/mask_uploader.py` | 2 | PyQt6 widget | PNG alpha mask |
| `desktop/app/widgets/image_edit_panel.py` | 2 | PyQt6 widget | edit endpoint 面板 |
| `desktop/app/widgets/quality_dial.py` | 2 | PyQt6 widget | 成本撥盤 |
| `desktop/app/pages/brand_settings_tab.py` | 2 | PyQt6 page | DESIGN.md 編輯器 |
| `desktop/app/utils/design_memory.py` | 2 | Utility | DESIGN.md parse / save / validate |

---

## 七、實作順序與里程碑

### 7.1 Sprint 1（Tier 1，估時 1 週）

| Day | 任務 | 輸出 | 驗收 |
|---:|---|---|---|
| 1 | 建立 gallery 篩選表 | 50-80 條候選清單 | 排除類別無漏收 |
| 2 | 建立 Web JSON schema | `web/prompt-library/*.json` | JSON parse 全通過 |
| 3 | Web gallery loader | Section 3 / 4 可載入範例 | 不破壞既有 flow |
| 4 | 建立 `skills/forma-studio/SKILL.md` | Skill 可讀、frontmatter 正確 | Claude / Codex 安裝格式符合規範 |
| 5 | 建立 `craft.md` | 19 節 + #0 + anti-slop + 5-10-2-8 | Prompt audit checklist 完整 |

Sprint 1 指令：

```bash
# 驗證 JSON
python -m json.tool web/prompt-library/gallery-index.json >/tmp/gallery-index.ok

# 驗證 Skill frontmatter
python - <<'PY'
from pathlib import Path
p = Path('skills/forma-studio/SKILL.md')
text = p.read_text(encoding='utf-8')
assert text.startswith('---')
assert 'name: forma-studio' in text
assert 'description:' in text
print('SKILL.md OK')
PY
```

### 7.2 Sprint 2（Tier 2，估時 2 週）

| 週 | 任務 | 輸出 | 驗收 |
|---:|---|---|---|
| 2-1 | `images/edits` client | `OpenAIClient.edit_image()` | mock multipart body 正確 |
| 2-1 | reference / mask widgets | drag-drop + PNG mask validation | 超過 4 張會阻擋 |
| 2-1 | image edit panel | `生成新圖` / `修改既有圖` 分流 | endpoint 不混用 |
| 2-2 | quality dial | 成本估算 + auto high suggestion | 中文/海報/infographic 觸發提示 |
| 2-2 | DESIGN.md memory | parse / save / system prompt injection | GUI 編輯後可讀回 |
| 2-2 | integration tests | pytest + pytest-qt | 不碰 Keychain 真 Key |

Sprint 2 測試指令：

```bash
pytest desktop/tests/test_openai_client.py -q
pytest desktop/tests/test_quality_dial.py -q
pytest desktop/tests/test_design_memory.py -q
pytest desktop/tests/test_image_edit_panel.py -q
```

### 7.3 驗收節點

| 節點 | 條件 | 負責檢查 |
|---|---|---|
| T1-A Gallery | 50-80 條，全部有 source attribution | 人工 review + JSON schema |
| T1-B Web | 既有 4 區塊流程可完成一次 prompt 生成 | Playwright |
| T1-C Skill | `SKILL.md` frontmatter 可被 installer 辨識 | CLI dry run |
| T1-D Craft | 最終 prompt 會跑 audit checklist | 單元測試 prompt fixture |
| T2-A Edits | 1-4 張圖 + optional mask 可送 multipart | mock server |
| T2-B Quality | 成本公式正確，auto high 有提示不強制 | widget test |
| T2-C DESIGN.md | GUI 編輯後 system prompt 注入 | integration test |

---

## 八、相容性與資料遷移

### 8.1 既有 Web v1.0 用戶遷移路徑

Web v1.0 不需要資料庫遷移，因為目前狀態主要存在 runtime state。v2.5 只新增外部 gallery data。

| 項目 | v1.0 | v2.5 | 遷移方式 |
|---|---|---|---|
| 使用者輸入 | session state | session state | 無需遷移 |
| API Key | session state，不存 localStorage | session state | 無需遷移 |
| 設計哲學 | HTML 內建 | HTML 內建 + gallery hint | 保持原 constant |
| 設計品牌 | HTML 內建 | HTML 內建 + gallery hint | 保持原 constant |
| prompt library | 無 | JSON fetch | 新增 loader，fetch 失敗時隱藏 gallery |

Web fallback：

```javascript
async function safeLoadGallery(categoryId) {
  try {
    return await loadPromptGallery(categoryId);
  } catch (err) {
    console.warn('Prompt gallery unavailable:', err);
    return [];
  }
}
```

### 8.2 SKILL.md 與 Web 並行的同步策略

同步原則：Web JSON 是結構化來源，Skill markdown 是人類可讀與 agent 可讀版本。兩者以 `id` 對齊。

| 資料 | Source of truth | 產物 |
|---|---|---|
| prompt gallery metadata | `web/prompt-library/*.json` | `skills/forma-studio/references/gallery*.md` |
| prompt 品質規則 | `skills/forma-studio/references/craft.md` | Web 可摘錄 checklist |
| 4 區塊 workflow | `web/forma-studio.html` + `SKILL.md` | 兩邊人工同步 |

建議同步檢查：

```bash
python - <<'PY'
import json
from pathlib import Path

ids = set()
for path in Path('web/prompt-library').glob('*.json'):
    if path.name == 'gallery-index.json':
        continue
    data = json.loads(path.read_text(encoding='utf-8'))
    for item in data:
        if item['id'] in ids:
            raise SystemExit(f"duplicate id: {item['id']}")
        ids.add(item['id'])

md = Path('skills/forma-studio/references/gallery.md').read_text(encoding='utf-8')
missing = [i for i in ids if i not in md]
if missing:
    raise SystemExit(f"missing in skill gallery: {missing[:5]}")
print(f"sync OK: {len(ids)} prompts")
PY
```

---

## 九、測試與驗收標準

### 9.1 Tier 1 done criteria

| 項目 | 標準 | 驗證方式 |
|---|---|---|
| Gallery 數量 | 50-80 條 | script count |
| Gallery 類別 | 只包含保留類別 | JSON schema + category allowlist |
| Attribution | 每筆都有 `Source: gpt_image_2_skill (CC BY 4.0)` | script assert |
| Web 不破壞 | 4 區塊 glow 可完成一次生成 | Playwright |
| Skill frontmatter | `name` / `description` 存在 | text assert |
| Skill references | `gallery.md`、`craft.md` 可路由 | text assert |
| craft 整合 | 20 節（#0 + 1-19）完整 | heading count |
| 既有資料 | 20 philosophies、12 brands 未移除 | grep / unit fixture |

Tier 1 測試範例：

```bash
python - <<'PY'
import json
from pathlib import Path

allowed = {
    "UI/UX Mockups", "Typography & Posters", "Infographics & Field Guides",
    "Brand Systems & Identity", "Edit Endpoint Showcase", "Photography",
    "Product & Food", "Data Visualization", "Architecture & Interior",
    "Technical Illustration", "Cinematic & Animation"
}

count = 0
for path in Path('web/prompt-library').glob('*.json'):
    if path.name == 'gallery-index.json':
        continue
    data = json.loads(path.read_text(encoding='utf-8'))
    for item in data:
        assert item['category'] in allowed
        assert item['source']['name'] == 'gpt_image_2_skill'
        assert item['source']['license'] == 'CC BY 4.0'
        count += 1
assert 50 <= count <= 80, count
print(f'gallery OK: {count}')
PY
```

### 9.2 Tier 2 done criteria

| 項目 | 標準 | 驗證方式 |
|---|---|---|
| Edits endpoint | multipart 包含 `image[]` 與 optional `mask` | mock server |
| Reference images | 最多 4 張，0 張阻擋 edit | pytest-qt |
| Mask validation | 只接受 PNG alpha | unit test |
| Quality dial | low/medium/high 成本正確 | unit test |
| Auto high suggestion | 中文、海報、infographic 觸發提示 | unit test |
| DESIGN.md parse | schema 欄位可讀入 dataclass | unit test |
| DESIGN.md GUI | 編輯、儲存、重開可讀回 | pytest-qt |
| Key safety | 不 print、不 log、不寫入 QSettings | grep + code review |

Tier 2 測試 fixture：

```python
def test_estimate_image_cost():
    assert estimate_image_cost(1, "low") == 0.005
    assert estimate_image_cost(3, "medium") == 0.12
    assert estimate_image_cost(2, "high") == 0.34

def test_suggest_quality_for_zh_poster():
    q, msg = suggest_quality("繁體中文活動海報，標題需清晰", "medium")
    assert q == "high"
    assert "建議" in msg
```

---

## 十、風險與回滾

### 10.1 風險清單（每個 Tier 至少 2 個風險）

| Tier | 風險 | 影響 | 緩解 |
|---:|---|---|---|
| 1 | gallery 條目授權標註遺漏 | CC BY 4.0 attribution 不完整 | schema 必填 `source`，CI assert |
| 1 | gallery 變成取代既有哲學/品牌 | 破壞 v1.0 使用習慣 | UI 文案寫「範例庫」，資料層不改既有 constants |
| 1 | prompt 類別過多導致 Web 單檔變慢 | 首屏載入延遲 | lazy fetch JSON，不 inline 到 HTML |
| 1 | Skill 與 Web prompt 不同步 | 同一 prompt 兩版輸出不同 | `id` 對齊與 sync script |
| 2 | GPT Image 2 edits multipart 格式變動 | API 呼叫失敗 | client 隔離在 `openai_client.py`，mock 測試 body |
| 2 | mask 語意使用者不理解 | 修改區域錯誤 | UI 顯示 alpha mask 說明與預覽 |
| 2 | high quality 成本累積過快 | 使用者 API 費用不可控 | 送出前顯示估算成本，不自動強制升級 |
| 2 | DESIGN.md 內容過長 | system prompt token 過高 | parse 後只注入摘要欄位，限制檔案大小 |
| 3 | Comment mode 實作量超過預期 | Sprint 延誤 | v2.5 不實作，只保留 schema |
| 3 | 多格式匯出 fidelity 不穩 | 客戶交付品質不可控 | 先做 Markdown/HTML，再評估 PDF/PPTX |

### 10.2 回滾策略

Tier 1 回滾：

| 問題 | 回滾方式 |
|---|---|
| Web gallery loader 造成錯誤 | 關閉 gallery feature flag，保留原 4 區塊流程 |
| JSON prompt library 有問題 | 移除 `web/prompt-library/` fetch，HTML 不受影響 |
| Skill 安裝格式錯誤 | 修正 `skills/forma-studio/SKILL.md` frontmatter，不影響 Web |
| craft.md 規則過嚴 | 將 audit 從 blocking 改 warning |

Feature flag：

```javascript
const ENABLE_PROMPT_GALLERY = true;
```

Tier 2 回滾：

| 問題 | 回滾方式 |
|---|---|
| edits endpoint 不穩 | 隱藏 `修改既有圖` 按鈕，只保留 generations |
| quality 撥盤有成本誤導 | 改顯示「估算」並預設 medium |
| DESIGN.md parse 失敗 | 忽略 DESIGN.md，使用原 prompt builder |
| PyQt6 widget 造成 crash | 在 page 初始化時 lazy import，失敗則降級 |

Desktop 降級範例：

```python
try:
    from app.widgets.image_edit_panel import ImageEditPanel
    EDITS_ENABLED = True
except Exception:
    EDITS_ENABLED = False
```

回滾驗收：

```bash
# Web：關閉 gallery 後仍可生成 prompt
rg "ENABLE_PROMPT_GALLERY = false" web/forma-studio.html

# Desktop：edits disabled 後 app 可啟動
python desktop/main.py
```
