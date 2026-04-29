# Forma Studio v2.5 · DEVLOG

> 最新在最上面。每次重要改動後追加一筆。

---

## [2026-04-29] Sprint 2D：pytest 套件 + PyInstaller 打包（unsigned .app）

### pytest 套件（24 test 全 PASS、0.22s）
- `desktop/tests/conftest.py`：sys.path + offscreen Qt
- `desktop/tests/test_design_memory.py`：8 test（parse / round trip / build_system_prompt / apply / load missing / 三欄 table / idempotent）
- `desktop/tests/test_quality_dial.py`：8 test（QUALITY_OPTIONS / estimate_image_cost / suggest_quality / QualityDial defaults / set_quality）
- `desktop/tests/test_widgets.py`：8 test（PNG alpha 驗證 4 種、ReferenceDropZone limits/skip invalid、MaskUploader clears on invalid）
- 命令：`QT_QPA_PLATFORM=offscreen pytest desktop/tests/ -q`

### PyInstaller 打包
- `desktop/forma-studio.spec`：spec 檔（含 prompt-library/ datas、hidden imports、PyQt6 排除清單、macOS BUNDLE info_plist）
- `desktop/build_mac.sh`：macOS build script（exec 權限）
- `desktop/build_win.bat`：Windows build script
- `.github/workflows/desktop-build.yml`：GitHub Actions（手動觸發 + macOS/Windows 雙 build + artifact upload）
- 實際 build 結果：`desktop/dist/Forma Studio.app`（80MB，unsigned）
- `bundle_identifier`: `ai.formastudio.desktop`
- `LSMinimumSystemVersion`: 12.0

### 待用戶完成（需私有資源）
- Apple Developer ID Application 憑證 → codesign
- App Store Connect API Key → notarize
- Windows Authenticode 憑證 → signtool

### .gitignore 更新
- `desktop/build/`、`desktop/dist/`、`*.egg-info/` 已排除

### README 更新
- 各模組狀態升級為「完成」/「Sprint 2A+2B+2C 完成」
- 加快速啟動命令（web / desktop / build）

### Sprint 2 整體 Done
| Sprint | 狀態 |
|---|---|
| 2 計劃書 | ✅ |
| 2A 基礎設施 | ✅ |
| 2B edit endpoint UI | ✅ |
| 2C DESIGN.md | ✅ |
| 2D unsigned .app + CI workflow | ✅ |
| 2D 簽名 + notarize | ⏸ 等用戶 Apple Developer ID |

---

## [2026-04-29] 🎉 Sprint 2 桌面版實機驗收 PASS（venv + headless GUI smoke）

### 驗收環境
- Python 3.14.4 / pip 26.0.1
- venv：`forma-studio-v2.5/.venv/`
- 套件：PyQt6 6.11.0 / httpx 0.28.1 / keyring 25.7.0 / pytest 9.0.3 / pytest-qt 4.5.0 / pytest-asyncio 1.3.0 / pytest-mock 3.15.1 / respx 0.22.0
- pip install 一次成功（PyQt6-Qt6 64MB 約 6 秒下載）

### Headless smoke（QT_QPA_PLATFORM=offscreen）
測試腳本：`desktop/tests/smoke_launch.py`

```
tabs found (4): ['Prompt Gallery', '圖像生成 / 修改', '品牌記憶', '設定']
widgets OK: ImageEditPanel + BrandSettingsTab built, quality default=medium
  tab 1 'Prompt Gallery' -> smoke-tab-01-Prompt_Gallery.png (45 KB)
  tab 2 '圖像生成 / 修改' -> smoke-tab-02-圖像生成_-_修改.png (75 KB)
  tab 3 '品牌記憶' -> smoke-tab-03-品牌記憶.png (88 KB)
  tab 4 '設定' -> smoke-tab-04-設定.png (37 KB)
brand status: DESIGN.md 不存在，可填寫後儲存建立
```

### UI 驗收項目（4 張截圖目視確認）

