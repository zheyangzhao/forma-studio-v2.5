# Forma Studio · Prompt 品質檢查層（craft.md）

每次最終輸出 prompt 前，依序跑完 19 節 audit。**寧缺毋濫**：缺欄位寧可回頭補，也不要硬塞稻草人。

合併三層規則：
- `gpt_image_2_skill` 的 19 節 prompt 寫作清單（CC BY 4.0）
- Forma Studio v1.0 的「#0 事實驗證」「反 AI Slop」「5-10-2-8 品質門檻」

---

## §0 事實驗證先於假設（Huashu #0）

**規則**：prompt 中若提到具體品牌／產品／版本／人名／法規／日期 → **先 WebSearch 驗證**。

**為什麼**：AI 對特定事實常幻想（錯誤 logo 形狀、不存在的型號、過時版本）。一旦寫進 prompt 等於把幻想固化進輸出。

**必填**：在 prompt 草稿中標註 `[VERIFY: <項目>]`，audit 時逐項通過或註明已查。

**範例**：
- ❌ Bad：「Apple Vision Pro 2026 款的渲染圖」（型號需驗證是否存在）
- ✅ Good：「[VERIFY: Apple Vision Pro 第一代 2024-02 上市] 的渲染圖，依官方規格 23M 像素 micro-OLED」

---

## §1 任務意圖

**規則**：開頭一句講清楚這張圖要幹什麼。

**選項**：`image`（純生成）／`edit`（修既有圖）／`infographic`（資訊圖）／`prototype`（UI/UX）／`brand`（品牌資產）

**為什麼**：意圖決定 endpoint（generations vs edits）、決定 quality 預算、決定後續欄位有哪些。

**範例**：「Generate a polished UI mockup for ...」「Edit the provided poster to ...」

---

## §2 受眾與使用場景

**規則**：受眾＋渠道＋決策情境，三項齊全。

**為什麼**：同一品牌主視覺給 C-level 看 vs 給社群滑就要不同的字級、留白、資訊密度。

**必填**：
- audience：年齡層、職務／身分
- channel：列印／螢幕／社群／投影／戶外
- decision context：閱讀情境（趕時間 / 細看 / 簡報中）

---

## §3 核心訊息

**規則**：用一句話寫出這張圖最想讓人記住什麼。

**為什麼**：沒有核心訊息的 prompt 會讓模型亂塞元素，畫面雜亂。

**測試**：一句話讀不出來重點 → 回頭重寫，不要進下一節。

---

## §4 內容素材

**規則**：列出 user-provided assets 與 missing assets。

**必填**：
- 已有：Logo、產品圖、UI 截圖、文案、色值、字型
- 缺的：明確標記，並在 prompt 用 `[PLACEHOLDER: <項目>]` 占位

**為什麼**：缺素材就硬寫會逼模型編造（畫假 logo），破壞品牌識別。

---

## §5 品牌資產優先級

**規則**：依重要性排序：Logo > 產品圖／UI 截圖 >> 色值 >> 字型。

**為什麼**：Logo 錯了整張作廢；色值錯一點通常還能用。資源有限時優先補 Logo。

**動作**：缺 Logo → 停下要素材；只缺字型 → 可用 fallback（如 `system-ui`）

---

## §6 5-10-2-8 品質門檻

**規則**：
- 搜 **5** 條官方來源（不夠 5 不繼續）
- 留 **10** 個 candidate prompts
- 產 **2** 個 finalist
- 迭代 **8** 輪內收斂

**為什麼**：太少候選 = 偏見；太多迭代 = 時間黑洞。5-10-2-8 是經驗值。

**ESC 條件**：第 8 輪還收斂不了 → 回頭檢查 §3（核心訊息是否模糊）。

---

## §7 構圖與版面

**規則**：明示 grid（n 列 m 欄）、hierarchy（主／副／背景）、negative space（佔比約幾成）。

**為什麼**：模型沒被指定就會自由發揮，常出現「滿版資訊牆」這種糟糕排版。

**範例**：「12-column grid, hero takes 8 columns left, KPIs take 4 columns right, ~30% negative space」

---

## §8 Typography

**規則**：font role（heading／body／caption）+ scale（如 48/24/16）+ line-height + 中英文 fallback。

**為什麼**：模型對中文字距常處理差，明示 line-height 與 letter-spacing 能改善很多。

**注意**：中文 prompt 要寫 `"繁體中文"` 而非 `"中文"`（後者會給簡體）。

---

## §9 Color System

**規則**：用 oklch 表達主色，搭配 contrast ratio。HEX 補充。

**為什麼**：oklch 的 lightness 是視覺一致的（HSL 不是），跨色相比較才公平。WCAG AA 需 contrast ≥ 4.5:1 (normal text) / 3:1 (large)。

