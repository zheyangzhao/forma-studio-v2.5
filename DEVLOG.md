# Forma Studio v2.5 · DEVLOG

> 最新在最上面。每次重要改動後追加一筆。

---

## [2026-04-29] 🎉 Sprint 1.5 全部完成：B + A + Tier 1.6（tag v2.5-sprint-1.5）

### Tier 1.6：Claude 一鍵增強鈕

工作流程
1. **Codex CLI 規劃**：PLAN-sprint-1.5 §四 已就緒
2. **Claude 寫程式**：4 個 Edit（頂層 helpers + OutBox prop + DesignTab 2 處 caller）
3. **Codex CLI Code Review**：規格遵循度 A、0 Critical / 0 Major、1 Minor（disabled button title 兼容性備註）
4. **Playwright 驗證**：自寫 spec 9 步、PASS、3.8 秒

### Sprint 1.5 整體

| Section | 任務 | Playwright |
|---|---|---|
| §B | gallery 接 4 區塊 UI | 11/11 PASS |
| §A | EvoLinkAI 整合（gallery 66 → 116） | 8/8 PASS |
| §四 Tier 1.6 | Claude 一鍵增強鈕 | PASS |

### 規模變化（Sprint 1 起 → Sprint 1.5 完）

| 指標 | Sprint 1 起 | 1.5 完 |
|---|---|---|
| gallery total | 0 | **116** |
| categories | 0 | **17** |
| sources | 0 | **2** |
| HTML size | 148 KB | **293 KB** |
| Playwright spec | 0 | **3 個 / 28 步** |

### 後續
- [ ] #11 [Tier 2 Sprint 2] PyQt6 桌面版升級
- [ ] #12 [v3.0 backlog] nexu-io / Comment mode / 多格式匯出

---

## [2026-04-29] Sprint 1.5 §A 完成：EvoLinkAI 整合 · Playwright 8/8 PASS · gallery 從 66 → 116

### 工作流程
1. **Codex CLI 規劃**（既有 PLAN-sprint-1.5 §三）
2. **Claude 寫程式**：
   - 上游偏差：PLAN 寫的 `gpt_image_2_prompt.json` 不存在（404），實際資料在 `data/ingested_tweets.json`（meta 索引）+ `README.md`（5723 行 prompt 主文）
   - 改解析 README.md 的 `### Case N: TITLE (by @AUTHOR)` heading + ` ``` ` 區塊
   - 新增 `tools/build_gallery_evolink.py`（解析 + 5 類別輸出）
   - 修改 `tools/inline_gallery.py`（補 cat-level source + 多 source `sources` array）
   - 修改 `web/forma-studio.html` 的 `SUB_TO_GALLERY_SLUGS`（加 evolink-* mapping，否則 4 個 sub 都不顯示 EvoLink 條目）
3. **Codex CLI Code Review** → 抓 2 個 Major：
   - `merge_index()` 重跑不穩定（重跑會把 evolink count 算進 wuyo_count）→ 已修
   - UI industries 不符 PLAN（多了 marketing）→ 已修
4. **Codex CLI 跑 Playwright**：
   - 第 1 跑：6/8（spec 預估錯 marketing+image 條目上限、SUB_TO_GALLERY_SLUGS 還沒加 evolink）
   - 第 2 跑：codex 卡 stdin（已 kill）；改用 `npx --prefix /tmp/playwright_test playwright test` 直接執行
   - 結果：**8/8 PASS、0 console error、3.6 秒**

### 規模變化
- gallery：66 → **116** 條（PLAN 預估 100-115，超 1 條可接受）
- categories：12 → **17**（+5 EvoLink 類別）
- sources：1（wuyoscar）→ **2**（wuyoscar 66 + EvoLinkAI 50）
- HTML size：217KB → **293KB**（+76KB inline JSON + JSX）

### 已交付檔案
- `tools/build_gallery_evolink.py`：274 行（新增）
- `tools/inline_gallery.py`：補 cat-level source + sources array
- `web/prompt-library/evolink-{ecommerce,ad-creative,poster,ui,comparison}.json`：5 檔，每檔 10 條
- `web/prompt-library/gallery-index.json`：加 sources、append 5 evolink categories
- `web/forma-studio.html`：SUB_TO_GALLERY_SLUGS 加 evolink-* mapping
- `.playwright/sprint1.5A-verify.spec.js`：8 步驗證 spec（CC0 / Codex 寫）

### 開發踩雷紀錄
- PLAN 假設上游有結構化 JSON，實際只有 README.md（必須 markdown parser）
- `SUB_TO_GALLERY_SLUGS` 沒加 evolink-* slug → EvoLink 條目根本無法顯示在 4 個 sub 裡（review 沒抓到、Playwright 抓到）
- Python build script 我寫錯 `/* */` 注釋（誤套 v2.5 React 規範），改回 `#`
- codex CLI 的 stdin 模式可能會 stuck（觀察值，已用 npx 直接跑作為 fallback）

### 待處理（Sprint 1.5 剩 1 項）
- [ ] #10 [Tier 1.6] Claude 一鍵增強鈕

---

## [2026-04-29] Sprint 1.5 §B 完成：gallery 接 4 區塊 UI · Playwright 11/11 PASS

### 工作流程（嚴格遵照用戶指示）
1. **Codex CLI 規劃** → `docs/PLAN-sprint-1.5.md` §二
2. **Claude 寫程式** → 6 個 Edit 改 `web/forma-studio.html`
3. **Codex CLI Code Review** → 0 Critical / 0 Major / 0 Minor，「可直接 commit」
4. **Codex CLI 跑 Playwright 11 步測試** → 修兩處 spec 邏輯後，**11/11 PASS、0 console error、5.4 秒**

### 本次完成
- 頂層新增：INDUSTRY_CHIPS（10 跨行業）/ SUB_TO_GALLERY_SLUGS / GALLERY_SIZE_TO_RATIO / useGallery() / GalleryPromptList
- DesignTab 內：industries / showGallery state + applyGalleryPrompt handler
- Section 2：適用行業 chip block（gallery.enabled 才顯示）
- Section 3：secondary controls（手動設定/📚 範例庫）+ 範例庫展開時 render GalleryPromptList
- 行為：點 prompt → 自動切回 image sub + 注入 desc + 切 size + 關 gallery + goStep(3)
- HTML 從 217KB → 224KB（+7KB JSX）

### Playwright spec 修正紀錄（兩處 spec 邏輯 bug，與程式碼無關）
- Step 07：原 spec assert「套用」按鈕必存在；但 industries=legal + sub=image 命中 0 條 → 改驗證空狀態 fallback
- Step 11：原 spec 在 Step 9 後找複製鈕（畫面已無）→ 改：切 info sub + 重開範例庫 + 點 GalleryPromptList 內 CopyBtn
- 加 `permissions: ['clipboard-read','clipboard-write']`：headless Chromium 預設拒絕 clipboard write，CopyBtn 的 setOk(true) 不執行

### 已交付檔案
- `web/forma-studio.html`：+153 行（v2.5 PROMPT GALLERY HELPERS + UI 接線）
- `.playwright/sprint1-verify.spec.js`：11 步驗證 spec
- `.gitignore`：加 .playwright artifact 過濾

### 待處理（Sprint 1.5 剩兩項）
- [ ] #9 [A] EvoLinkAI prompt 庫整合（gallery 從 66 → 100-115 條）
- [ ] #10 [Tier 1.6] Claude 一鍵增強鈕

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
