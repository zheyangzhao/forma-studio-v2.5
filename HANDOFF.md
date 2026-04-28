# Forma Studio v2.5 · HANDOFF.md

> 每次對話結束前更新此檔。Claude Code 開新對話時先讀這裡。

---

## 目前版本狀態

| 模組 | 版本 | 狀態 |
|---|---|---|
| SDD v2.5 規格書 | ✅ 定稿 | `docs/SDD-v2.5-integration-upgrade.md`（1005 行） |
| Web 版升級（Tier 1） | 🟢 Sprint 1 完成 | gallery 66 條 + SKILL.md + craft.md + HTML loader 全到位 |
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

#### Sprint 1 verification（Sprint 1 已完成資料層 + loader，UI 接線下一步做）

**Step 6**：把 gallery 資料接到 4 區塊 UI
- 在 React 內建 `useGallery()` hook，`industries` chip 改成跨行業選項（律師 / 教師 / 會計師 / 設計 / 行銷 / ...）
- 區塊 3「製圖方式」子頁籤展示對應類別 prompts（從 FORMA_GALLERY 拉，按 industries 過濾）
- 點 prompt 後注入 textarea 作 starter
- 用 Playwright 跑 11 步互動測試（同 v1.0 的 health-check）

**Step 7**：實際 SKILL 安裝測試
- 在另一台 / 另一個 Claude Code 跑 `/plugin install forma-studio@zheyangzhao`
- 驗證 SKILL.md frontmatter 被正確讀取
- 同步 Codex `$skill-installer install` 流程

#### Sprint 2：Tier 2 PyQt6 桌面版（建議 3-4 週）

按 SDD 章節 4.1 / 4.2 / 4.3 順序：
1. `desktop/app/api/openai_client.py`：擴充 `client.images.edit()` 支援
2. `desktop/app/widgets/quality_dial.py`：成本撥盤
3. `desktop/app/widgets/reference_drop_zone.py` + `mask_uploader.py`：edit UI
4. `desktop/app/widgets/image_edit_panel.py`：整合上述三者
5. `desktop/app/utils/design_memory.py`：DESIGN.md parser
6. `desktop/app/pages/brand_settings_tab.py`：DESIGN.md GUI 編輯器

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
