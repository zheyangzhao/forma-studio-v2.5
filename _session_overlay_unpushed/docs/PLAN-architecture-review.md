# Forma Studio v2.0 架構整併規格書（Codex × Claude 整合版）

日期：2026-04-30
方法：Codex 從程式碼結構審視 + Claude 從使用者旅程實測，兩份報告獨立完成後對比共識。
原始報告：
- `docs/CODEX-architecture-analysis.md`（489 行，程式碼角度）
- `docs/CLAUDE-user-journey-analysis.md`（使用者旅程角度，含 Playwright 實測）

---

## §一、共識：兩份報告的 6 大一致結論

兩邊獨立分析後，在以下 6 點完全共識：

| # | 共識點 | Codex 觀點 | Claude 觀點 |
|---|---|---|---|
| 1 | **Smart 應為主入口** | 「Smart 是入口，不一定要永久佔頂層 tab」 | 「Smart 解決 80% 場景」 |
| 2 | **Style Studio 與 Design 重疊度最高，應整併** | 「Style 是 prompt 組裝器，與 Design 重疊度高，最適合被嵌入」 | 「Style Studio 對牙醫看診忙的場景幫助小，可移除或合併」 |
| 3 | **彩蛋 Lab 應降到進階區** | 「Lab 是歷史包袱與實驗場的混合，應移到進階 / 實驗」 | 「彩蛋 🧪 < 5% 使用頻率」 |
| 4 | **Prompt Lab 是獨立資源庫，保留** | 「Prompt Lab 應保持輕量，因為它本質上是資料庫」 | 「Prompt Lab 116 條是獨立資源，wizard 化會破壞瀏覽體驗」 |
| 5 | **Audit 是品質閘門，獨立保留** | 「Audit 比較特殊，它既是 style 的下游，也是 design 的上游」 | 「Audit 是獨立工具，不重疊」 |
| 6 | **不破壞 v1.1 凍結契約** | 「不改 web/forma-studio.html」 | 「v1.1 hash 仍是 1bf63d1c...」 |

決策摘要：兩個獨立分析者得出相同結論——Smart 升主入口、Style 嵌入 Design、Lab 降進階、Prompt Lab + Audit 保留獨立。

---

## §二、輕微差異：兩份報告的 3 個分歧點

| 分歧點 | Claude 推薦 | Codex 推薦 | 我的整合判斷 |
|---|---|---|---|
| **Style Studio 是否完全移除** | 移除或併入 Design 為 sub-tab | 嵌入 Design 但保留頂層 tab 作捷徑 | 採 Codex：保留捷徑，避免 v1.1 → v2 切換時迷惑 |
| **整併幅度** | 7 → 5 tab（一次到位）| 7 → 4-5 tab，分兩段交付（B-lite → wizard）| 採 Codex：分兩段降低風險 |
| **是否做 wizard** | 部分 wizard 概念，不強制 layout | 第二段做生圖 wizard + NLM wizard | 採 Codex：先 B-lite 觀察使用，再決定 wizard 必要性 |

決策摘要：分歧點都是「保守度」的差異，採 Codex 較保守路線，分兩段交付降低風險。

---

## §三、最終推薦：方案 B-lite（共識方案）

### 整體目標
從「7 個平行 tab 的功能集合」變成「4-5 個有層級的工作台」，但**不刪任何核心功能**，只移位置與降層級。

### tab 改動表

| 之前 | 之後 | 動作 | 工程風險 |
|---|---|---|---|
| 🎨 Claude Design（tab 0）| 🎨 Claude Design（tab 1）| 維持核心，加入 Style chips sub-mode | 低 |
| 📑 NotebookLM（tab 1）| 📑 NotebookLM（tab 2）| 維持，5 step 流程不變 | 零 |
| 🖼️ 智慧製圖（tab 2）| **🚀 開始（tab 0）**| 升為預設首頁，名稱改「開始」或保留「智慧製圖」| 中（需改預設 tab + 名稱）|
| 📚 提示詞庫（tab 3）| 📚 提示詞庫（tab 3）| 維持獨立 | 零 |
| 🩺 體檢 & 增強（tab 4）| 🩺 體檢 & 增強（tab 4）| 維持獨立 | 零 |
| 🎬 風格實驗室（tab 5）| **嵌入 Design step 4** | 嵌入但保留頂層 tab 作捷徑（5 tab 仍存在）`(待用戶確認是否完全移除頂層)` | 中 |
| 彩蛋 🧪（tab 6）| **降到 Design 內「進階」抽屜** | 從頂層 tab bar 移除，改為 Design 內按鈕展開 | 低 |

