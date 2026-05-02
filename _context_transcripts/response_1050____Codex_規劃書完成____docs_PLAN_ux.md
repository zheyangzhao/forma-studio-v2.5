## Codex 規劃書完成 ✅
`docs/PLAN-ux-guidance.md` 413 行。摘要給你：

### Q1「下一步該怎麼辦」：7 個 tab 結尾都缺完成卡
| Tab | 現況問題 | 補什麼 |
|---|---|---|
| 🎨 Claude Design | 產出 prompt 後沒說「這是 prompt 不是圖、要貼到生圖工具」 | 完成卡 |
| 📑 NotebookLM | 兩個 OutBox 不知哪段先貼 | 貼上順序卡 |
| 🖼️ 智慧製圖 | 自動分類後沒引導去對應 tab | 「前往 Claude Design / NLM」按鈕 |
| 📚 提示詞庫 | 套用後跳 tab 但不說目的地 | 改按鈕「套用英文 prompt 到 Claude Design 圖像描述欄」 |
| 🩺 體檢 & 增強 | 低分不知怎麼修、高分不知能做什麼 | 分數行動卡（A 可套用 / B 補黃色 / C 修紅色）|
| 🎬 風格實驗室 | 看似要出圖、實際只給 prompt | 「這是 prompt，不是圖片」明示 |
| 彩蛋 🧪 | 各實驗孤立 | mode-based 下一步 |

### Q2「圖示與結論落差」：4 推論方向都成立
- **A** 截圖 vs 描述不一致 ✅ — 折疊卡只見第一層中文，要展開才看到完整三層
- **B** 按鈕 label vs 實際行為落差 ✅ — 「套用到 Claude Design」沒說會跳 tab + 填到哪
- **C** 「自動組好的英文 prompt」vs 期待看到圖 ✅ — Smart / Style / Design 都讓人以為會直接出圖
- **D** Audit 分數沒翻成行動 ✅ — 看到 56/C 不知道是好是壞、先改哪裡

### 12 個小修補（總計 ~6h）

| # | 改什麼 | 工時 |
|---|---|---|
| 1 | 共用元件加 `NextStepCard` | 0.5-1h |
| 2 | DesignTab Step 4 完成卡 | 0.5h |
| 3 | DesignTab 套用後顯示來源提示 | 1h |
| 4 | PromptLabCard 套用按鈕文案 | 0.5h |
| 5 | PromptLabCard 折疊摘要說明 | 0.25h |
| 6 | AuditTab 分數行動卡（A/B/C/D/F）| 0.5h |
| 7 | AuditTab 套用按鈕區分原文/增強版 | 0.25h |
| 8 | StyleStudio「這是 prompt 不是圖」 | 0.5h |
| 9 | SmartTab 依結果顯示去哪 tab | 1h |
| 10 | NLMTab Step 5 貼上順序 | 0.5h |
| 11 | LabTab mode-based 下一步 | 0.5h |
| 12 | BrandPane「自評起點」說明 | 0.25h |

### 明確不做
- ❌ 不改 v1.1
- ❌ 不加新 tab
- ❌ 不改 7 tab 結構 / 4 區塊 glow / 核心 layout
- ❌ 不重寫 Prompt Lab 資料
- ❌ 不做直接生圖（另一個 sprint）

---

**請你決定**：
1. **全部 12 項都做** —— 我順序逐項實作（P0 先 → P1 → P2）
2. **只做 P0**（5 項：完成卡 / 跨 tab 目的地 / Prompt Lab 套用文案 / Smart Style Design 不會直接出圖 / Audit 分數行動卡）—— 約 3h
3. **先看完整規劃書**（路徑 `docs/PLAN-ux-guidance.md`）再決定
4. **改方向 / 補要求**

我等你指示，不會自己跑去改。