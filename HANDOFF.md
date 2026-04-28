# Forma Studio v2.5 · HANDOFF.md

> 每次對話結束前更新此檔。Claude Code 開新對話時先讀這裡。

---

## 目前版本狀態

| 模組 | 版本 | 狀態 |
|---|---|---|
| SDD v2.5 規格書 | ✅ 定稿 | `docs/SDD-v2.5-integration-upgrade.md`（1005 行） |
| Web 版升級（Tier 1） | ❌ 未開始 | prompt gallery / SKILL.md / craft.md 皆待實作 |
| 桌面版升級（Tier 2） | ❌ 未開始 | edit endpoint / quality 撥盤 / DESIGN.md 待實作 |
| v3.0 觀望項（Tier 3） | ⏸ Backlog | Comment mode / 多格式匯出 |

---

## 上次做到哪裡（2026-04-28）

### v2.5 啟動完成
- 從 [`zheyangzhao/forma-studio`](https://github.com/zheyangzhao/forma-studio)（v1.0 / v1.1 凍結）拆分出本 repo
- 最小繼承：`CLAUDE.md`（已更新 v2.5）、`.gitignore`、`docs/SDD-v2.5-integration-upgrade.md`、`docs/huashu-design-SKILL.md`
- 建立目錄骨架：`web/prompt-library/`、`skills/forma-studio/references/`、`desktop/app/`
- 寫入 `README.md`、`LICENSE`（MIT）、`SKILL.md` 草稿、`craft.md` 草稿

### v1.0 凍結保護
- 原 repo 已推送至 GitHub（main + tags：`v1.0-stable`, `v1.1`, `v2.0-spec-frozen`）
- 原 `web/forma-studio.html` 與 SDD-desktop-v2.0 永久備份於凍結 repo

---

## 下次繼續

### 優先順序

按 SDD 章節七的 Sprint 規劃：

#### Sprint 1：Tier 1 Web 版升級（建議 2-3 週）

**Step 1**：篩選 `gpt_image_2_skill` 的 162 條 prompt
- 從 [上游 repo](https://github.com/wuyoscar/gpt_image_2_skill/tree/main/skills/gpt-image/references) 抓 12 個適用類別的 `gallery-*.md`
- 適用：UI/UX Mockups、Typography & Posters、Infographics、Brand Systems、Edit Endpoint Showcase、Photography、Product & Food、Data Visualization、Architecture & Interior、Technical Illustration、Cinematic & Animation
- 排除：Anime/Manga、Tattoo、Gaming HUD、Cinematic Film References
- 預期保留：50–80 條

**Step 2**：產出 `web/prompt-library/*.json`（按類別分檔）+ `gallery-index.json`
- 每筆 entry 必含 `id` / `category` / `prompt` / `size` / `quality` / `source`
- 加 `industries` 欄位標註適用行業

**Step 3**：完成 `skills/forma-studio/SKILL.md`（從草稿擴充）

**Step 4**：完成 `skills/forma-studio/references/craft.md`（合併 19 節 + #0 + 反 AI Slop + 5-10-2-8）

**Step 5**：把 v1.0 的 `web/forma-studio.html` 移植進來，加 prompt gallery 載入器（feature flag `ENABLE_PROMPT_GALLERY`）

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
