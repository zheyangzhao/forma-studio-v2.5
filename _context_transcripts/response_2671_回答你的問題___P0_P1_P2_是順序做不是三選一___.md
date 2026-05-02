回答你的問題：**P0/P1/P2 是順序做不是三選一**。但我建議的順序是：

## 建議：**P0 + P1 一次到位**（13-23h），P2 留作獨立專案

### 為什麼 P0 + P1 一起做

| 階段 | 對牙醫師的價值 | 為什麼 |
|---|---|---|
| **P0 Smart PPT Flow** | 患者衛教簡報、診所介紹一句話入手 | 主入口 |
| **P1-1 NotebookLM 簡報出口** | **病例討論會、文獻整理 → deck**（牙醫高頻場景）| 既有 5 step 加碼 |
| **P1-2 Markdown 素材辨識** | 上傳病例 markdown 自動抽圖位置 | 省手動 |
| **P1-3 Design HTML slides prompt** | 診所介紹官網式投影片 | 視覺進階 |
| P2 獨立 Claude Skill | 讀本機檔案、自動產 pptx | 需 Claude Code 環境，不在 v2 範圍 |

**P0 單做問題**：牙醫場景多是「文獻 → 簡報」（病例討論會、學術發表），這走 NotebookLM。只做 P0 等於把高頻場景留在 P1。

**P0+P1 一起做的好處**：
- Smart（一句話入口）+ NotebookLM（文獻深度入口）兩個都覆蓋
- 牙醫場景 80%+ 滿足
- 不用等「第二次 sprint」

**P2 應該獨立**：
- Claude Skill 是另一個技術棧（要 git clone、本機檔案系統）
- v2 web app 做不到 pptx 直接生成
- P2 應該是 P0+P1 上線後**收集到實際痛點**才做（不是預先做）

---

## 為了避免你再花時間選擇，我直接給 5 個確認問題的合理預設

| Codex 問題 | 我的建議答案 | 理由 |
|---|---|---|
| axi 真實輸出格式？ | **不模仿，做我們的版本**（產 prompt + Markdown 大綱）| v2 是 web，產 prompt 給外部 AI 用最合理 |
| 是否做獨立 Claude Skill？ | **P0+P1 上線後視回饋再決定**（暫不做）| 避免分散精力 |
| 功能名稱？ | **「📊 簡報企劃」** | 直白中文，不用 Lite/Flow 英文混搭 |
| 第一版抽 Markdown 圖片引用？ | **做**（Codex 估 3-6h 但其實正則 1h 內可做） | 簡單實用 |
| 外部 prompt 偏哪個工具？ | **中性多工具**（ChatGPT / Claude / NotebookLM 都列出）| 牙醫各種工具都可能用 |

---

## 工時估算與順序

| Sub-task | 工時 | 階段 |
|---|---|---|
| Smart PPT Flow Lite + 反問清單 + 3 方案 + Markdown 大綱 + prompt | 4-7h | P0 |
| 命名與文案邊界（防止過度承諾「直接生成 PPT」）| 1-2h | P0 |
| Smart 驗證（既有功能不破壞）| 1-2h | P0 |
| NotebookLM Step 5 加「→ 轉成 deck prompt」按鈕 | 3-5h | P1 |
| Markdown 圖片引用辨識 | 1-3h | P1 |
| Design 加 HTML slides prompt sub | 3-5h | P1 |

**總計：13-24h**（一個完整工作週的子集）

---

## 我的建議

直接走 **P0+P1 全套**。如果你同意，我立刻動手按上面 6 個 sub-task 順序做。

P2 獨立 Skill **記在未來 backlog**，不在當前 sprint 動手。

要動工嗎？