**範例**：「primary: oklch(55% 0.18 250); on-primary: white; contrast 5.2:1 ✓」

---

## §10 Material and Lighting

**規則**：明示 medium：photography（光源／鏡頭／景深）／3D（材質／燈光／渲染器風格）／illustration（筆觸／媒材）。

**為什麼**：不指定就出「3D-flat-illustration 混合體」這種尷尬產出。

**範例**：「Photo, 50mm prime, f/2.8, soft window light from left, shallow DoF」

---

## §11 Image Endpoint

**規則**：依任務選 endpoint：
- 純生成 → `POST /v1/images/generations`
- 多參考圖 → `POST /v1/images/edits`（image[]）
- 局部 inpaint → `POST /v1/images/edits` + mask（PNG alpha）

**為什麼**：用錯 endpoint 會白花 token。edits 才能保留原圖結構。

---

## §12 Reference Images

**規則**：若用 edits，明示每張參考圖角色（subject / style / layout）與 priority（主／輔）。

**最多**：4 張（更多會讓模型困惑）。

**範例**：「Image 1 (subject, priority): the woman; Image 2 (style ref): the cafe lighting」

---

## §13 Text Rendering

**規則**：所有要出現在圖上的文字用 `"..."` 引號明示，**逐字**列。中文／密集標籤／海報 → 自動跳 `quality=high`。

**為什麼**：模型會把 prompt 內未引號的詞當「描述」而非「要寫的字」，常少寫或漏寫。

**範例**：✅ `Show the in-image text "山川茶事" / "冷泡系列" / "中杯 16 元"`

---

## §14 Anti AI Slop

**規則**：禁用以下 AI slop 慣性產出：
- 紫色漸變背景
- emoji 圖標當資訊圖
- 圓角 card + 左側 border accent 牆
- AI-generated 人臉（除非明確需要 stock-photo style）
- 超寫實但比例詭異的手指

**為什麼**：這些是 LLM/MLLM 訓練資料的偏差殘留，會立刻洩露「AI 做的」並貶低品牌。

**正向動作**：用 `text-wrap: pretty`、CSS Grid、oklch、「」直角引號（中文用）。

---

## §15 Accessibility

**規則**：
- contrast ratio ≥ 4.5:1
- 行動裝置裁切後仍可讀（mobile crop test）
- alt text 思維：閉眼描述能還原內容嗎

**為什麼**：上線後再回頭改 contrast 是地獄。

---

## §16 Output Size

**規則**：`size` 捷徑對應實際 pixel：

| 捷徑 | Pixel | 用途 |
|---|---|---|
| `square` | 1024x1024 | IG／預設 |
| `portrait` | 1024x1536 | 海報／App 截圖 |
| `landscape` | 1536x1024 | 電腦截圖／橫式 banner |
| `2k` | 2048x2048 | 印刷 / paper figure |
| `4k` | 3840x2160 | 戶外大圖 / 螢幕桌布 |

---

## §17 Quality and Budget

**規則**：

| Quality | 單張成本 | 適用 |
|---|---|---|
| `low` | ~$0.005 | 草稿、批量探索 |
| `medium` | ~$0.04 | 風格探索、初步比稿 |
| `high` | ~$0.17 | 含中文／海報／infographic／交付 |

**自動升級觸發**：prompt 含中文文字／海報／密集 in-image text → 自動跳 `high`。

---

## §18 Negative Constraints

**規則**：明示禁用：
- watermark
- fake brand logo
- unreadable text
- 超出 brand guideline 的色票
- 比例詭異的肢體

**為什麼**：模型「沒被禁的就會做」，正面表列不夠。

---

## §19 Final Prompt Audit

**規則**：輸出前跑這份 checklist。**任一項 ✗ 不出 prompt**。

```markdown
## Final Prompt Audit

- [ ] §0  具體品牌／產品／版本前已 WebSearch 驗證
- [ ] §3  核心訊息一句可讀
- [ ] §5  Logo > 產品 > 色值 > 字型 優先級已標
- [ ] §13 in-image text 用 "..." 引號逐字列出
- [ ] §14 反 AI Slop 五項約束都寫進 prompt
- [ ] §16 size 捷徑對應到實際 pixel
- [ ] §17 quality 等級與成本已可見
- [ ] §18 negative constraints 明示
- [ ] Source attribution 保留（gallery-derived prompts）
```

---

## 來源 Attribution

- `gpt_image_2_skill` 的 19 節 prompt 寫作清單：CC BY 4.0
  原始檔：https://github.com/wuyoscar/gpt_image_2_skill/blob/main/skills/gpt-image/references/craft.md
- Huashu Design 的 #0 事實驗證、反 AI Slop、5-10-2-8 品質門檻：本專案內部規範（`docs/huashu-design-SKILL.md`）
