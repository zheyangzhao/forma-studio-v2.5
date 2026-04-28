---
name: forma-studio
description: 跨行業 AI prompt 生成工具——把模糊需求轉成可直接餵 GPT-4o-mini / GPT Image 2 / Claude 的高品質提示詞。涵蓋律師、會計師、教師、設計師、產品經理、行銷企劃、不動產、餐旅、研究等。沿襲 4 區塊 glow 流程（描述需求→受眾基調→製圖方式→風格生成），整合 66 條結構化 prompt gallery（12 類）、19 節 craft.md 品質檢查層、20 種設計哲學庫。觸發：使用者說「幫我生 prompt」「幫我做海報/簡報/Logo/UI mockup/年報視覺/教材插圖」「給我設計指令」「跨行業通用 prompt」「Forma Studio」「forma-studio」。
---

# Forma Studio

跨行業 AI prompt 生成工具。從模糊需求 → 完整 AI 設計指令，4 區塊依序引導，內建 20 種設計哲學庫 + 66 條跨行業 prompt gallery + 19 節 prompt 品質檢查層。

## 何時使用此 Skill

觸發條件：
- 使用者描述模糊的設計／視覺／簡報／圖像需求，需要結構化 prompt
- 跨行業情境（任一即觸發）：
  - 律師：提案書視覺、案件流程圖、法庭簡報
  - 會計師：年報視覺、財務儀表板、稅務流程圖
  - 教師：教材插圖、知識圖卡、課程招募海報
  - 設計師：UI mockup、品牌指引、Logo 系統
  - 產品經理：pitch deck、用戶旅程圖、概念稿
  - 行銷／企劃：廣告素材、活動海報、社群圖卡
  - 不動產：建案概念圖、空間提案、虛擬看屋
  - 餐旅：菜單視覺、空間氛圍、商品攝影
  - 研究／學術：論文配圖、概念示意、資料視覺化
- 需要符合品牌一致性的多輪 prompt 產出
- 需要 #0 事實驗證、反 AI Slop、5-10-2-8 品質門檻檢查

## 安裝

### Claude Code
```text
/plugin marketplace add zheyangzhao/forma-studio-v2.5
/plugin install forma-studio@zheyangzhao
```

### Codex
```text
$skill-installer install https://github.com/zheyangzhao/forma-studio-v2.5/tree/main/skills/forma-studio
```

### 手動安裝
```bash
git clone https://github.com/zheyangzhao/forma-studio-v2.5.git
ln -s "$PWD/forma-studio-v2.5/skills/forma-studio" "$AGENT_SKILLS_DIR/forma-studio"
```

讀 `OPENAI_API_KEY` 環境變數或 `~/.env`。

## 主要工作流（4 區塊 glow，沿襲 v1.0）

當使用者要求生成 prompt 時，**依序**引導完成 4 區塊。每區塊可在使用者確認後才推進下一區塊（避免資訊一次過載）。

### 區塊 1：描述需求
- 使用者上傳素材（圖片／文件／URL）或寫文字描述
- 詢問場景：行業、用途、預計使用渠道
- 若提到具體品牌／產品／版本 → **觸發 #0 事實驗證**（craft.md §0）

### 區塊 2：受眾與基調
- 受眾：誰會看到、決策情境、年齡層
- 基調：嚴肅／活潑／高端／實用／編輯感
- 行業關鍵詞：用 `web/prompt-library/gallery-index.json` 的 `industries` 欄位匹配

### 區塊 3：選擇製圖方式
- 4 種子選項：
  - 🖼️ 圖像生成（GPT Image 2 generations）
  - 🎯 設計稿／原型（Junior Designer 工作流）
  - 📊 資訊圖表（infographic schema）
  - 🏷️ 品牌資產協議 + 5 維度評審
- 跨參考 `web/prompt-library/{slug}.json` 找對應類別範本

### 區塊 4：風格與生成
- 從 20 種設計哲學選 1-3 個（風格 DNA）
- 從 12 個設計品牌選 0-1 個（品牌參考）
- 套 craft.md 19 節品質檢查層
- 輸出最終 prompt（可直接貼進 ChatGPT / Claude / DALL-E / 桌面版 PyQt6）

## 跨行業範例

### 範例 A：律師事務所提案書封面
```
使用者：「我要做一份併購交易的提案書封面」
→ 區塊 1：行業=legal、用途=pitch、渠道=PDF 列印 + 數位
→ 區塊 2：受眾=企業客戶 C-level、基調=嚴肅高端
→ 區塊 3：設計稿／原型 → 從 prompt-library 撈 ui-ux-mockups + brand-systems
→ 區塊 4：哲學=Pentagram 信息建築派、品牌=自有 Logo
→ 輸出：含 "M&A Advisory" / "Q2 2026" 等 in-image text 的封面 prompt
```

### 範例 B：教師教材插圖
```
使用者：「我要做光合作用的概念示意圖」
→ 區塊 1：行業=education、用途=教材、渠道=投影片
→ 區塊 2：受眾=高中學生、基調=活潑清晰
→ 區塊 3：資訊圖表 → 從 prompt-library 撈 scientific-and-educational
→ 區塊 4：哲學=日式極簡派、無品牌約束
→ 輸出：含葉綠體剖面 + CO₂/H₂O/光線箭頭標籤的 prompt
```