### 結果：頂層 tab 從 7 個降為 5-6 個

**5 tab 版本**（移除 Style 與 Lab 頂層）：
1. 🚀 開始（原 Smart）
2. 🎨 Claude Design（含 Style chips + Lab 進階抽屜）
3. 📑 NotebookLM
4. 📚 提示詞庫
5. 🩺 體檢 & 增強

**6 tab 版本**（保留 Style 頂層作捷徑）：
1. 🚀 開始
2. 🎨 Claude Design
3. 📑 NotebookLM
4. 🎬 風格實驗室（捷徑）
5. 📚 提示詞庫
6. 🩺 體檢 & 增強

決策摘要：B-lite 版本把 7 tab 降到 5-6 tab，所有功能保留可達。

---

## §四、實作切分（B-lite 第一段）

### Sub-task 1：Smart 升為主入口（tab 0）
- 把 tabs 陣列順序改為 `[smart, design, nlm, plab, audit, ...]`
- 預設 tab `useState('design')` 改為 `useState('smart')`
- last-tab localStorage 邏輯不變（沒切過 tab 時用預設 smart）
- 名稱可改「🚀 開始」或保留「🖼️ 智慧製圖」`(待用戶確認)`
- 工時：1h

### Sub-task 2：Lab 從頂層降到 Design 進階抽屜
- 從 tabs 陣列移除 `lab`
- DesignTab 內加「🧪 進階實驗工具（彩蛋 Lab）」抽屜（預設收合）
- 抽屜展開後直接 inline 渲染 LabTab 內容（mode 選擇 + 4 個實驗）
- VALID_TAB_IDS 移除 `lab`
- 工時：2-3h

### Sub-task 3：Style Studio 嵌入 Design step 4
- DesignTab step 4「風格與生成」加入分段控制：
  - 模式 A：手動精修（現有 8 風格 + 20 哲學 + 12 品牌）
  - 模式 B：風格組裝（嵌入 Style Studio 的 5 類別 chips）
- 兩種模式產出後都進入「品牌靈感 + 平台 + 尺寸 + 語言」共用區
- 頂層 🎬 風格實驗室 tab 是否保留 `(待用戶確認 5 tab 還是 6 tab 版本)`
- 工時：4-6h

### Sub-task 4：Smart 結果區加「→ 直接複製」與「→ 進入 Design 精修」明確分流
- 既有「→ 前往 Claude Design 精修」按鈕加 prominent 樣式
- 加「✅ 直接複製，不進 Design」按鈕（讓 80% 場景一個 tab 結束）
- 工時：1h

### Sub-task 5：Playwright 驗收
- 從 Smart 進入做完植牙衛教海報旅程，確認 1 tab 可以完成
- 從 Smart 進入做完 NLM 文獻整理旅程，確認可分流到 NLM 完整流程
- Lab 進階抽屜在 Design 內可展開
- Style chips 在 Design step 4 可切換模式
- v1.1 git diff 維持 0
- 工時：1-2h

**第一段總計：9-13h**

決策摘要：第一段交付 5 個 sub-task，把 7 tab 降到 5-6 tab，不需做 wizard。

---

## §五、第二段（B-lite 後續，視第一段使用情況決定）

### Wizard 1：生圖品質流程
- Step 1：Smart 自動偵測（已有）
- Step 2：Style chips 快速組（已嵌入 Design）
- Step 3：Audit 8 維度體檢（送檢按鈕已有）
- Step 4：套用回 Design 精修（已有）
- Step 5：複製生圖
- 工時：6-10h

### Wizard 2：NotebookLM 知識整理
- Step 1：Smart 自動偵測 NLM route（已有）
- Step 2：進 NLM 5 step（已有）
- Step 3：兩段 OutBox + 貼上順序卡（已有）
- 工時：3-5h（主要是貫通既有功能）

**第二段總計：9-15h**

決策摘要：第二段視第一段使用回饋決定是否做 wizard，避免過度設計。

---

## §六、明確不做的事