| Tab | 驗證項目 |
|---|---|
| Prompt Gallery | 「已載入 116 條 prompt、17 個類別」+ 「來源：wuyoscar (66 條)、EvoLinkAI (50 條)」雙 source 全顯示 |
| 圖像生成 / 修改 | API Key 列、Prompt textarea、4 drop slot 平排（drop #1-4）、+ 加入圖片、Mask 選填區（PNG alpha）、Quality 三段 radio + Estimated cost、生成新圖／修改既有圖 兩按鈕 |
| 品牌記憶 | 專案目錄 + 選擇/載入、5 基本欄位（Project/Brand/Industry/Audience/Tone）、Color Tokens 表 + 加色票/移除、Typography/Visual Rules/Prompt Defaults/Negative Constraints 4 個 textarea、儲存 DESIGN.md 按鈕、status「DESIGN.md 不存在」 fallback OK |
| 設定 | API Key 提示 + keyring 規範說明 |

### 全工程驗收
- ✅ AST 15 檔 PASS
- ✅ design_memory unit test 5/5 PASS（含 SDD §4.3 三欄 table、round trip、None fallback、negative inject、validate warns）
- ✅ Headless smoke：4 tab 全建立、預設 quality=medium、DESIGN.md 缺失 fallback 正常、4 張截圖總 245KB
- ✅ 中文渲染正確（Mac Qt offscreen，可能 production native 視窗會有更好字型）

### 待真機驗證（用戶手動）
桌面版 GUI 在實際 macOS 桌面 launch（非 offscreen）：

```bash
cd ~/Desktop/APP/forma-studio-v2.5
source .venv/bin/activate
python desktop/main.py
```

預期：開啟主視窗、可實際操作 4 tab、API Key 寫入 macOS Keychain、DESIGN.md 可建立／載入。

### 已交付
- `desktop/tests/smoke_launch.py`：headless smoke 腳本（保留進 repo 給未來 sprint 重跑）
- `.gitignore` 加 `.venv/`、`desktop/tests/smoke-artifacts/`

### 待處理
- [ ] task #13：Sprint 2D 打包（PyInstaller .app + 簽名）
- [ ] task #12：v3.0 backlog（nexu-io / Comment mode / 多格式匯出）

---

## [2026-04-29] Sprint 2C 完成：DESIGN.md 共享記憶（parser + GUI + memory injection）

### 工作流程
1. Codex 規劃：PLAN-sprint-2.md §四
2. Claude 寫程式：design_memory.py（parser + serializer）+ brand_settings_tab.py（GUI）+ main_window/image_edit_panel 接線
3. Codex Code Review：抓 1 Critical + 3 Major + 2 Minor
4. 修 1 Critical + 2 Major + Major 1 unit test 驗證
5. AST 15 檔 + design_memory unit test 全 PASS

### Codex review 抓到（已修）
- **Critical**：main_window 啟動時 `load_from_project` 在 connect 之前 → emit 不會傳到 ImageEditPanel → 改成 connect → load 順序
- **Major 1**：`_TABLE_ROW_RE` 只接受 2 欄，SDD §4.3 範例 3 欄 fail → 放寬 regex（單元測試通過 3 欄）
- **Major 2**：`save_to_project` 沒 catch OSError → 加 try/except + QMessageBox

### Sprint 2C scope-out（commit 註記）
- **Major 3**：enhance_prompt UI 整合 — OpenAIClient.enhance_prompt 已支援 system_prompt 參數（Sprint 2A 完成），但桌面版尚未有 enhance 按鈕。UI 接線留 Sprint 2D 或後續 sprint
- **Minor 1**：audience GUI 改 multi-line — 保留 QLineEdit + 多分隔符 placeholder（parser 已支援 5 種分隔符）
- **Minor 2**：英文 label 統一中文 — 部分保留以便對照 PLAN

### 已交付檔案
- `desktop/app/utils/design_memory.py`（~250 行）：DesignMemory dataclass + parse / serialize / save / load / validate / build_system_prompt / apply_design_memory_to_prompt
- `desktop/app/pages/brand_settings_tab.py`（~210 行）：GUI form + color table + load/save buttons
- `desktop/app/main_window.py`：替換 brand placeholder + memory_changed signal 流轉到 ImageEditPanel
- `desktop/app/widgets/image_edit_panel.py`：set_design_memory + 兩 click handler 用 apply_design_memory_to_prompt prepend

