# Forma Studio · v2.5

**跨行業 AI Prompt 生成工具**——律師、會計師、教師、設計師、產品經理、行銷企劃皆可用。

> **這是 v2.5 整合升級版的工作 repo。** v1.0 / v1.1 穩定版本凍結保存於 [`zheyangzhao/forma-studio`](https://github.com/zheyangzhao/forma-studio)（tag: `v1.0-stable` / `v1.1` / `v2.0-spec-frozen`）。

---

## 目前狀態

| 項目 | 狀態 |
|---|---|
| SDD v2.5 規格書 | ✅ 定稿（[`docs/SDD-v2.5-integration-upgrade.md`](docs/SDD-v2.5-integration-upgrade.md)） |
| Tier 1：Web 版升級 | 🟡 待實作（prompt gallery / SKILL.md / craft.md） |
| Tier 2：PyQt6 桌面版 | 🟡 待實作（edit endpoint / quality 撥盤 / DESIGN.md） |
| Tier 3：v3.0 評估 | ⏸ Backlog（Comment mode / 多格式匯出） |

---

## v2.5 整合計畫

整合兩個外部開源專案的菁華能力，**不替換**既有 4 區塊 glow 流程與 20 種設計哲學庫，**只擴充**：

### 來源 A：[`gpt_image_2_skill`](https://github.com/wuyoscar/gpt_image_2_skill)（CC BY 4.0）
- 162 條結構化 prompt（28 類）
- OpenAI gpt-image-2 兩個 endpoint（generations + edits/inpaint）
- 19 節 prompt 寫作清單（craft.md）
- `--quality` 預算撥盤（low/medium/high）

### 來源 B：[`open-codesign`](https://github.com/OpenCoworkAI/open-codesign)（MIT）
- 多 Provider BYOK 架構參考
- DESIGN.md 共享記憶模式
- AI-tuned sliders 概念

---

## 目錄結構

```
forma-studio-v2.5/
├── docs/
│   ├── SDD-v2.5-integration-upgrade.md   # 整合升級規格書（1005 行）
│   └── huashu-design-SKILL.md            # Huashu Design 原始參考
├── web/
│   └── prompt-library/                   # 待實作：跨行業 prompt gallery（Tier 1）
├── skills/
│   └── forma-studio/                     # Claude Code / Codex Skill 入口
│       ├── SKILL.md                      # 草稿
│       └── references/
│           └── craft.md                  # 草稿：19 節 prompt 品質清單
└── desktop/
    └── app/                              # 待實作：PyQt6 v2.5（Tier 2）
```

---

## 對既有專案的關係

| Repo | 角色 | 備註 |
|---|---|---|
| [`zheyangzhao/forma-studio`](https://github.com/zheyangzhao/forma-studio) | v1.x 凍結保存 | Web v1.0-stable 已 production-ready，桌面版 SDD v2.0 已定稿 |
| `zheyangzhao/forma-studio-v2.5`（本 repo） | v2.5 開發中 | 整合升級實作 |

**v1.0 用戶不受影響**：原 `web/forma-studio.html` 單檔 HTML 版本維持可用，本 repo 不會破壞既有體驗。

---

## 整合來源 Attribution

本專案吸收以下開源專案的概念與資料，於對應檔案中保留 attribution：

| 來源 | License | 吸收內容 | 標註位置 |
|---|---|---|---|
| `wuyoscar/gpt_image_2_skill` | CC BY 4.0 | prompt gallery、craft.md 19 節清單、quality 撥盤 | `web/prompt-library/*.json` 之 `source` 欄位 + `skills/forma-studio/references/` |
| `OpenCoworkAI/open-codesign` | MIT | DESIGN.md 共享記憶模式、UI sliders 概念 | `desktop/app/utils/design_memory.py` |

---

## License

本 repo 程式碼採 [MIT License](LICENSE)。吸收自上述開源專案的 prompt 與資料維持原 license（CC BY 4.0），分別於檔案內標註。

---

## 開發規範

詳見 [`CLAUDE.md`](CLAUDE.md)。重點：
- React 元件嚴格頂層化（沿襲 v1.0）
- 中文注釋包在 `/* */`
- API Key 一律 BYOK，不 hardcode、不寫 repo
- SKILL.md 雙相容（Claude Code / Codex）
