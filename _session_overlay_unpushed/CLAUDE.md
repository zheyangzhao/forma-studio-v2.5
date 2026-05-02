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

## 工作分工規範（v2.0+ 強制要求）

### Codex 寫規格 → Claude 執行（嚴格分工）

任何 ≥ 2h 的功能改動或架構決策，**必須**走以下流程：

1. **Codex 寫規格書**（`codex exec --sandbox workspace-write -`）
   - 產出 `docs/PLAN-<feature>.md`
   - 必須含：問題分析、A/B/C 方案、Codex 推薦、§驗收清單（Playwright 步驟）、§不破壞點、§明確不做的事
   - **不寫程式碼實作**，只寫範圍、決策、驗收標準
2. **用戶看規格書後決策**
   - 選方案 A/B/C 或要求改方向
   - 確認 §待用戶確認 的決策點
3. **Claude 依規格書執行**
   - 建 git tag 還原點（≥ 5h sprint）
   - 拆 sub-task（TaskCreate）
   - 實作 + Playwright 驗證
   - JSX 檢查 + v1.1 git diff 檢查
   - commit（commit message 引用規格書與旅程驗收結果）

**為什麼這樣分工**：
- Codex 沒有對話歷史包袱，能獨立評估與否決自己（曾把 8 領域方向自己否決）
- Claude 接力執行時，用戶已對方向背書，不需邊做邊跟用戶確認
- 規格書留檔讓未來開新對話有根據

**例外**（不需走完整流程的情況）：
- 文案微調 / typo 修正 / 1 行 bug fix（< 30 分鐘）
- 用戶明確說「直接動手」「不用 Codex」
- 純 docs 更新（README / CHANGELOG）

### 違反此分工的歷史教訓

- 早期 Claude 直接動手做桌面版，用戶反饋「跟原本友善工具差十萬八千里」（commit 前期）
- 用戶後來明確要求：「請 Codex CLI 先規劃」「Codex 負責規劃再說」
- 兩次紫微斗數 / 多領域規劃，第一次 Codex 自己列 8 領域被否決，第二次重寫真正中性

## 驗收規範（v2.0+ 強制要求）

### Playwright 驗證是 **每次 commit 前的硬條件**

任何修改 `web/forma-studio-v2.html` 或相關元件的 commit，**必須**經過：

1. **JSX 語法檢查**：`node` + `@babel/parser` parse 通過
2. **v1.1 凍結驗證**：`git diff web/forma-studio.html | wc -l` 必須為 0
3. **Playwright 至少跑 1 個典型旅程**：
   - 開啟 `http://localhost:8765/forma-studio-v2.html`
   - 模擬使用者操作（輸入、點按鈕、切 tab）
   - 截圖 + console errors 檢查（必須 0 errors）
4. **改到 SmartTab / NLM / Design / Audit / Style 的核心邏輯時**，必須跑「3 旅程驗收」：
   - 牙醫場景（植牙衛教 / 病例討論）— 驗證醫療關鍵字仍正確觸發品質檢查
   - 紫微/教育場景（紫微入門課程 / 微積分教學）— 驗證不被分類成醫療
   - 一般場景（咖啡店海報 / 履歷）— 驗證 fallback 中性

### Codex CLI 規劃書必須含 Playwright 步驟

當用 Codex 寫規劃書（`codex exec`）時，prompt 必須要求 Codex 在規劃書中：

1. **§驗收清單** 章節列出 Playwright 步驟（具體的 URL、輸入、預期結果）
2. **§不破壞點** 章節明確列出哪些既有功能 Playwright 必須仍 PASS
3. **每個 sub-task** 都要有「驗收方法」欄位

範例驗收 prompt 段落：

```
請在規劃書中加入 §驗收清單：
- 步驟 1：Playwright 開啟 v2，清空 localStorage
- 步驟 2：輸入「具體測試文字」
- 步驟 3：預期看到「具體 UI 元素」
- 步驟 4：截圖檔名 `journey-X.png`，檢查 0 console errors
- 步驟 5：v1.1 git diff 必須仍為 0
```

### 動工前先建 git tag 還原點

**動工任何 ≥ 5h 的 sprint 前**，先建 git tag：

```bash
git tag -a v2.0-pre-<sprint-name> -m "<sprint> 動工前還原點"
```

萬一改壞，可以 `git reset --hard <tag>` 或 `git checkout <tag> -- web/forma-studio-v2.html`。

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
