## Sprint 1.8 完成 ✅（commit `6410190`，+726 行 / -42 行）

12 項全部交付。Chrome 右半邊刷新就能看到所有變化。

### 你會在每個 tab 看到的新東西

| Tab | 新增引導 |
|---|---|
| 🎨 Claude Design | 跨 tab 套用後顯示「📥 從 📚 提示詞庫 套用 已套用「XXX」的英文 prompt → 已自動填到下方...」+ Step 4 完成卡（3 步驟貼到生圖工具）|
| 📑 NotebookLM | Step 5 兩段 OutBox 後加「先設自定義指示 → 再貼任務指令」順序卡 |
| 🖼️ 智慧製圖 | 自動分類完成後依 selSub 顯示對應下一步按鈕（image→Claude Design / nlm→NotebookLM / 等）|
| 📚 提示詞庫 | 摘要 label「（快速理解，不是要複製的 prompt）」+ 套用按鈕「→ 套用英文 prompt 到 Claude Design」|
| 🩺 體檢 & 增強 | 分數行動卡：**A** 可直接用 / **B** 補黃色 / **C/D/F** 先修紅色再重新體檢；套用按鈕區分原文 vs AI 增強版 |
| 🎬 風格實驗室 | 琥珀色「⚠️ 不是圖片」banner + 完成卡 3 步驟 + 3 動作按鈕 |
| 彩蛋 🧪 | 4 個 mode 各自顯示對應下一步（viral/ted/batch→NotebookLM / anti→體檢）|

### Codex 規劃書中提到的 4 個推論方向，全部解決
- A 截圖 vs 描述不一致 → 摘要 label 更明確
- B 按鈕 label vs 行為落差 → 所有跨 tab 按鈕加 tooltip + 來源提示卡
- C 期待出圖實際只給 prompt → 各 tab 都明示「這是 prompt 不是圖」
- D 分數沒翻成行動 → A/B/C 各有對應下一步

### v1.1 凍結契約持續
- git diff = **0 行**
- hash 仍是 `1bf63d1c...`

---

接下來要做什麼？
- **Sprint 4** — v1.1↔v2 雙向資料相容（從 PLAN-v2.0 路線圖）
- **Sprint 5** — v2 release（README 更新宣告新主版本）
- **微調修補** — 你試用後發現的具體問題
- **暫停** — 讓你先試用所有 7 個 tab 找問題