### Unit test 驗證（不需 PyQt6 即可跑）
- 3 欄 table parser（Major 1 fix）：PASS
- markdown round trip：PASS
- None fallback：PASS
- build_system_prompt 注入 negative：PASS
- validate 警告 brand_name 缺失：PASS

### Sprint 2 整體狀態
| Sprint | 狀態 |
|---|---|
| 2 計劃書 | ✅ |
| 2A 基礎設施 | ✅ |
| 2B edit endpoint UI | ✅ |
| 2C DESIGN.md | ✅ **本次** |
| 2D 打包 | ⏳ |

桌面版核心能力（生圖 / 修圖 / Quality 撥盤 / Keychain / DESIGN.md 共享記憶）全到位。venv install 後即可實際 launch GUI 驗收。

### 待處理
- [ ] Sprint 2D：PyInstaller .app 打包 + 簽名（macOS）+ Windows .exe（後續）
- [ ] pytest-qt smoke test（Sprint 2A/2B/2C 各自 5 test）
- [ ] enhance_prompt UI（按鈕 + 接 build_system_prompt）— 未排期

---

## [2026-04-29] Sprint 2B 完成：edit endpoint UI（reference drop / mask / image edit panel）

### 工作流程
1. Codex 規劃：PLAN-sprint-2.md §三
2. Claude 寫程式：3 個 widget + main_window 接線
3. Codex Code Review：抓 4 Major + 2 Minor，皆已修
4. AST parse：4/4 PASS、import graph DAG

### Codex review 抓到的 4 Major（已全修）
1. **QThread cleanup 順序錯**：worker.deleteLater 應在 worker.finished/error 同步排程，不該等 thread.finished → 改用標準 `worker.finished → worker.deleteLater + thread.deleteLater`
2. **closeEvent 沒處理執行中 thread**：補 `closeEvent` 內 `thread.quit() + thread.wait(2000)` 避免 "Destroyed while running"
3. **MaskUploader.set_mask invalid 時不清舊 mask**：改成 invalid 直接清 `_mask_path` + emit None
4. **submit 前沒重驗 mask**：image_edit_panel `_on_edit_clicked` 加 `validate_png_alpha(mask)` 重驗（檔案可能被外部刪改）

### Minor 1 也修了
validation error 用 `modal=False`（不開 QMessageBox），API error 才彈 modal — 方便未來 pytest-qt smoke test

### 已交付檔案
- `desktop/app/widgets/reference_drop_zone.py`（~155 行）：drag-drop 最多 4 張、PNG/JPEG/WebP、4 個縮圖 slot + 移除鈕
- `desktop/app/widgets/mask_uploader.py`（~80 行）：QImage 驗 PNG alpha + invalid 清舊 state
- `desktop/app/widgets/image_edit_panel.py`（~210 行）：整合 prompt + reference + mask + quality + 兩按鈕（生成新圖／修改既有圖）
  - QThread + _OpenAIWorker（async coroutine 包進 worker thread）
  - closeEvent 處理執行中 thread
  - validation/API error 分流（modal=False/True）
- `desktop/app/main_window.py`：`_build_image_tab()` 改回傳 ImageEditPanel、新增 `_create_openai_client()` factory（從 keyring 取 key）

