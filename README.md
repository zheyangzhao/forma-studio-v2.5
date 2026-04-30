# Forma Studio · v2.5

**跨行業 AI Prompt 生成工具**——律師、會計師、教師、設計師、產品經理、行銷企劃皆可用。

> **這是 v2.5 整合升級版的工作 repo。** v1.0 / v1.1 穩定版本凍結保存於 [`zheyangzhao/forma-studio`](https://github.com/zheyangzhao/forma-studio)（tag: `v1.0-stable` / `v1.1` / `v2.0-spec-frozen`）。

---

## 目前狀態（2026-04-29）

| 項目 | 狀態 |
|---|---|
| SDD v2.5 規格書 | ✅ 定稿（[`docs/SDD-v2.5-integration-upgrade.md`](docs/SDD-v2.5-integration-upgrade.md)） |
| Tier 1：Web 版升級 | ✅ 完成（116 條 prompt / 17 類 / 雙 CC BY 4.0 source / SKILL.md / craft.md / Claude 一鍵增強鈕；28 步 Playwright PASS，tag `v2.5-sprint-1.5`） |
| Tier 2：PyQt6 桌面版 | ✅ Sprint 2A-2D 完成（18 個 .py / 4 tab / Markdown+PDF export / unsigned .app 80MB，tag `v2.5-sprint-2`） |
| Tier 3：v3.0 schema + Markdown + PDF export | ✅ Sprint 3A+3B+3C 完成（DESIGN.md 9 區塊 / Markdown sidecar PNG / PDF cover+image+memory，tag `v3.0-sprint-3c`） |
| 全套 pytest | ✅ **67 PASS**（design_memory 17 + quality_dial 8 + widgets 7 + openai_client 10 + image_edit_panel 5 + smoke 2 + exporters 10 + pdf_exporter 7 + 1 v3 mismatch placeholder） |
| Production hardening | 🟡 進行中（README 同步、.app 重 build 驗證、PyQt6 GPL 授權策略、簽名 + notarize 待 Apple Developer ID） |
| v3.0.5 Backlog | ⏸ Sprint 3D Comment mode（outline）/ Sprint 3E PPTX export（outline） |

### Web 版快速啟動

```bash
cd web && python3 -m http.server 8765
# 瀏覽器開 http://localhost:8765/forma-studio.html
```

### 桌面版快速啟動

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r desktop/requirements.txt
python desktop/main.py
```

### 桌面版打包（macOS）

```bash
bash desktop/build_mac.sh
# 產出 desktop/dist/Forma Studio.app（80 MB unsigned）
```

### Python 版本矩陣

| 環境 | Python | 用途 |
|---|---|---|
| 本機開發 / smoke | 3.12+（實測 3.14.4 OK） | 開 venv、`python desktop/main.py` |
| CI（GitHub Actions） | 3.12 | macOS / Windows build artifact |
| pytest | 同本機 | `QT_QPA_PLATFORM=offscreen pytest desktop/tests/` |

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
