# Forma Studio Web 版 CHANGELOG

> 本檔案紀錄 `web/forma-studio-v2.html` 的演進。
> `web/forma-studio.html`（v1.1 穩定版）自 commit `ff8e11d` 起永久凍結，git diff 須為 0 行。

---

## v2.0 — 實驗版（持續迭代中）

### Sprint 1.8 — UX 引導性大修補（commit `6410190`，2026-04-30）

依 `docs/PLAN-ux-guidance.md` 完成 12 項小修補，全部都在 v2 文案 / 元件層，不動 v1.1。

**P0（5 項）**
- 共用元件 `NextStepCard`（emerald/amber/cyan/rose 4 配色 + actions 按鈕陣列）
- DesignTab Step 4 完成卡：「✅ 已產出圖像 prompt → 3 步驟複製到生圖工具」
- DesignTab 跨 tab 套用後顯示來源提示卡「📥 從 📚 提示詞庫 套用 已套用『XXX』的英文 prompt」（10 秒自動消失）
- PromptLabCard 套用按鈕：「→ 套用英文 prompt 到 Claude Design」+ targetSub 改中文 label
- PromptLabCard 折疊摘要 label：「📖 中文摘要（快速理解，不是要複製的 prompt）」
- AuditTab 分數行動卡：A → 可直接套用 / B → 補黃色 / C/D/F → 先修紅色再重新體檢
- StyleStudio 琥珀色「⚠️ 不是圖片」banner + 完成卡 3 步驟下一步

**P1（4 項）**
- AuditTab 套用按鈕區分原文 vs AI 增強版
- SmartTab 依 selSub 顯示對應下一步按鈕（image / nlm / proto / brand）
- NLMTab Step 5 加貼上順序完成卡（先設自定義指示 → 再貼任務指令）
- LabTab mode-based 下一步（viral/ted/batch → NotebookLM / anti-slop → Audit）

**P2（1 項）**
- BrandPane 5 維度評審加「自評起點，不是 AI 最終品質保證」說明

### Sprint 1.7 — 116 條 prompt 全文中文翻譯（commit `284771f`，2026-04-30）

- 新增 `tools/translate_prompts_zh.py` 用 GPT-4o-mini 並行翻譯 116 條（207 秒，零失敗）
- `translations-zh.json` schema v3：116 條完整中文翻譯
- 修 `re.sub` replacement string 中的 `\n` 被解釋為換行符的 inline bug（用 lambda 規避）
- PromptLabCard 展開狀態：中文摘要 → 中文整段翻譯（cyan 框）→ 黃色「英文純複製」提示 → 純英文 prompt（font-mono lang="en"）

### Sprint 1.6 — 116 條中文摘要（commit `15df652`，2026-04-30）

- 116 條每條 1-2 句中文摘要（描述「這條 prompt 想做什麼」）
- 折疊狀態：顯示中文摘要（不再英文截斷）
- 展開狀態：中文摘要 + 「💡 英文 prompt（推薦複製使用）」+ 完整英文 prompt
- 搜尋演算法包含 `prompt_summary_zh` 欄位

### Sprint 3 — 風格實驗室 tab（commit `f4f57b7`，2026-04-29）

- 新增第 7 個 tab「🎬 風格實驗室」
- 5 大類別 × 4-6 組 chips 自動組裝英文 prompt：
  - 📷 人像 / 商業攝影（含「診間白光」for 牙醫場景）
  - 🎨 海報 / 插畫（含「薄荷奶油」for 醫療品牌）
  - 💻 UI / 產品介面
  - 👤 角色 / 吉祥物（含「Pop Mart 盲盒風」）
  - 🩺 醫學圖解 / 衛教（含「台灣患者」對象 → in-image text 繁中）
- 尺寸 1:1/2:3/3:2 + 品質 low/medium/high（成本顯示）
- 跨 tab：「→ 套用到 Claude Design」與「🩺 送去體檢」雙橋接

### Sprint 1.5 — 提示詞庫中文化（commit `6e2c5b3`，2026-04-30）

- `web/prompt-library/translations-zh.json` 新增（116 條中文標題）
- v2 inline 該 JSON 為 `<script id="forma-titles-zh">` 區塊
- 卡片標題：中文（粗大白字）+ 英文（小灰斜體副標）
- 頂部加琥珀色 banner 解釋「為什麼預設顯示中文，但 prompt 仍是英文」
- 搜尋框 placeholder 改為中英都可
- 搜尋演算法包含 `prompt_title_zh` 欄位

