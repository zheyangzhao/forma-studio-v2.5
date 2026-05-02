## Sprint 1 完成 ✅

**Commit `8e653f3`**：v2 新增第 5 個 tab「📚 提示詞庫」(+252 行)

### 你現在可以做的事

打開 `http://localhost:8765/forma-studio-v2.html`，點「📚 提示詞庫」tab：
- 看 116 條 prompt（wuyoscar 66 + EvoLinkAI 50）
- 搜尋任何關鍵字（試試「chess」「dashboard」「poster」）
- 用「來源」「製圖方式」「類別」三層 filter
- 點「套用到 Claude Design」→ 自動跳轉並填好 prompt
- 點「複製」直接拿到剪貼簿

### 驗收結果
| 項目 | 結果 |
|---|---|
| v1.1 hash 變化 | **0**（hash 仍是 `1bf63d1c...`）|
| v2 JSX 語法 | **PASS**（@babel/parser）|
| Console errors | **0** |
| 跨 tab 套用測試 | **PASS**（chess prompt 完整填入 desc）|
| Attribution 顯示 | **PASS**（CC BY 4.0、作者 handle）|

### 截圖證據
- `v1.1-baseline.png` — v1.1 老樣子
- `v2-baseline.png` — v2 標題顯示「v2.0 實驗版」
- `v2-promptlab.png` — Prompt Lab 116 條
- `v2-promptlab-search.png` — 搜尋「chess」過濾出 2 條
- `v2-after-apply.png` — 套用後切到 Claude Design + desc 已填

---

## 接下來

Sprint 2 是 **Audit & Enhance**（craft.md §19 prompt 體檢）。預估 14-22h，會在 v2 加第 6 個 tab。

**你要：**
1. **繼續 Sprint 2**（直接開做 Audit & Enhance）
2. **先停下來讓你看診時試用 Prompt Lab**，回頭再決定
3. **改順序**（譬如先做 Style Studio / History & Save）

我建議先讓你試用，回饋哪裡卡卡的再調整。Server 還在背景跑（`http://localhost:8765/forma-studio-v2.html`），你看診空檔可以打開玩玩看。