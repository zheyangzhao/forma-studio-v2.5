## Sprint PPT Flow 完成 ✅（commit `69d2eb8`，+330 行）

P0+P1 全套交付，3 個極端旅程驗收 PASS。

### 你會在 v2 看到的新功能

| 入口 | 行為 |
|---|---|
| **🖼️ 智慧製圖** | 一句話有「簡報」字眼 → 完成卡後出現「📊 開啟簡報企劃」紫色按鈕 |
| **📑 NotebookLM** | Step 5 任務=簡報製作 → PPT Flow 自動展開 |
| **🎨 Claude Design** | 第 5 個 sub「📊 投影片簡報」直接做 |

### 點開後 PPT Flow Lite 給你 7 區塊

| 區塊 | 內容 |
|---|---|
| ⚠️ 邊界提示 | 「不直接生成 PPT 檔」明確說 |
| 📝 任務摘要 | 主題詞 / 受眾 / 推薦頁數 / 比例（自動推斷）|
| 🎨 **3 套風格方案** | 雜誌編輯 / 資訊密度 / 視覺敘事（點選即時換大綱與 prompt）|
| ❓ AI 反問清單 | 標題 / 講者 / speaker notes / 品牌色（4 條）|
| 🖼️ 素材引用清單 | 自動抽 markdown / HTML 圖片引用 |
| 📋 **Markdown 大綱** | 可貼 Marp / Slidev / Gamma |
| ✨ **完整 deck prompt** | 給 ChatGPT Canvas / Claude Artifacts / NotebookLM |
| 🛠️ 下一步工具建議 | 5 個工具中性列表 |

### 重要邊界（為什麼不直接產 PPT）

> v2 是 web app，沒有檔案系統存取。要本機自動產 pptx 需要 **Claude Code Skill 環境**，這是 P2 後續專案。

### v2.0 完整 Sprint 史

| Sprint | 內容 |
|---|---|
| 0-3 | v2 基礎 + 體檢 + 風格實驗室 |
| 1.5-1.7 | 中文化（標題 + 摘要 + 全文翻譯）|
| 1.8 | UX 引導 12 項 |
| 2 修補 | Audit onboarding |
| 4 | localStorage 持久化 |
| 5 | README + CHANGELOG |
| B-lite | 7→6 tab 整併 |
| Truly-Neutral | 多用途中性化 |
| **PPT Flow** | **簡報企劃流程**（剛完成）|

**v1.1 hash 仍不變**：`1bf63d1c...`

---

## 你的下一步建議

1. **試用** v2，特別是這 3 個入口的 PPT Flow（重整 Chrome 後）
2. 試試實際的牙醫場景（「植牙衛教簡報」/「病例討論會」）
3. 試試紫微斗數（「紫微入門課程簡報」）
4. 試試一般情境（「咖啡店開幕宣傳簡報」/「履歷簡報」）
5. 把產出的 deck prompt 真的貼到 ChatGPT 看效果如何

有任何發現或需要修補的地方告訴我。如果方向對了，下一步可以做：
- 收集你實際使用的回饋 → 微調文案 / 補功能
- P2 獨立 Claude Skill（讀本機檔案、自動產 pptx）