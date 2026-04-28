# Forma Studio v2.5 · CLAUDE.md

## 專案概覽

Forma Studio 是**跨行業通用** AI 提示詞生成工具——律師、會計師、教師、設計師、產品經理、行銷企劃皆可用。**不限定任何特定行業**。

**目前狀態**：v2.5 整合升級開發中。
- v1.0 / v1.1 已凍結保存於 [`zheyangzhao/forma-studio`](https://github.com/zheyangzhao/forma-studio)
- 本 repo 是 v2.5 整合升級的工作 repo（含規格書 + 實作）
- 規格書：[`docs/SDD-v2.5-integration-upgrade.md`](docs/SDD-v2.5-integration-upgrade.md)

## 技術棧

| 層 | 技術 |
|---|---|
| Web | React 18 + Babel CDN + Tailwind CSS（單一 HTML 檔，沿襲 v1.0） |
| Desktop | Python 3.12 + PyQt6 + keyring + httpx |
| Skill | Claude Code Plugin / Codex Skill 雙相容（SKILL.md 標準格式） |
| 圖像 API | OpenAI GPT Image 2（generations + edits/inpaint） |
| 文字 API | OpenAI GPT-4o-mini（智慧分析） |

## 開發規範（從 v1.0 繼承）

- 所有 React 元件**必須**定義在頂層函數，嚴禁 nested component with hooks
- 每次修改 HTML 前先用 `@babel/parser` 驗證 JSX 語法
- 中文注釋必須包在 `/* */` 內，不能是裸文字
- 完成一個功能立即 commit，格式：`feat: 說明（繁體中文）`

## v2.5 新增規範

### SKILL.md 標準格式

```markdown
---
name: forma-studio
description: <one-line 描述，給 agent 看，要說清楚何時用>
---

# Forma Studio

<完整 skill 文件>

## References
- references/gallery.md
- references/craft.md
```

### Prompt Gallery 條目格式

每個 prompt entry（JSON / Markdown）必須含：

```json
{
  "id": "ui-ux-001",
  "category": "UI/UX Mockups",
  "prompt": "<prompt text>",
  "size": "portrait",
  "quality": "high",
  "source": "gpt_image_2_skill (CC BY 4.0)",
  "industries": ["legal", "education", "marketing", "general"]
}
```

`source` 欄位為**必填**，吸收自外部專案的條目要保留授權標註。

### DESIGN.md 共享記憶（桌面版 Tier 2）

每個專案資料夾下放一份 `DESIGN.md`，存品牌 tokens：

```markdown
# Brand Identity
- name: <品牌名>
- industry: <行業>
- audience: <主要受眾>

# Color Tokens
- primary: oklch(...)
- secondary: oklch(...)

# Typography
- heading: <font>
- body: <font>

# Tone of Voice
- <風格描述>
```

桌面版會把 DESIGN.md 解析後注入 system prompt，跨對話共用。

## 對話開始時的例行確認

1. 讀 [`HANDOFF.md`](HANDOFF.md) 「下次繼續」區塊
2. 讀 [`DEVLOG.md`](DEVLOG.md) 最新 3 筆
3. 確認本次目標屬於 Tier 1 / Tier 2 / Tier 3 哪個範圍
4. 跨 Tier 工作前先檢查 SDD 章節七的順序

## 對話結束前的例行動作

1. 寫入 [`DEVLOG.md`](DEVLOG.md)
2. git commit（若有修改），commit message 用繁體中文
3. 更新 [`HANDOFF.md`](HANDOFF.md) 的「下次繼續」區塊
4. 若是 Tier 完成節點，打 git tag（例如 `v2.5-tier1-complete`）

## 重要路徑

| 路徑 | 用途 |
|---|---|
| `docs/SDD-v2.5-integration-upgrade.md` | 整合升級規格書（1005 行） |
| `docs/huashu-design-SKILL.md` | Huashu Design 原始 SKILL（v1.0 繼承） |
| `web/forma-studio.html` | Web 版主檔（待從 v1.0 移植 + 升級） |
| `web/prompt-library/*.json` | 跨行業 prompt gallery（Tier 1 待產出） |
| `skills/forma-studio/SKILL.md` | Claude Code / Codex 安裝入口（Tier 1） |
| `skills/forma-studio/references/craft.md` | 19 節 prompt 品質清單（Tier 1） |
| `desktop/main.py` | 桌面版入口（Tier 2 待從 v1.0 移植 + 升級） |
| `desktop/app/widgets/*.py` | edit endpoint / quality 撥盤（Tier 2 新增） |

## API Key 規範

### Web 版
- 從 `ApiCtx` 讀取（`useContext(ApiCtx)`）
- session state，**不寫 localStorage、不寫檔**
- 不允許 hardcode

### 桌面版
- 絕對不能 hardcode API Key
- 使用 `keyring` 存系統鑰匙圈（macOS Keychain / Windows Credential Manager）
- service: `"Forma Studio"`
- account: `"openai_api_key"`
- 不寫進 git，`.env*` / `secrets.json` / `config.local.*` 已在 `.gitignore`

## v1.0 / v2.5 並行原則

- v1.0 在 [`zheyangzhao/forma-studio`](https://github.com/zheyangzhao/forma-studio) 凍結，不再變更
- v2.5 在本 repo 開發
- 兩者**共享規格書精神**（4 區塊 glow 流程、20 設計哲學、12 設計品牌）
- v2.5 不是改寫 v1.0，是**擴充**：加 prompt gallery、加 SKILL.md、加桌面版 edit endpoint
