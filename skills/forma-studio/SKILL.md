---
name: forma-studio
description: 跨行業 AI prompt 生成工具——把模糊需求轉成可直接餵 GPT-4o-mini / GPT Image 2 / Claude 的高品質提示詞。涵蓋律師、會計師、教師、設計師、產品經理、行銷企劃。沿襲 4 區塊 glow 流程（描述需求→受眾基調→製圖方式→風格生成），整合 162 條結構化 prompt gallery（篩跨行業通用子集）、19 節 craft.md 品質檢查層、20 種設計哲學庫。觸發：使用者說「幫我生 prompt」「我要做海報/簡報/Logo/UI mockup」「給我設計指令」「跨行業通用 prompt」「Forma Studio」「forma-studio」。
---

# Forma Studio

> ⚠️ **狀態：草稿（v2.5 開發中）**。完整能力依 SDD 章節三實作，本檔目前僅描述 skill 入口輪廓，實作細節 TBD。

跨行業 AI prompt 生成工具。從模糊需求 → 完整 AI 設計指令，4 區塊依序引導，內建 20 種設計哲學庫 + 跨行業 prompt gallery。

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

## 何時使用此 Skill

- 使用者描述模糊的設計/視覺/簡報需求，需要結構化 prompt
- 跨行業：律師（提案書）、會計師（年報視覺）、教師（教材視覺）、設計師（mockup）、產品經理（pitch deck）、行銷（廣告素材）
- 需要符合品牌一致性的多輪 prompt 產出
- 需要 #0 事實驗證、反 AI Slop、5-10-2-8 品質門檻檢查

## 主要能力（依 v2.5 規格）

| 能力 | 對應 SDD 章節 | 狀態 |
|---|---|---|
| 4 區塊 glow 流程（描述→受眾→製圖→風格） | v1.0 繼承 | ✅ 規格定稿 |
| 20 種設計哲學庫（5 流派） | v1.0 繼承 | ✅ 規格定稿 |
| 12 個設計品牌參考 | v1.0 繼承 | ✅ 規格定稿 |
| 跨行業 prompt gallery（50-80 條） | 3.1 | 🟡 待實作 |
| craft.md 19 節品質檢查層 | 3.3 | 🟡 待實作（草稿見 references/craft.md） |
| GPT Image 2 generations | 4.1 | 🟡 待實作 |
| GPT Image 2 edits / inpaint（多參考圖 + mask） | 4.1 | 🟡 待實作 |
| `--quality` 預算撥盤（low/medium/high） | 4.2 | 🟡 待實作 |
| DESIGN.md 共享記憶（品牌 tokens） | 4.3 | 🟡 待實作 |

## References

- `references/gallery.md` — prompt gallery 路由索引（v2.5 實作後產出）
- `references/craft.md` — 19 節 prompt 品質檢查層
- `references/gallery-ui-ux.md` 等 — 各類別 prompt 庫（v2.5 實作後產出）

## 設計原則（從 v1.0 繼承）

1. **跨行業通用**：不限定特定行業，所有資料庫設計需通用
2. **API Key BYOK**：使用者自帶 key，session 暫存，不寫 localStorage / 不寫檔
3. **反 AI Slop**：禁紫漸變、emoji 圖標、generic card wall、AI-generated 臉
4. **#0 事實驗證**：具體品牌/產品/版本前必須先 WebSearch 驗證
5. **5-10-2-8 品質門檻**：搜 5 條、留 10 個 candidates、產 2 個 finalist、迭代 8 輪內收斂

## License & Attribution

本 Skill 沿襲 [Forma Studio v2.5 MIT License](https://github.com/zheyangzhao/forma-studio-v2.5/blob/main/LICENSE)。

吸收自外部開源專案的內容保留原 license：
- prompt gallery 條目：CC BY 4.0（來源 [`gpt_image_2_skill`](https://github.com/wuyoscar/gpt_image_2_skill)）
- DESIGN.md 共享記憶模式：MIT（來源 [`open-codesign`](https://github.com/OpenCoworkAI/open-codesign)）
