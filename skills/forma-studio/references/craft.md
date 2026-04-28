# Forma Studio · Prompt 品質檢查層（craft.md）

> ⚠️ **狀態：草稿（v2.5 Tier 1 待實作）**。完整內容依 SDD 章節 3.3 實作，本檔目前僅列章節骨架。

合併三層規則：
- `gpt_image_2_skill` 的 19 節 prompt 寫作清單（CC BY 4.0）
- Forma Studio v1.0 的「#0 事實驗證」「反 AI Slop」「5-10-2-8 品質門檻」

---

## 19 節合併清單

| # | 章節 | 必填輸出 | 來源 |
|---:|---|---|---|
| 0 | 事實驗證先於假設 | 是否需要 WebSearch、待驗證項目 | Huashu #0 |
| 1 | 任務意圖 | image / edit / infographic / prototype / brand | gpt_image_2 §1 |
| 2 | 受眾與使用場景 | audience、channel、decision context | gpt_image_2 §2 |
| 3 | 核心訊息 | one-sentence message | gpt_image_2 §3 |
| 4 | 內容素材 | user-provided assets / missing assets | gpt_image_2 §4 |
| 5 | 品牌資產優先級 | Logo / product / UI / color / font | Huashu 5-10-2-8 |
| 6 | 5-10-2-8 門檻 | 搜 5 候 10 選 2 迭 8 | Huashu 5-10-2-8 |
| 7 | 構圖與版面 | grid、hierarchy、negative space | gpt_image_2 §5 |
| 8 | typography | font role、scale、line-height | gpt_image_2 §6 |
| 9 | color system | oklch / HEX / contrast | gpt_image_2 §7 |
| 10 | material and lighting | photography / 3D / illustration constraints | gpt_image_2 §8 |
| 11 | image endpoint | generations / edits / mask | gpt_image_2 §9 |
| 12 | reference images | image count、role、priority | gpt_image_2 §10 |
| 13 | text rendering | 中文文字、海報、infographic 品質提高 | gpt_image_2 §11 |
| 14 | anti AI Slop | 禁紫漸變、emoji 圖標、generic card wall | Huashu 反 AI Slop |
| 15 | accessibility | contrast、readability、mobile crop | gpt_image_2 §13 |
| 16 | output size | size shortcut + pixel target | gpt_image_2 §14 |
| 17 | quality and budget | low / medium / high | gpt_image_2 §15 |
| 18 | negative constraints | watermark、fake UI、unreadable text | gpt_image_2 §16 |
| 19 | final prompt audit | 檢查缺漏、輸出最終 prompt | gpt_image_2 §19 |

---

## Final Prompt Audit（每次輸出前 checklist）

```markdown
## Final Prompt Audit

Before output, check:
- [ ] If specific brand/product/version is mentioned, verification step is explicit.（#0）
- [ ] Logo/product/UI asset priority is stated.（5-10-2-8）
- [ ] Anti AI Slop constraints are concrete, not generic.（反 AI Slop）
- [ ] Quality level and estimated cost are visible.（17）
- [ ] Size shortcut maps to a real API size.（16）
- [ ] Source attribution is preserved for gallery-derived prompts.
```

---

## 後續實作（Tier 1 Sprint 1）

每個章節（0-19）需展開為：
- 何時觸發
- 必填欄位
- 範例（good vs bad）
- 對應 SDD 條目

**目前是骨架，完整內容待 v2.5 Tier 1 Sprint 1 產出。**

---

## 來源 Attribution

- `gpt_image_2_skill` 的 19 節 prompt 寫作清單：CC BY 4.0
  原始檔：https://github.com/wuyoscar/gpt_image_2_skill/blob/main/skills/gpt-image/references/craft.md
- Huashu Design 的 #0 事實驗證、反 AI Slop、5-10-2-8 品質門檻：本專案內部規範（`docs/huashu-design-SKILL.md`）