### 範例 C：會計師年報資料視覺化
```
使用者：「我要做 2025 年度營收成長的年報視覺」
→ 區塊 1：行業=accounting、用途=annual_report、渠道=PDF + 印刷
→ 區塊 2：受眾=股東、基調=穩健可信
→ 區塊 3：資訊圖表 → 從 prompt-library 撈 data-visualization
→ 區塊 4：哲學=信息建築派、品牌=公司主色
→ 輸出：含具體數據（YoY +18.4% 等）的儀表板 prompt
```

### 範例 D：餐廳菜單視覺
```
使用者：「我要做新菜單的拍攝指示」
→ 區塊 1：行業=hospitality、用途=menu、渠道=印刷 + IG
→ 區塊 2：受眾=用餐客群、基調=溫暖食慾感
→ 區塊 3：圖像生成 → 從 prompt-library 撈 product-and-food + photography
→ 區塊 4：哲學=北歐功能派、無品牌約束
→ 輸出：拍攝角度 + 光線 + 道具的完整 prompt
```

## Prompt Gallery 索引

66 條跨行業通用 prompt，分 12 類，路徑 `web/prompt-library/`：

| 類別 | 條數 | 適用行業 |
|---|---:|---|
| UI/UX Mockups | 5 | product, design, marketing, legal, education |
| Typography & Posters | 13 | marketing, events, design, education |
| Infographics & Field Guides | 8 | education, legal, accounting, research |
| Brand Systems & Identity | 3 | design, marketing |
| Edit Endpoint Showcase | 2 | design, marketing（含多參考圖 + mask 範例） |
| Photography | 4 | marketing, real_estate, hospitality, retail |
| Product & Food | 4 | marketing, retail, hospitality |
| Data Visualization | 5 | accounting, research, education, product |
| Architecture & Interior | 5 | real_estate, design, hospitality |
| Technical Illustration | 5 | engineering, manufacturing, education |
| Cinematic & Animation | 5 | marketing, entertainment |
| Scientific & Educational | 7 | education, research |

每筆 entry 含 `id` / `title` / `size` / `pixel` / `credit` / `prompt` / `source`。
索引檔：`web/prompt-library/gallery-index.json`

### 載入方式（agent 用）

```python
import json
from pathlib import Path

idx = json.loads(Path("web/prompt-library/gallery-index.json").read_text())
# 找符合行業的類別
for cat in idx["categories"]:
    if "legal" in cat["industries"]:
        data = json.loads(Path(f"web/prompt-library/{cat['file']}").read_text())
        for p in data["prompts"]:
            print(p["id"], p["title"])
```

## Craft 品質檢查層

每次輸出最終 prompt 前，**必須**過 `references/craft.md` 的 19 節 audit checklist。
重點：
- §0 事實驗證（具體品牌／產品／版本前必先 WebSearch）
- §5–6 品牌資產 5-10-2-8 門檻
- §13 中文文字／海報／infographic 自動跳 `quality=high`
- §14 反 AI Slop 約束
- §19 final prompt audit（跑一次再輸出）

## GPT Image 2 endpoint 對應

當 prompt 已生成、使用者要實際出圖：

| 情境 | endpoint | 主要參數 |
|---|---|---|
| 純文字生圖 | `POST /v1/images/generations` | prompt, size, quality, n |
| 多參考圖修圖 | `POST /v1/images/edits` | image[], prompt, size, quality |
| 局部 inpaint | `POST /v1/images/edits` | image, mask (PNG alpha), prompt |

`size` 捷徑：`portrait`(1024x1536) / `landscape`(1536x1024) / `square`(1024x1024) / `2k`(2048x2048) / `4k`(3840x2160)

`quality` 預算：
- `low` ≈ $0.005／張 — 草稿、批量探索
- `medium` ≈ $0.04／張 — 探索與風格嘗試
- `high` ≈ $0.17／張 — 含中文文字／海報／infographic／交付稿

桌面版（Tier 2 待實作）會把這三段做成 slider，即時顯示 n × 單價估算。

## References

| 檔案 | 用途 |
|---|---|
| `references/craft.md` | 19 節 prompt 品質檢查層（含 #0 + 反 AI Slop + 5-10-2-8） |
| `references/gallery-index.md`（待產出） | gallery 路由索引（TBD） |

## 設計原則（從 v1.0 繼承）

1. **跨行業通用**：不限定特定行業，所有資料庫設計需通用標籤化
2. **API Key BYOK**：使用者自帶 key，session 暫存，**不寫 localStorage、不寫檔**
3. **反 AI Slop**：禁紫漸變、emoji 圖標、generic card wall、AI-generated 假臉
4. **#0 事實驗證**：具體品牌／產品／版本前必須先 WebSearch 驗證
5. **5-10-2-8 品質門檻**：搜 5 條、留 10 個 candidates、產 2 個 finalist、迭代 8 輪內收斂
6. **Junior Designer 工作流**：先寫 assumptions + placeholders + reasoning comments，多次 show 進度

## License & Attribution

本 Skill 採 [MIT License](https://github.com/zheyangzhao/forma-studio-v2.5/blob/main/LICENSE)。

吸收自外部開源專案的內容保留原 license：
- prompt gallery 條目：CC BY 4.0（來源 [`gpt_image_2_skill`](https://github.com/wuyoscar/gpt_image_2_skill)）
- DESIGN.md 共享記憶模式：MIT（來源 [`open-codesign`](https://github.com/OpenCoworkAI/open-codesign)）

每個 `web/prompt-library/*.json` 內 `source` 欄位含 repo / license / url 完整 attribution。