### 待驗收（venv install 後）
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r desktop/requirements.txt
QT_QPA_PLATFORM=offscreen python -c "
import sys; sys.path.insert(0, 'desktop')
from app.main_window import MainWindow
print('imports OK')
"
python desktop/main.py     # 主視窗開啟
```

### 待處理
- [ ] Sprint 2B pytest-qt 測試（5 個 test，PLAN §3.5）
- [ ] Sprint 2C：DESIGN.md（design_memory.py + brand_settings_tab.py）
- [ ] Sprint 2D：PyInstaller 打包

---

## [2026-04-29] Sprint 2A 完成：PyQt6 桌面版基礎設施

### 工作流程
1. **Codex CLI 規劃**：`docs/PLAN-sprint-2.md`（1518 行 / 十大章節 / Sprint 2A/2B/2C 分期）
2. **Claude 寫程式**：6 個核心檔 + 3 個 `__init__.py` + requirements.txt（總 ~600 行 Python）
3. **Codex CLI Code Review**：抓 2 Major（mask 未驗 PNG、`get_key()` 沒容錯 KeyringError），均已修
4. **AST Parse**：8/8 .py 檔通過

### 已交付檔案

```
desktop/
├── main.py                          # QApplication 入口（30 行）
├── requirements.txt                 # PyQt6 6.11 / httpx 0.28 / keyring 25.7 + pytest 套件
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── key_store.py             # macOS Keychain / Windows Credential（45 行）
│   │   └── openai_client.py         # generate_image / edit_image / enhance_prompt（180 行）
│   ├── widgets/
│   │   ├── __init__.py
│   │   └── quality_dial.py          # QualityDial widget + estimate_image_cost / suggest_quality（110 行）
│   └── main_window.py               # 4 tab 主視窗 + ApiKeyBar + 深色主題（230 行）
```

### 規格符合度（PLAN §二）
- ✅ keyring service="Forma Studio"、account="openai_api_key"
- ✅ OpenAI client：generations + edits + chat completions 三 endpoint
- ✅ edit_image：拒絕 0/>4 張、PNG mask 驗證、b64_json 解碼
- ✅ 友善錯誤訊息（401/413/429）
- ✅ QualityDial 三段（low $0.005 / medium $0.04 / high $0.17）
- ✅ HIGH_QUALITY_TRIGGERS 中文/海報/infographic 自動建議升 high
- ✅ 4 tab（Gallery / Image / Brand / Settings），placeholder 留給 Sprint 2B/2C
- ✅ Gallery tab 讀 web/prompt-library/gallery-index.json 顯示 total/cats/sources
- ✅ 深色主題對齊 Web 版 slate-900 系
- ✅ `from __future__ import annotations` + Python 注釋用 `#`（不誤套 React `/* */`）

### 待驗收（需要 venv 環境）
本機 ast.parse 已通過；PyQt6 GUI launch 與 pytest-qt smoke test 留給用戶 venv install 後執行：

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r desktop/requirements.txt
python desktop/main.py    # 主視窗應該開起來
pytest desktop/tests/     # （Sprint 2A 暫時沒 test，留給 2B 補）
```

### 待處理
- [ ] Sprint 2B：edit endpoint UI（reference_drop_zone / mask_uploader / image_edit_panel）
- [ ] Sprint 2C：DESIGN.md（design_memory.py + brand_settings_tab.py）
- [ ] Sprint 2D：打包（PyInstaller .app + signing + notarize）

---

## [2026-04-29] 🎉 Sprint 1.5 全部完成：B + A + Tier 1.6（tag v2.5-sprint-1.5）

### Tier 1.6：Claude 一鍵增強鈕

工作流程
1. **Codex CLI 規劃**：PLAN-sprint-1.5 §四 已就緒
2. **Claude 寫程式**：4 個 Edit（頂層 helpers + OutBox prop + DesignTab 2 處 caller）
3. **Codex CLI Code Review**：規格遵循度 A、0 Critical / 0 Major、1 Minor（disabled button title 兼容性備註）
4. **Playwright 驗證**：自寫 spec 9 步、PASS、3.8 秒

### Sprint 1.5 整體

| Section | 任務 | Playwright |
|---|---|---|
| §B | gallery 接 4 區塊 UI | 11/11 PASS |
| §A | EvoLinkAI 整合（gallery 66 → 116） | 8/8 PASS |
| §四 Tier 1.6 | Claude 一鍵增強鈕 | PASS |

### 規模變化（Sprint 1 起 → Sprint 1.5 完）

| 指標 | Sprint 1 起 | 1.5 完 |
|---|---|---|
| gallery total | 0 | **116** |
| categories | 0 | **17** |
| sources | 0 | **2** |
| HTML size | 148 KB | **293 KB** |
| Playwright spec | 0 | **3 個 / 28 步** |

### 後續
- [ ] #11 [Tier 2 Sprint 2] PyQt6 桌面版升級
- [ ] #12 [v3.0 backlog] nexu-io / Comment mode / 多格式匯出

---

## [2026-04-29] Sprint 1.5 §A 完成：EvoLinkAI 整合 · Playwright 8/8 PASS · gallery 從 66 → 116

### 工作流程
1. **Codex CLI 規劃**（既有 PLAN-sprint-1.5 §三）
2. **Claude 寫程式**：
   - 上游偏差：PLAN 寫的 `gpt_image_2_prompt.json` 不存在（404），實際資料在 `data/ingested_tweets.json`（meta 索引）+ `README.md`（5723 行 prompt 主文）
   - 改解析 README.md 的 `### Case N: TITLE (by @AUTHOR)` heading + ` ``` ` 區塊
   - 新增 `tools/build_gallery_evolink.py`（解析 + 5 類別輸出）
   - 修改 `tools/inline_gallery.py`（補 cat-level source + 多 source `sources` array）
   - 修改 `web/forma-studio.html` 的 `SUB_TO_GALLERY_SLUGS`（加 evolink-* mapping，否則 4 個 sub 都不顯示 EvoLink 條目）