### Sprint 2 修補 — AuditTab onboarding（commit `065fc8b`，2026-04-30）

- 加黃色說明卡（💡 這個 tab 是做什麼的？）
- 範例改成卡片（每個附 hint 副標）
- 預設載入「弱例」並立刻跑體檢（不再空白頁）
- 按鈕標籤更明確（重新體檢 / 已跑過 / API Key 鎖頭）
- textarea placeholder 用 O2Win 牙醫情境

### Sprint 2 — 體檢 & 增強 tab（commit `046ec2a`，2026-04-30）

- 新增第 6 個 tab「🩺 體檢 & 增強」
- 8 維度本地體檢（依 craft.md §19 final audit）：
  1. 任務意圖
  2. 受眾與情境
  3. 核心訊息（字數門檻）
  4. 構圖 / 版面 / 色彩
  5. in-image 文字（引號偵測）
  6. size / quality / negative
  7. 反 AI Slop（黑名單 12 詞 + 否定詞偵測：no/avoid/不要 不扣分）
  8. Source attribution
- Score 0-100 + Grade A-F + 通過/補強/缺失計數
- AI 增強：用 GPT-4o-mini 改寫 + 自動再體檢
- 跨 tab：「→ 套用到 Claude Design」橋接

### Sprint 1 — 提示詞庫 tab（commit `8e653f3`，2026-04-29）

- 新增第 5 個 tab「📚 提示詞庫」
- 116 條 prompt 完整瀏覽器（wuyoscar 66 + EvoLinkAI 50）
- 全文搜尋（標題 / prompt 內容 / 作者）
- 來源 filter / 製圖方式 filter / 17 類別 chips 多選
- 卡片式 grid + 漸進顯示（每次 24，按「載入更多」）
- 「套用到 Claude Design」跨 tab 橋接（重用 `applyGalleryPrompt` 機制）
- App 加 `pendingApply` state 作為跨 tab 橋接
- DesignTab 改接 props `{pendingApply, clearPending}`

### Sprint 0 — v2 基線（commit `ff8e11d`，2026-04-29）

- 完整複製 `web/forma-studio.html`（348858 bytes）→ `web/forma-studio-v2.html`
- 改 v2 標題為「Forma Studio v2.0 實驗版」+ 副標「v1.1 穩定版仍可用」
- 新增 `docs/PLAN-v2.0-new-version.md`（397 行整體規劃）
- 保留 `docs/PLAN-v1.x-strengthening.md` 為決策歷史
- **v1.1 凍結契約成立**：自此 commit 起 `git diff web/forma-studio.html` 須為 0 行

---

## v1.1 — 穩定版（永久凍結）

`web/forma-studio.html` 永遠維持 commit `ff8e11d` 之前的最後狀態。
v1.1 完整規格 / 28 步 Playwright 驗收 / 116 條 prompt 整合在 [`zheyangzhao/forma-studio`](https://github.com/zheyangzhao/forma-studio) tag `v1.1`。

主要功能：
- 4 區塊 glow 流程：描述需求 → 受眾基調 → 製圖方式 → 風格生成
- 4 大 tab：Claude Design / NotebookLM / 智慧製圖 / 彩蛋 Lab
- 20 種設計哲學庫（5 流派）
- 12 個設計品牌 chips
- 11 任務 / 20 領域 / 10 受眾 / 12 框架
- 116 條 prompt gallery（inline JSON）
- AI 增強鈕（GPT-4o-mini）

---

## 統計

- v2.0 共 9 個 sprint commit（Sprint 0 → Sprint 1.8）
- v2 HTML 從 348858 bytes 成長到約 56 萬 bytes（含中文翻譯 inline）
- v1.1 hash 全程不變：`1bf63d1cfbf6900afbe5927496413f216de23c43`
- 所有 sprint 都用 `@babel/parser` JSX 驗證 + Playwright 截圖驗收

---

## 來源 Attribution

| 來源 | License | v2 用途 |
|---|---|---|
| `wuyoscar/gpt_image_2_skill` | CC BY 4.0 | 提示詞庫 66 條 + craft.md §19 audit + size/quality 撥盤 |
| `EvoLinkAI/awesome-gpt-image-2-prompts` | CC BY 4.0 | 提示詞庫 50 條 + 5 大類別案例 |
| 用戶自製 claude.ai Artifact | 用戶授權 | 風格實驗室 5 類別 UX 方向參考 |
