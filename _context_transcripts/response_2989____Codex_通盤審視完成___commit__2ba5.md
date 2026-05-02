## Codex 通盤審視完成 ✅（commit `2ba5f5c`，440 行）

### Codex 的核心洞察

> **v2 不是功能不足，是「缺少統一的『一個區塊一個區塊』流程語言」**。
> v1.1 Claude Design 4 區塊 glow 是你最認可的設計 DNA，應該成為 v2 主視覺語言。

### 6 tab 對 v1.1 流程精神的評分

| Tab | 分數 | 判斷 |
|---|---|---|
| 🎨 Claude Design | **10/10** | 完整 4 區塊 glow ← **應作主流程語言** |
| 📑 NotebookLM | **10/10** | 5 step + badge + arrow |
| 🎬 風格實驗室 | 6/10 | 有 ①-⑤ 但缺 active glow |
| 🖼️ 智慧製圖 | 6/10 | 缺整區 glow，更像快速入口 |
| 🩺 體檢 & 增強 | 5/10 | 診斷面板而非流程 |
| 📚 提示詞庫 | 2/10 | 資料庫式，不適合改 wizard |

### 6 對候選合併系統評估

| 對 | 推薦度 | 說明 |
|---|---|---|
| **E. Style Studio + Design Step 4** | 🟢 **最高** | Step 4 加 segmented control「手動精修 / 風格組合 / 品質檢查」 |
| A. Smart + Design | 🟢 高 | Smart 預填 Step 1-2，進 Design 落在 Step 3 active |
| C. NLM + PPT Flow | 🟢 高 | 任務=簡報製作時 Step 5 條件延伸 |
| D. 提示詞庫 + 體檢 | 🟢 高 | 卡片加「🩺 體檢這條」次要 action |
| F. Smart + NLM | 🟡 中高 | Smart 預填 NLM Step 1-4 |
| B. 體檢 + 風格 | 🟡 中 | 輕合併，Style 結果加 inline mini Grade |

### 推薦方案：B「流程化重構」（16-28h）

- 保留 6 tab + Smart 預設首頁
- **Claude Design 4 區塊作主視覺語言**（其他 tab 都向它對齊）
- Style Studio 真合併到 Step 4
- Audit 變成各 prompt 結果的品質檢查出口
- Prompt Lab 變資源庫（卡片加體檢入口）
- NLM + PPT Flow 串成簡報收尾

### 循序流程 8 條設計守則（Codex 寫的）

1. 每步只問一件事
2. **步驟名稱用動作**（避免 Prompt Lab / Audit Engine / Style Studio 系統名）
3. 每步可跳過（最後一步除外）
4. 顯示「第 N 步 / 共 M 步」
5. 跨 tab 套用必須有落地說明
6. 一般任務最多 4 步、進階最多 6 步
7. 進階選項摺疊
8. 結果頁說清楚「這是 prompt，不是成品」

---

## 三方案總比較

| 方案 | 工時 | 風險 | 用戶可感差異 | 適用情境 |
|---|---|---|---|---|
| A 保守整理 | 6-10h | 低 | 仍像 6 個工具並列，下一步更清楚 | 想快速修順 |
| **B 流程化重構** | **16-28h** | 中 | **6 個平行 tab 變成有主流程的工作台** | **「允許流程增加 + 保留循序」最佳平衡** |
| C 大刀闊斧 | 40-70h | 高 | 像新產品，老使用者可能不適 | 確認 v2 要全新主產品時 |

Codex 推薦 **B**。

---

## 你的決策（依 CLAUDE.md 工作分工規範，等你選後我才動手）

| 選擇 | 結果 |
|---|---|
| 🟢 **走 B（推薦）**16-28h | 我建 git tag → 拆 sub-task → 依 §六 §驗收清單動工 |
| A 保守整理 6-10h | 我建 tag → 動工小修 |
| C 大刀闊斧 40-70h | Codex 重新寫更詳細規劃（C 規劃書還不夠細）|
| 改方向 / 補要求 | 我重請 Codex 寫新規劃 |

完整 440 行規劃書在 `docs/PLAN-system-consolidation.md`。要先看完整文件再決定？還是直接走 B？