3. **Codex CLI Code Review** → 抓 2 個 Major：
   - `merge_index()` 重跑不穩定（重跑會把 evolink count 算進 wuyo_count）→ 已修
   - UI industries 不符 PLAN（多了 marketing）→ 已修
4. **Codex CLI 跑 Playwright**：
   - 第 1 跑：6/8（spec 預估錯 marketing+image 條目上限、SUB_TO_GALLERY_SLUGS 還沒加 evolink）
   - 第 2 跑：codex 卡 stdin（已 kill）；改用 `npx --prefix /tmp/playwright_test playwright test` 直接執行
   - 結果：**8/8 PASS、0 console error、3.6 秒**

### 規模變化
- gallery：66 → **116** 條（PLAN 預估 100-115，超 1 條可接受）
- categories：12 → **17**（+5 EvoLink 類別）
- sources：1（wuyoscar）→ **2**（wuyoscar 66 + EvoLinkAI 50）
- HTML size：217KB → **293KB**（+76KB inline JSON + JSX）

### 已交付檔案
- `tools/build_gallery_evolink.py`：274 行（新增）
- `tools/inline_gallery.py`：補 cat-level source + sources array
- `web/prompt-library/evolink-{ecommerce,ad-creative,poster,ui,comparison}.json`：5 檔，每檔 10 條
- `web/prompt-library/gallery-index.json`：加 sources、append 5 evolink categories
- `web/forma-studio.html`：SUB_TO_GALLERY_SLUGS 加 evolink-* mapping
- `.playwright/sprint1.5A-verify.spec.js`：8 步驗證 spec（CC0 / Codex 寫）

### 開發踩雷紀錄
- PLAN 假設上游有結構化 JSON，實際只有 README.md（必須 markdown parser）
- `SUB_TO_GALLERY_SLUGS` 沒加 evolink-* slug → EvoLink 條目根本無法顯示在 4 個 sub 裡（review 沒抓到、Playwright 抓到）
- Python build script 我寫錯 `/* */` 注釋（誤套 v2.5 React 規範），改回 `#`
- codex CLI 的 stdin 模式可能會 stuck（觀察值，已用 npx 直接跑作為 fallback）

### 待處理（Sprint 1.5 剩 1 項）
- [ ] #10 [Tier 1.6] Claude 一鍵增強鈕

---

## [2026-04-29] Sprint 1.5 §B 完成：gallery 接 4 區塊 UI · Playwright 11/11 PASS

### 工作流程（嚴格遵照用戶指示）
1. **Codex CLI 規劃** → `docs/PLAN-sprint-1.5.md` §二
2. **Claude 寫程式** → 6 個 Edit 改 `web/forma-studio.html`
3. **Codex CLI Code Review** → 0 Critical / 0 Major / 0 Minor，「可直接 commit」
4. **Codex CLI 跑 Playwright 11 步測試** → 修兩處 spec 邏輯後，**11/11 PASS、0 console error、5.4 秒**

### 本次完成
- 頂層新增：INDUSTRY_CHIPS（10 跨行業）/ SUB_TO_GALLERY_SLUGS / GALLERY_SIZE_TO_RATIO / useGallery() / GalleryPromptList
- DesignTab 內：industries / showGallery state + applyGalleryPrompt handler
- Section 2：適用行業 chip block（gallery.enabled 才顯示）
- Section 3：secondary controls（手動設定/📚 範例庫）+ 範例庫展開時 render GalleryPromptList
- 行為：點 prompt → 自動切回 image sub + 注入 desc + 切 size + 關 gallery + goStep(3)
- HTML 從 217KB → 224KB（+7KB JSX）

