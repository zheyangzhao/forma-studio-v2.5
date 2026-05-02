我的巡邏報告完成，共找到 **6 大關鍵醫療偏向**，最嚴重的是 Smart 的 GPT system prompt 寫死「**你是 O2Win 牙醫診所 AI 助理**」。等 Codex 寫完規格書後合併。

---

**目前狀態**：
- ✅ B-lite 已 commit `5f97c3f`（7→6 tab + 文案去醫療化）
- ✅ Claude 巡邏報告完成 `docs/CLAUDE-medical-bias-audit.md`（6 大偏向 + P0/P1/P2 修補清單）
- ⏳ Codex 在背景寫 `docs/PLAN-multi-domain.md`（task `bqrrrd6e4`）
- ⏳ 等 Codex 完成後合併成最終規格書

**Claude 巡邏的 3 個重大發現**：

1. **🔴 Smart 的 GPT system prompt 寫死「你是 O2Win 牙醫診所 AI 助理」**（line 1079）
   - JSON schema 強迫 `nlm_domain` 只能六選一全部醫療相關
   - JSON schema 強迫 `nlm_aud` 只能選「患者/家長/牙醫/實習醫師/兒童患者」
   - **結論：紫微斗數老師輸入「紫微入門課程」會被 GPT 強迫塞進醫療框架**

2. **🟡 本地規則 fallback 直接到醫療**（line 1547-1559）
   - `domain` fallback = `'口腔醫學'`
   - `audience` fallback = `'成人患者/家長'`
   - 沒有命中任何醫療關鍵字 → 紫微斗數仍被分到「口腔醫學 + 成人患者/家長」

3. **🟡 20 哲學 useCase 至少 13 個含醫療字眼**
   - Pentagram 信息建築：「診所衛教、學術報告」
   - IDEO 功能主義：「App 介面、患者導引流程」
   - 紫微斗數老師看會覺得「全部不適合我」

**P0 修補清單（紫微斗數能用的關鍵）**：
- Smart system prompt 重寫為多領域（2-3h）
- 本地規則 fallback 去醫療化 + 加命理/教育/商業關鍵字（3-4h）

我等 Codex 通知再合併規格書。