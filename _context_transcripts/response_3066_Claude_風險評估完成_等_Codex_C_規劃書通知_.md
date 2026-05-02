Claude 風險評估完成。等 Codex C 規劃書通知。

---

## 我寫的 Claude 風險評估摘要

### 結論：**C 不該做，推薦 B+**

### 4 個矛盾把 C 推回 B

| 矛盾 | 說明 |
|---|---|
| 1. wizard vs 4 區塊 | 線性 wizard 失去整體預覽 / 4 區塊式 wizard = 既有 Design |
| 2. 6 tab vs 跨 tab wizard | 4 種實作策略 C-A 跟 B 重疊、C-B 違反規則、C-C 破壞性、C-D 風險最大 |
| 3. Prompt Lab 不適合 wizard | Codex 自己評 2/10 |
| 4. NLM 已 10/10 wizard | C 重做會打架 |

### Claude 推薦 B+（B 16-28h + 4-6h = **20-34h**）

在 Codex B 方案上加 1 個關鍵點：**Smart 升級為「4 區塊 glow 風格」線性 wizard**。

進入 Smart 同時顯示 4 區塊：
1. 說明需求（active glow）
2. 確認 AI 建議（dimmed）
3. 選擇路徑（dimmed）— 直接複製 / 進 Design / 送體檢 / 進 NLM
4. 取得結果（dimmed）

讓使用者一進來就知道「**做完只要 4 步、結果是 prompt 不是圖**」。

### 給 Codex 的 5 個討論問題（等它規劃出來對比）

1. Codex 會不會自己否決 C？（看 §八 誠實判斷）
2. Codex 怎麼處理 Prompt Lab 矛盾？
3. C-D 取代 Design 是升級還是重做？
4. C 工時 40-70h 能否分段交付？
5. 與 v1.1 差距會多大？

---

**目前狀態**：
- ✅ Claude 風險評估 commit 中（`docs/CLAUDE-c-risk-audit.md`）
- ⏳ Codex C 詳細規劃在背景跑（task `bngrjiurw`）
- ⏳ 等 Codex 通知 → 合併規劃書 → 給你決策

我等 Codex 完。