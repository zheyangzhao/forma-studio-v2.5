## Codex PPT 評估完成 ✅（commit `e85a184`，275 行）

### Codex 的核心判斷

Codex **不建議直接複製 axi Skill**，而是「拆兩層」：

| 層 | 工具 | 做什麼 |
|---|---|---|
| **第一層** | Forma Studio v2 (web) | 簡報**企劃**：反問清單 + 3 套風格方案 + Markdown 大綱 + 給外部 AI 的 prompt |
| **第二層** | 未來獨立 Forma Studio Claude Skill | 簡報**生成**：讀本機檔案、抓素材、產 HTML slides、截圖驗證 |

### 最推薦方案 A：Smart 內的「PPT Flow Lite」（P0，4-7h）

不加新 tab。在 Smart 偵測到「簡報」需求時，結果區出現「📊 PPT Flow Lite」按鈕。點開後產出：

| 區塊 | 內容 |
|---|---|
| **任務摘要** | 從一句話拆解出主題 / 受眾 / 用途 |
| **反問清單** | 風格偏哪種？尺寸？頁數？要不要 speaker notes？ |
| **3 套風格方案** | 每套含：風格名、適合情境、視覺語言、敘事節奏、頁面結構 |
| **推薦頁數與比例** | 例：10 頁 / 16:9 |
| **Markdown 大綱** | 可貼到 Marp / Slidev / Gamma |
| **素材清單與缺口** | 提醒使用者哪些素材還沒給 |
| **外部 AI prompt** | 完整 deck prompt 給 ChatGPT / Claude |
| **下一步工具建議** | 列出哪些工具可承接這份 prompt |

### Codex 推薦的「不做」清單
- ❌ 不新增第 7 tab（B-lite 剛 7→6）
- ❌ 不重做 NotebookLM 5 step
- ❌ 不承諾 v2 自動產 pptx
- ❌ 不承諾抓取所有文章原圖（v2 single-file HTML 做不到）
- ❌ 不把 axi Skill 原樣搬進 v2

### Codex 待你確認的 5 件事

1. **axi Skill 真實輸出格式**？是 pptx、HTML slides、還是 Markdown？（影響 P0 對齊體驗）
2. **是否真的要獨立 Claude Skill**？P2 才做還是不做？
3. **功能名稱**：PPT Flow Lite / 簡報企劃流程 / 其他？
4. **第一版是否抽取 Markdown 圖片引用**（`![](path)` 這種）？
5. **外部 prompt 偏哪個工具**？ChatGPT、Claude、還是中性多工具？

### 工時估算

| 階段 | 範圍 | 工時 |
|---|---|---|
| **P0（推薦做）** | Smart PPT Flow Lite + 文案邊界 + 驗證 | **4-7h** |
| P1（觀望）| NotebookLM 簡報出口 + 素材辨識 + Design HTML slides prompt | 9-16h |
| P2（後續專案）| 獨立 Claude Skill / docx 抽圖 / HTML slide preview | 數天 |

---

## 你的決策

📂 完整規劃書：`docs/PLAN-ppt-flow.md`

🟢 **推薦做 P0（4-7h）**：Smart 內加 PPT Flow Lite，不動 6 tab 架構

要動工嗎？或者你想先回答 Codex 那 5 個確認問題我再開工？或者完整規劃書要看完再決定？