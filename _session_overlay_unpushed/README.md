# Forma Studio · v2.5

**跨行業 AI Prompt 生成工具**——律師、會計師、教師、設計師、產品經理、行銷企劃皆可用。

> **這是 v2.5 整合升級版的工作 repo。** v1.0 / v1.1 穩定版本凍結保存於 [`zheyangzhao/forma-studio`](https://github.com/zheyangzhao/forma-studio)（tag: `v1.0-stable` / `v1.1` / `v2.0-spec-frozen`）。

---

## 🆕 Web 版 v2.0 上線（2026-04-30）

`web/forma-studio-v2.html` 是 v1.1 的擴充實驗版，**v1.1 永久凍結並存可用**。
v2.0 在 v1.1 既有 4 大 tab 之外新增 3 個 tab，並把全部 116 條 prompt 中文化、加入 prompt 體檢與風格組合工具。

### 兩個版本怎麼選

| 場景 | 用 v1.1 | 用 v2.0 |
|---|---|---|
| 看診時的穩定工具 | ✅ 推薦 | 🟡 可用 |
| 想瀏覽 116 條 prompt | ❌ 沒功能 | ✅ 📚 提示詞庫 |
| 想體檢自己寫的 prompt | ❌ 沒功能 | ✅ 🩺 體檢 & 增強 |
| 想 chips 組合英文 prompt | ❌ 沒功能 | ✅ 🎬 風格實驗室 |
| 想看中文翻譯的 prompt | ❌ 都英文 | ✅ 中文標題 + 中文摘要 + 中文整段翻譯 |
| 怕介面改動影響工作流 | ✅ 永遠不變 | 🟡 持續迭代中 |

### Web v2.0 七個 tab

1. **🎨 Claude Design** — v1.1 同步：4 區塊 glow（描述需求 → 受眾 → 製圖方式 → 風格生成）
2. **📑 NotebookLM** — v1.1 同步：11 任務 × 20 領域 × 12 框架的知識指令中樞
3. **🖼️ 智慧製圖** — v1.1 同步：自然語言自動分類分流到對應 tab
4. **📚 提示詞庫**（v2.0 新）— 116 條 prompt 完整瀏覽器，中英對照（wuyoscar 66 + EvoLinkAI 50）
5. **🩺 體檢 & 增強**（v2.0 新）— 8 維度本地體檢 + GPT-4o-mini AI 改寫
6. **🎬 風格實驗室**（v2.0 新）— 5 類別 × 4-6 組 chips 自動組英文 prompt
7. **彩蛋 🧪** — v1.1 同步：病毒版 / TED 風格 / 反 AI Slop 診斷 / 四受眾批次

### 快速啟動（3 步驟）

```bash
# 1. 啟動本地 server（在 web/ 目錄）
cd web && python3 -m http.server 8765

# 2. 開瀏覽器
# v1.1 穩定版： http://localhost:8765/forma-studio.html
# v2.0 實驗版： http://localhost:8765/forma-studio-v2.html

# 3.（選填）右上角設 OpenAI API Key — AI 增強功能需要，純體檢免 Key
```

詳細 v2.0 commit 史見 [`CHANGELOG.md`](CHANGELOG.md)。

### v1.1 凍結契約

從 commit `ff8e11d` 起 `web/forma-studio.html` 永久凍結。所有 v2.0 sprint 都會跑 `git diff web/forma-studio.html` 必須為 0 行。
這是**硬約定**：v1.1 是您看診時的友善老朋友，永遠不會被改壞。

---

## 目前狀態（2026-04-30）

| 項目 | 狀態 |
|---|---|
| **Web 版 v2.0**（forma-studio-v2.html）| ✅ Sprint 0–1.8 完成（7 tab / 116 條中文化 / 8 維度體檢 / 5 類別風格組合 / UX 引導 12 項；commits ff8e11d → 6410190）|
| SDD v2.5 規格書 | ✅ 定稿（[`docs/SDD-v2.5-integration-upgrade.md`](docs/SDD-v2.5-integration-upgrade.md)） |
| Tier 1：Web 版升級 | ✅ 完成（116 條 prompt / 17 類 / 雙 CC BY 4.0 source / SKILL.md / craft.md / Claude 一鍵增強鈕；28 步 Playwright PASS，tag `v2.5-sprint-1.5`） |
| Tier 2：PyQt6 桌面版 | ✅ Sprint 2A-2D 完成（18 個 .py / 4 tab / Markdown+PDF export / unsigned .app 80MB，tag `v2.5-sprint-2`） |
| Tier 3：v3.0 schema + Markdown + PDF export | ✅ Sprint 3A+3B+3C 完成（DESIGN.md 9 區塊 / Markdown sidecar PNG / PDF cover+image+memory，tag `v3.0-sprint-3c`） |
| 全套 pytest | ✅ **67 PASS**（design_memory 17 + quality_dial 8 + widgets 7 + openai_client 10 + image_edit_panel 5 + smoke 2 + exporters 10 + pdf_exporter 7 + 1 v3 mismatch placeholder） |
| Web v2.0 Sprint 4 | ⏳ 規劃中（localStorage 持久化：API Key 記憶 / 提示詞收藏 / Style 偏好 / 體檢歷史）|
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
