# Forma Studio v2.5 · HANDOFF.md

> 每次對話結束前更新此檔。Claude Code 開新對話時先讀這裡。

---

## 目前版本狀態

| 模組 | 版本 | 狀態 |
|---|---|---|
| SDD v2.5 規格書 | ✅ 定稿 | `docs/SDD-v2.5-integration-upgrade.md`（1005 行） |
| Web 版升級（Tier 1 + Tier 1.5） | 🟢 **Sprint 1.5 全部完成** | gallery **116** 條 + SKILL.md + craft.md + HTML loader + UI 接線 + AI 增強鈕（28 步 Playwright 全 PASS、tag `v2.5-sprint-1.5`）|
| 桌面版升級（Tier 2） | ❌ 未開始 | edit endpoint / quality 撥盤 / DESIGN.md 待實作 |
| v3.0 觀望項（Tier 3） | ⏸ Backlog | Comment mode / 多格式匯出 |

---

## 上次做到哪裡（2026-04-28）

### Tier 1 Sprint 1 完成
- **資料層**：`web/prompt-library/` 12 個 JSON、66 條 prompt（schema 含 industries / source / size / pixel）
- **Skill 文件**：`skills/forma-studio/SKILL.md` 完整版 + `references/craft.md` 19 節品質檢查層
- **Web 版**：`web/forma-studio.html` 從 v1.1 移植 + gallery loader 接通（feature flag `ENABLE_PROMPT_GALLERY=true`）
- **Build 工具**：`tools/build_gallery.py`（上游解析）+ `tools/inline_gallery.py`（HTML 注入）
- **Playwright 驗證**：FORMA_GALLERY 全域可讀、0 error
- 詳見 `DEVLOG.md` 最新一筆

### v2.5 啟動完成（更早）
- 從 [`zheyangzhao/forma-studio`](https://github.com/zheyangzhao/forma-studio)（v1.0 / v1.1 凍結）拆分出本 repo
- 最小繼承策略：CLAUDE.md（重寫 v2.5）、.gitignore、SDD-v2.5、huashu-design-SKILL.md

### v1.0 凍結保護
- 原 repo 已推送至 GitHub（main + tags：`v1.0-stable`, `v1.1`, `v2.0-spec-frozen`）
- 原 README 已加 v2.5 pointer
- 原 `web/forma-studio.html` 與 SDD-desktop-v2.0 永久備份於凍結 repo

---

## 下次繼續

### 優先順序

#### Sprint 1.5（已有完整計劃書：[`docs/PLAN-sprint-1.5.md`](docs/PLAN-sprint-1.5.md)）

按計劃書章節順序：

**B（最優先）**：Sprint 1 verification — gallery 接到 React 4 區塊 UI（task #8）
- `useGallery()` hook + industries chip 過濾 + 區塊 3「📚 範例庫」子分頁 + 點 prompt 注入 textarea + Playwright 11 步測試
- 詳見 PLAN-sprint-1.5 §二

**A**：EvoLinkAI 整合（task #9）
- 抓 `gpt_image_2_prompt.json` + 篩選 30-50 條跨行業適用 + `tools/build_gallery_evolink.py`
- 預期 gallery 從 66 → 100-115 條
- 詳見 PLAN-sprint-1.5 §三

**Tier 1.6**：Claude 一鍵增強鈕（task #10）
- 在 prompt 輸出旁加「✨ AI 增強」鈕，呼叫 GPT-4o-mini 套 craft.md §19 audit
- 詳見 PLAN-sprint-1.5 §四

**Sprint 1.5 收尾**：tag `v2.5-sprint-1.5`、commit、push

#### Sprint 2：Tier 2 PyQt6 桌面版（task #11，建議 3-4 個 session）

按 SDD-v2.5 章節 4 順序：
1. `desktop/app/api/openai_client.py`：擴充 `client.images.edit()` 支援
2. `desktop/app/widgets/quality_dial.py`：成本撥盤
3. `desktop/app/widgets/reference_drop_zone.py` + `mask_uploader.py`：edit UI
4. `desktop/app/widgets/image_edit_panel.py`：整合上述三者
5. `desktop/app/utils/design_memory.py`：DESIGN.md parser
6. `desktop/app/pages/brand_settings_tab.py`：DESIGN.md GUI 編輯器

#### v3.0 backlog（task #12，目前不實作）

- 借鑑 nexu-io/open-design 的 design-systems markdown 格式（擴充既有 12 個品牌庫）
- Comment mode（點元素改局部）
- 多格式匯出（HTML / PDF / PPTX / ZIP / Markdown）
- 整碗端走 nexu-io **不適合**（架構衝突，Vite + Express daemon vs 單檔 HTML / PyQt6）

#### 後續延伸

- 實際 SKILL 安裝測試：在另一台機器跑 `/plugin install forma-studio@zheyangzhao` 驗證
- 同步 Codex `$skill-installer install` 流程

#### Sprint 2：Tier 2 PyQt6 桌面版（建議 3-4 週）

按 SDD 章節 4.1 / 4.2 / 4.3 順序：
1. `desktop/app/api/openai_client.py`：擴充 `client.images.edit()` 支援
2. `desktop/app/widgets/quality_dial.py`：成本撥盤
3. `desktop/app/widgets/reference_drop_zone.py` + `mask_uploader.py`：edit UI
4. `desktop/app/widgets/image_edit_panel.py`：整合上述三者
5. `desktop/app/utils/design_memory.py`：DESIGN.md parser
6. `desktop/app/pages/brand_settings_tab.py`：DESIGN.md GUI 編輯器

---

## 關鍵決策記錄

| 日期 | 決策 | 原因 |
|---|---|---|
| 2026-04-28 | v2.5 拆分為新 repo（不在 v1.0 上覆寫） | 保護 v1.0 穩定版本，新 repo 可放手大改 |
| 2026-04-28 | v2.5 採 MIT license | 與整合來源（CC BY 4.0 / MIT）相容，最寬鬆 |
| 2026-04-28 | 最小繼承策略（不複製 v1.0 web/desktop 實作） | 避免半成品污染，從規格書重新開始 |
| 2026-04-28 | 排除 Anime/Tattoo/Gaming HUD 類 prompt | 不適合企業客戶，且人物權利風險高 |
| 2026-04-28 | v2.5 採跨行業通用定位 | 用戶明確指示「不指示醫療用，希望各行各業都方便用」 |

---

## 凍結 repo 連結

- [v1.0-stable](https://github.com/zheyangzhao/forma-studio/tree/v1.0-stable)：Web 4 區塊 glow 流程穩定版
- [v1.1](https://github.com/zheyangzhao/forma-studio/tree/v1.1)：v1.0 + PWA + 重命名為 forma-studio.html
- [v2.0-spec-frozen](https://github.com/zheyangzhao/forma-studio/tree/v2.0-spec-frozen)：SDD-desktop-v2.0.md 規格定稿（v2.5 實作起點）