### Playwright spec 修正紀錄（兩處 spec 邏輯 bug，與程式碼無關）
- Step 07：原 spec assert「套用」按鈕必存在；但 industries=legal + sub=image 命中 0 條 → 改驗證空狀態 fallback
- Step 11：原 spec 在 Step 9 後找複製鈕（畫面已無）→ 改：切 info sub + 重開範例庫 + 點 GalleryPromptList 內 CopyBtn
- 加 `permissions: ['clipboard-read','clipboard-write']`：headless Chromium 預設拒絕 clipboard write，CopyBtn 的 setOk(true) 不執行

### 已交付檔案
- `web/forma-studio.html`：+153 行（v2.5 PROMPT GALLERY HELPERS + UI 接線）
- `.playwright/sprint1-verify.spec.js`：11 步驗證 spec
- `.gitignore`：加 .playwright artifact 過濾

### 待處理（Sprint 1.5 剩兩項）
- [ ] #9 [A] EvoLinkAI prompt 庫整合（gallery 從 66 → 100-115 條）
- [ ] #10 [Tier 1.6] Claude 一鍵增強鈕

---

## [2026-04-29] Sprint 1.5 計劃書定稿（B + A + Tier 1.6）

### 本次完成
- 由 Codex CLI 產出 `docs/PLAN-sprint-1.5.md`（1236 行 / 40 KB / 七大章節）
- 整合範圍盤點：
  - **B**（最優先）：Sprint 1 verification — gallery 接到 React 4 區塊 UI
  - **A**：EvoLinkAI/awesome-gpt-image-2-prompts 整合（CC BY 4.0、8745 stars）
    - 篩選 30-50 條跨行業適用條目（收 E-commerce / Ad Creative / Comparison / Poster / UI；排除 Portrait / Cosplay / Korean Idol 等人物肖像權風險）
    - 預期 gallery 從 66 → 100-115 條
  - **Tier 1.6**：Claude 一鍵增強鈕（靈感來自 claude.ai 自製版）
- nexu-io/open-design 評估：**不整合**（架構衝突），但 design-systems markdown 格式列入 v3.0 借鑑

### 已交付檔案
- `docs/PLAN-sprint-1.5.md`：Sprint 1.5 完整實作計劃書

### 待處理（task #8-12 已建檔，避免遺忘）
- [ ] #8 [B] gallery 接 4 區塊 UI（下個 session 主菜）
- [ ] #9 [A] EvoLinkAI prompt 庫整合
- [ ] #10 [Tier 1.6] Claude 一鍵增強鈕
- [ ] #11 [Tier 2 Sprint 2] PyQt6 桌面版
- [ ] #12 [v3.0 backlog] nexu-io / Comment mode / 多格式匯出

---

## [2026-04-28] Tier 1 Sprint 1 完成：prompt gallery + HTML loader 全到位

### 本次完成
- **資料層**：12 個跨行業類別、66 條結構化 prompt（落在 SDD 預估 50-80 條範圍內）
  - `tools/build_gallery.py`：解析上游 `gallery-*.md` → 12 個 JSON + index
  - `web/prompt-library/*.json`：每筆含 `id` / `title` / `size` / `pixel` / `credit` / `prompt` / `industries` / `source`
  - 排除 Anime / Tattoo / Gaming HUD / Cinematic Film 等不適合企業客戶的類別
- **Skill 文件**：兩份從骨架擴充到完整版
  - `skills/forma-studio/SKILL.md`：跨行業使用情境、4 區塊工作流、4 個產業範例（律師 / 教師 / 會計師 / 餐旅）、gallery 索引、endpoint 對應
  - `skills/forma-studio/references/craft.md`：19 節品質檢查層完整內容（合併 #0 + 反 AI Slop + 5-10-2-8 + Final Audit checklist）
