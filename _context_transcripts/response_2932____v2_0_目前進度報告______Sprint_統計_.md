## v2.0 目前進度報告

### Sprint 統計（從 2026-04-29 起 12 個 commit）

| Sprint | Commit | 內容 | 狀態 |
|---|---|---|---|
| 0 | `ff8e11d` | v2 基線（複製 v1.1）| ✅ |
| 1 | `8e653f3` | 📚 提示詞庫 tab（116 條）| ✅ |
| 1.5 | `6e2c5b3` | 提示詞庫中文標題 | ✅ |
| 1.6 | `15df652` | 中文摘要 | ✅ |
| 1.7 | `284771f` | 全文中文翻譯 | ✅ |
| 1.8 | `6410190` | UX 引導 12 項 | ✅ |
| 2 | `046ec2a` | 🩺 體檢 & 增強（8 維度）| ✅ |
| 2 修補 | `065fc8b` | Audit onboarding | ✅ |
| 3 | `f4f57b7` | 🎬 風格實驗室 | ✅ |
| 4 | `0adac88` | localStorage 持久化（5 項）| ✅ |
| 5 | `a900cb7` | README + CHANGELOG | ✅ |
| B-lite | `5f97c3f` | 7→6 tab + 去醫療化 | ✅ |
| Truly-Neutral | `a692813` | 多用途中性化（11 項）| ✅ |
| **PPT Flow** | **`69d2eb8`** | **簡報企劃流程**（剛完成）| ✅ |
| Playwright 規範 | `50d6422` | CLAUDE.md 驗收規範 | ✅ 剛 commit |

### 程式碼演進
- v1.1：3,422 行（**凍結，不變**）
- v2：**5,915 行**（增 73%）
- v1.1 hash：`1bf63d1c...`（從 Sprint 0 至今 0 行 diff）

### 還原點 git tags
- `v2.0-sprint-1.8`（Sprint 1.8 完成點）
- `v2.0-pre-neutral`（Truly-Neutral 動工前）
- `v2.0-pre-ppt-flow`（PPT Flow 動工前）

### 規格文件（10 份在 docs/）
- `PLAN-v1.x-strengthening.md`（被否決的舊方向）
- `PLAN-v2.0-new-version.md`（總路線圖）
- `PLAN-sprint-4-localstorage.md`
- `PLAN-ux-guidance.md`（Sprint 1.8）
- `PLAN-architecture-review.md`（Codex×Claude，B-lite）
- `PLAN-multi-domain.md`（被否決的 8 領域）
- `PLAN-multi-domain-final.md`
- `PLAN-truly-neutral.md`（最終中性方案）
- `PLAN-ppt-flow.md`（最新）
- `CODEX-architecture-analysis.md` / `CLAUDE-user-journey-analysis.md` / `CLAUDE-medical-bias-audit.md`

---

## CLAUDE.md 新規範（commit `50d6422`）

加了 **「驗收規範」** 章節，明確要求：

1. **每次 commit 前的硬條件**（已強制執行）：
   - JSX 語法檢查（@babel/parser）
   - v1.1 git diff = 0
   - Playwright 至少跑 1 個典型旅程
   - 0 console errors

2. **改 Smart/NLM/Design/Audit/Style 核心邏輯時的「3 旅程驗收」**：
   - 牙醫場景（植牙衛教 / 病例討論）
   - 紫微/教育場景（紫微入門 / 微積分）
   - 一般場景（咖啡店 / 履歷）

3. **Codex 規劃書必須含 §驗收清單**：
   - 具體 Playwright 步驟（URL / 輸入 / 預期結果 / 截圖檔名）
   - §不破壞點
   - 每個 sub-task 含「驗收方法」

4. **動工 ≥5h sprint 前必須建 git tag 還原點**

之後叫 Codex 寫規劃書時，這些規範會被自動引用（CLAUDE.md 是 Claude Code 預設讀取的檔案）。

---

## 下一步建議

| 選項 | 內容 |
|---|---|
| **A*