| 不做 | 理由 |
|---|---|
| ❌ 不改 `web/forma-studio.html` | v1.1 永久凍結 |
| ❌ 不刪除任何 tab 的核心功能 | 所有功能必須可達，只移位置 |
| ❌ 不一次做完 7 → 3（C 方案）| 風險過高 |
| ❌ 不在沒有用戶確認下完全移除 Style 頂層 tab | 避免使用者迷惑 |
| ❌ 不重新命名 Smart 為「開始」（除非用戶確認）| 避免破壞既有 SEO / 文件 / 截圖記憶 |
| ❌ 不引入新框架 | 這是資訊架構決策，不是技術棧問題 |
| ❌ 不打破 localStorage 持久化（forma-v2.last-tab、收藏、歷史、Style 偏好）| Sprint 4 已建立的使用連續性 |
| ❌ 不為了減少 tab 而犧牲「可直接複製 prompt」的核心模式 | 看診忙時最重要 |

決策摘要：不做的事都是「避免在資訊架構整理時順手破壞既有功能與用戶習慣」。

---

## §七、3 個方案總比較表（給用戶決策）

| 方案 | 主軸 | tab 變化 | 工時 | 風險 | 對用戶可感差異 | 建議度 |
|---|---|---|---|---|---|---|
| **A：保守整理** | 只移 Lab、Style 嵌入但保留頂層 | 7 → 6 | 6-10h | 低 | 改變很小 | 🟡 過於保守 |
| **B-lite：共識方案** | Smart 升主入口、Lab 降進階、Style 嵌入 Design（保留頂層捷徑）| 7 → 5-6 | 9-13h（第一段）+ 9-15h（第二段選做）| 中 | 主入口更清楚、tab 數明顯減少 | 🟢 **強烈推薦** |
| **C：大刀闊斧重構** | 7 → 3 tab + 全面 wizard 化 | 7 → 3 | 32-56h | 高 | 像新產品，學習成本大 | 🔴 不建議短期做 |

決策摘要：**方案 B-lite** 是 Codex 與 Claude 共同推薦的最佳選擇。

---

## §八、用戶 3 個關鍵決策點

請你（用戶）決定下列 3 點：

### 決策 1：選哪個方案？
- [ ] A 保守整理
- [ ] **B-lite 共識方案（推薦）**
- [ ] C 大刀闊斧

### 決策 2：B-lite 細節（若選 B-lite）

**2-1：Smart 名稱**
- [ ] 保留「🖼️ 智慧製圖」
- [ ] 改名「🚀 開始」
- [ ] 改名其他：________

**2-2：Style Studio 頂層 tab**
- [ ] 完全移除（5 tab 版本，最乾淨）
- [ ] 保留作捷徑（6 tab 版本，較保守）

**2-3：彩蛋 Lab 位置**
- [ ] 完全移到 Design 內進階抽屜（推薦）
- [ ] 保留頂層 tab 但改名

### 決策 3：第二段 wizard 要不要做？
- [ ] 第一段 B-lite 做完先觀察使用，看狀況再決定（推薦）
- [ ] 一次做完含 wizard
- [ ] 不需要 wizard

決策摘要：請用戶在 3 個決策點點選後，動工 sub-task 1-5。

---

## §九、預期成果

完成 B-lite 第一段後：

1. **使用者進入 v2** 預設停留在 🚀 Smart（80% 場景一鍵解決）
2. **頂層 tab 從 7 個降到 5-6 個**，介面更乾淨
3. **核心功能 0 損失**：Lab 在 Design 進階抽屜可達、Style chips 在 Design step 4 可切換
4. **v1.1 凍結契約完整**：`git diff web/forma-studio.html` 仍為 0 行
5. **localStorage 持久化全保留**：last-tab、收藏、歷史、Style 偏好全部繼續運作
6. **使用者習慣保護**：tab 名稱與位置變動可逆（必要時可回退）

驗收標準：
- Playwright 跑 3 個典型旅程都能在 ≤ 2 個 tab 內完成
- v1.1 hash 不變
- JSX @babel/parser 通過
- 0 console errors

決策摘要：B-lite 完成後，v2 從「sprint 疊加型工具」變成「有層級的工作台」，但不破壞既有任何能力。

---

## §十、結論

兩份獨立分析（Codex 程式碼角度 + Claude 使用者旅程實測）得到驚人相似的結論：
**v2.0 不是功能太多，而是「入口、素材庫、檢查器、終點工具」被放在同一層 tab bar**。

修法不是刪功能，而是 **把 tab 分層**：
- 入口層：🚀 Smart（主入口）
- 終點工具：🎨 Design / 📑 NotebookLM
- 素材庫：📚 Prompt Lab
- 品質閘門：🩺 Audit
- 進階實驗：🧪 Lab（藏在 Design 內）
- 風格組裝：🎬 Style Studio（嵌入 Design 內）

**等用戶從 §八 決策後即可動工。**
