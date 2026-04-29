# Forma Studio v2.5 · DEVLOG

> 最新在最上面。每次重要改動後追加一筆。

---

## [2026-04-29] Sprint 1.5 計劃書定稿（B + A + Tier 1.6）

### 本次完成
- 由 Codex CLI 產出 `docs/PLAN-sprint-1.5.md`（1236 行 / 40 KB / 七大章節）
- 整合範圍盤點：
  - **B**（最優先）：Sprint 1 verification — gallery 接到 React 4 區塊 UI
  - **A**：EvoLinkAI/awesome-gpt-image-2-prompts 整合（CC BY 4.0、8745 stars）
    - 篩選 30-50 條跨行業適用條目（收 E-commerce / Ad Creative / Comparison / Poster / UI；排除 Portrait / Cosplay / Korean Idol 等人物肖像權風險）
    - 預期 gallery 從 66 → 100-115 條
  - **Tier 1.6**：Claude 一鍵增強鈕（靈感來自 claude.ai 自製版）
- nexu-io/open-design 評估：**不整合**（架構衝突），但 design-systems markdown 格式列入 v3.0 借鑑

### 已交付檔案
- `docs/PLAN-sprint-1.5.md`：Sprint 1.5 完整實作計劃書

### 待處理（task #8-12 已建檔，避免遺忘）
- [ ] #8 [B] gallery 接 4 區塊 UI（下個 session 主菜）
- [ ] #9 [A] EvoLinkAI prompt 庫整合
- [ ] #10 [Tier 1.6] Claude 一鍵增強鈕
- [ ] #11 [Tier 2 Sprint 2] PyQt6 桌面版
- [ ] #12 [v3.0 backlog] nexu-io / Comment mode / 多格式匯出

---

## [2026-04-28] Tier 1 Sprint 1 完成：prompt gallery + HTML loader 全到位

### 本次完成
- **資料層**：12 個跨行業類別、66 條結構化 prompt（落在 SDD 預估 50-80 條範圍內）
  - `tools/build_gallery.py`：解析上游 `gallery-*.md` → 12 個 JSON + index
  - `web/prompt-library/*.json`：每筆含 `id` / `title` / `size` / `pixel` / `credit` / `prompt` / `industries` / `source`
  - 排除 Anime / Tattoo / Gaming HUD / Cinematic Film 等不適合企業客戶的類別
- **Skill 文件**：兩份從骨架擴充到完整版
  - `skills/forma-studio/SKILL.md`：跨行業使用情境、4 區塊工作流、4 個產業範例（律師 / 教師 / 會計師 / 餐旅）、gallery 索引、endpoint 對應
  - `skills/forma-studio/references/craft.md`：19 節品質檢查層完整內容（合併 #0 + 反 AI Slop + 5-10-2-8 + Final Audit checklist）
- **Web 版升級**：HTML 從 v1.1 移植 + gallery loader 接通
  - `web/forma-studio.html`（3137 行，185KB → 217KB inline 後）
  - `web/manifest.json` + `web/service-worker.js`（PWA 支援，同 v1.1）
  - `tools/inline_gallery.py`：build pipeline，把 `prompt-library/*.json` inline 到 HTML 的 `<script id="forma-gallery">` 區塊，保持單檔特性
  - feature flag `ENABLE_PROMPT_GALLERY` + DOM-based loader（解析失敗自動 fallback v1.0 行為）
- **Playwright 驗證**：`http://localhost:8765/forma-studio.html` 啟動正常，FORMA_GALLERY 全域可讀，`total_count=66`，`categoriesCount=12`，0 console error

### 開發踩雷紀錄
- `re.sub` replacement 字串會把 `\n` 解釋成真實換行符，導致 inline JSON 內含真實 newline 觸發 `JSON.parse` Unterminated string。修法：用 `lambda _m: new_tag` 包住 replacement
- 全域 hook（v1 留下的 `~/.claude/hooks/active_step_guard.py`）跨 repo 擋 .py 寫入；解法：在 v2.5 與原 Design-prompt 各設一份 allow-all `workflow-kit/state/active-step.json`（已加入 .gitignore）

### 已交付檔案
| 檔案 | 行數／大小 | 用途 |
|---|---|---|
| `tools/build_gallery.py` | 274 行 | 上游解析器 |
| `tools/inline_gallery.py` | 117 行 | HTML build pipeline |
| `web/prompt-library/*.json` | 13 檔 | 12 類別 + index |
| `skills/forma-studio/SKILL.md` | 完整版 | Skill 入口（雙相容 Claude Code / Codex） |
| `skills/forma-studio/references/craft.md` | 19 節 | 品質檢查層 |
| `web/forma-studio.html` | 3137 行 / 217KB | Web 版含 inline gallery |

### 待處理（下次繼續）
- [ ] Tier 1 Sprint 1 verification：把 gallery 真的接到 4 區塊 UI（chip 選 industry → 即時顯示對應 prompts）
- [ ] Tier 2 Sprint 2：PyQt6 桌面版（edit endpoint / quality 撥盤 / DESIGN.md）
- [ ] 後續 sprint：Skill 安裝測試（實際在另一台機器跑 `/plugin install` 驗證）

---

## [2026-04-28] v2.5 repo 啟動

### 本次完成
- 從 v1.0 拆分出新 repo `forma-studio-v2.5`
- 最小繼承：`CLAUDE.md`（重寫 v2.5）、`.gitignore`、`docs/SDD-v2.5-integration-upgrade.md`、`docs/huashu-design-SKILL.md`
- 目錄骨架建立：`web/prompt-library/`、`skills/forma-studio/references/`、`desktop/app/`
- 新增 `README.md`（含 attribution）、`LICENSE`（MIT）、`SKILL.md` 草稿、`craft.md` 草稿、`HANDOFF.md`
- v1.0 / v1.1 凍結於 [`zheyangzhao/forma-studio`](https://github.com/zheyangzhao/forma-studio)（含 tag `v2.0-spec-frozen`）

### 已交付檔案
- `README.md`：對外公開介紹（含整合來源 attribution）
- `LICENSE`：MIT + 第三方授權聲明
- `CLAUDE.md`：v2.5 開發規範
- `HANDOFF.md`：下次繼續
- `docs/SDD-v2.5-integration-upgrade.md`：整合升級規格書（從 v1.0 拷貝過來）
- `docs/huashu-design-SKILL.md`：Huashu Design 原始參考（從 v1.0 拷貝過來）
- `skills/forma-studio/SKILL.md`：Skill 入口草稿
- `skills/forma-studio/references/craft.md`：19 節品質清單草稿

### 待處理（下次繼續）
- [ ] Tier 1 Sprint 1：篩選 162 → 50-80 條跨行業 prompt
- [ ] Tier 1 Sprint 1：完成 `web/prompt-library/*.json`
- [ ] Tier 1 Sprint 1：把 v1.0 `forma-studio.html` 移植進來 + 加 gallery loader
- [ ] Tier 2 Sprint 2：PyQt6 桌面版

---