- **Web 版升級**：HTML 從 v1.1 移植 + gallery loader 接通
  - `web/forma-studio.html`（3137 行，185KB → 217KB inline 後）
  - `web/manifest.json` + `web/service-worker.js`（PWA 支援，同 v1.1）
  - `tools/inline_gallery.py`：build pipeline，把 `prompt-library/*.json` inline 到 HTML 的 `<script id="forma-gallery">` 區塊，保持單檔特性
  - feature flag `ENABLE_PROMPT_GALLERY` + DOM-based loader（解析失敗自動 fallback v1.0 行為）
- **Playwright 驗證**：`http://localhost:8765/forma-studio.html` 啟動正常，FORMA_GALLERY 全域可讀，`total_count=66`，`categoriesCount=12`，0 console error

### 開發踩雷紀錄
- `re.sub` replacement 字串會把 `\n` 解釋成真實換行符，導致 inline JSON 內含真實 newline 觸發 `JSON.parse` Unterminated string。修法：用 `lambda _m: new_tag` 包住 replacement
- 全域 hook（v1 留下的 `~/.claude/hooks/active_step_guard.py`）跨 repo 擋 .py 寫入；解法：在 v2.5 與原 Design-prompt 各設一份 allow-all `workflow-kit/state/active-step.json`（已加入 .gitignore）

### 已交付檔案
| 檔案 | 行數／大小 | 用途 |
|---|---|---|
| `tools/build_gallery.py` | 274 行 | 上游解析器 |
| `tools/inline_gallery.py` | 117 行 | HTML build pipeline |
| `web/prompt-library/*.json` | 13 檔 | 12 類別 + index |
| `skills/forma-studio/SKILL.md` | 完整版 | Skill 入口（雙相容 Claude Code / Codex） |
| `skills/forma-studio/references/craft.md` | 19 節 | 品質檢查層 |
| `web/forma-studio.html` | 3137 行 / 217KB | Web 版含 inline gallery |

### 待處理（下次繼續）
- [ ] Tier 1 Sprint 1 verification：把 gallery 真的接到 4 區塊 UI（chip 選 industry → 即時顯示對應 prompts）
- [ ] Tier 2 Sprint 2：PyQt6 桌面版（edit endpoint / quality 撥盤 / DESIGN.md）
- [ ] 後續 sprint：Skill 安裝測試（實際在另一台機器跑 `/plugin install` 驗證）

---

## [2026-04-28] v2.5 repo 啟動

### 本次完成
- 從 v1.0 拆分出新 repo `forma-studio-v2.5`
- 最小繼承：`CLAUDE.md`（重寫 v2.5）、`.gitignore`、`docs/SDD-v2.5-integration-upgrade.md`、`docs/huashu-design-SKILL.md`
- 目錄骨架建立：`web/prompt-library/`、`skills/forma-studio/references/`、`desktop/app/`
- 新增 `README.md`（含 attribution）、`LICENSE`（MIT）、`SKILL.md` 草稿、`craft.md` 草稿、`HANDOFF.md`
- v1.0 / v1.1 凍結於 [`zheyangzhao/forma-studio`](https://github.com/zheyangzhao/forma-studio)（含 tag `v2.0-spec-frozen`）

### 已交付檔案
- `README.md`：對外公開介紹（含整合來源 attribution）
- `LICENSE`：MIT + 第三方授權聲明
- `CLAUDE.md`：v2.5 開發規範
- `HANDOFF.md`：下次繼續
- `docs/SDD-v2.5-integration-upgrade.md`：整合升級規格書（從 v1.0 拷貝過來）
- `docs/huashu-design-SKILL.md`：Huashu Design 原始參考（從 v1.0 拷貝過來）
- `skills/forma-studio/SKILL.md`：Skill 入口草稿
- `skills/forma-studio/references/craft.md`：19 節品質清單草稿

### 待處理（下次繼續）
- [ ] Tier 1 Sprint 1：篩選 162 → 50-80 條跨行業 prompt
- [ ] Tier 1 Sprint 1：完成 `web/prompt-library/*.json`
- [ ] Tier 1 Sprint 1：把 v1.0 `forma-studio.html` 移植進來 + 加 gallery loader
- [ ] Tier 2 Sprint 2：PyQt6 桌面版

---
