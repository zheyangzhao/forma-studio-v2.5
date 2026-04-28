# Forma Studio v2.5 · DEVLOG

> 最新在最上面。每次重要改動後追加一筆。

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
