# Forma Studio codebase 健康檢查與下一階段規劃

日期：2026-04-30  
工作目錄：`/Users/jeyengjau/Desktop/APP/forma-studio-v2.5`  
審計方式：只讀檔案、AST 統計、pytest 實跑、Playwright 嘗試執行；未修改既有檔案、未重 build `.app`、未 commit。

---

## 一、執行摘要（用戶 3 分鐘看完）

### 1.1 整體健康度評分

| 維度 | 評分 | 客觀依據 | 主要風險 |
|---|---:|---|---|
| 桌面程式碼 | A- | `desktop/` 18 個 `.py`，app 2686 行；AST 可解析；本次 `67 passed in 0.59s` | PyQt6 GPL-3.0-only 授權、export helper 尚未抽共用層 |
| Web 單檔版 | B+ | `web/forma-studio.html` 3422 行 / 344 KB；gallery 116 條 / 17 類 | 單檔 JSX 已大，Babel runtime/CDN 依賴；本環境 Playwright 被 sandbox 擋住 |
| 測試覆蓋 | A- | 67 pytest 覆蓋 parser、GUI widget、OpenAI client mock、Markdown/PDF exporter | 缺真機 `.app` launch、Keychain 實機 dialog、Web 28 步本次未能重跑 |
| Production readiness | B- | PyInstaller spec、字型 bundle、GitHub Actions 均存在；既有 `desktop/dist/Forma Studio.app` 80 MB | 未簽名、未 notarize、未在本次 font/PDF 後重 build 驗證 |
| 依賴與授權 | C+ | direct deps 版本固定；reportlab BSD、Noto Sans TC OFL | PyQt6 metadata 顯示 GPL-3.0-only，商業分發需商業授權或改 Qt binding 策略 |
| 文件同步 | B- | DEVLOG/HANDOFF 記錄 v3.0 進度完整 | README/HANDOFF/desktop README/web README 有過期狀態與 PASS 數 |

整體評分：**B+**。核心功能與桌面測試健康，production blocker 集中在「授權、簽名 notarize、真機 frozen 驗證」。

決策摘要：現在不是功能失敗狀態，而是「可用 beta → production release」前的硬化階段。

### 1.2 立即必修（blocker）

| Blocker | 嚴重度 | 為什麼阻塞 production |
|---|---:|---|
| PyQt6 授權策略未決 | Critical | `.venv` metadata：`PyQt6 6.11.0 License-Expression: GPL-3.0-only`；若 closed-source / 商業散布，需 Riverbank commercial license 或替代方案 |
| macOS `.app` 未簽名 + 未 notarize | Critical | unsigned app 會被 Gatekeeper 攔截；對外交付不可視為 production-ready |
| Sprint 3C 後未重 build `.app` 驗證 frozen path | Major | PDF exporter 新增 `reportlab` + `NotoSansTC-Regular.ttf`，spec 已加 datas/hiddenimports，但需實際 build/launch 才算閉環 |
| Web Playwright 28 步本次未重跑成功 | Major | 本環境 Chromium launch 被 macOS sandbox 擋住；需用戶本機 shell 重跑確認 |
| README / HANDOFF 狀態過期 | Major | README 仍寫 24 pytest、待實作目錄；對外文件會誤導使用者 |

決策摘要：下一步應先處理 release gate，不建議立刻開大型新功能。

### 1.3 推薦下一個 sprint

推薦：**候選 A：簽名打包 + frozen 驗證 sprint（v3.0.5 release hardening）**。

理由：目前桌面核心測試已過，Markdown/PDF export 已落地；最大風險不是缺功能，而是 `.app` 能否穩定交付、授權能否合規、文件是否可信。Comment mode / PPTX 都會擴大 surface area，應排在 production gate 之後。

決策摘要：下一 sprint 做 A；3D/3E 等至少 3 個真實使用回饋或可編輯 PPTX 明確需求再開。

---

## 二、程式碼健康度

### 2.1 桌面版（13 modules）

桌面實際檔案數：

| 範圍 | 數量 | 行數 |
|---|---:|---:|
| `desktop/main.py` + app 業務模組 | 13 | 2720 |
| `desktop/app/**/*.py` 全部含 `__init__.py` | 17 | 2686 |
| `desktop/tests/**/*.py` | 12 | 1058 |

13 個主要 module 統計：

| Module | 行數 | classes | funcs | branch 節點 | TODO |
|---|---:|---:|---:|---:|---:|
| `desktop/main.py` | 33 | n/a | n/a | n/a | 0 |
| `app/main_window.py` | 276 | 3 | 23 | 13 | 0 |
| `app/api/key_store.py` | 40 | 0 | 3 | 6 | 0 |
| `app/api/openai_client.py` | 198 | 3 | 9 | 20 | 0 |
| `app/pages/brand_settings_tab.py` | 384 | 1 | 21 | 20 | 0 |
| `app/utils/design_memory.py` | 446 | 2 | 17 | 72 | 0 |
| `app/utils/exporters/__init__.py` | 16 | 0 | 0 | 0 | 0 |
| `app/utils/exporters/markdown_exporter.py` | 224 | 2 | 10 | 31 | 0 |
| `app/utils/exporters/pdf_exporter.py` | 375 | 2 | 15 | 43 | 0 |
| `app/widgets/image_edit_panel.py` | 350 | 2 | 24 | 30 | 0 |
| `app/widgets/mask_uploader.py` | 97 | 1 | 7 | 7 | 0 |
| `app/widgets/quality_dial.py` | 104 | 2 | 9 | 9 | 0 |
| `app/widgets/reference_drop_zone.py` | 171 | 2 | 14 | 14 | 0 |

Import graph 結論：

| 項目 | 結果 |
|---|---|
| circular imports | 未發現 local import cycle；主方向為 `main_window -> widgets/pages/utils`、`image_edit_panel -> api/utils/widgets/exporters` |
| dead code heuristic | 全 repo AST 名稱掃描只標出 `ApiKeyBar`、`set_key` 低引用；兩者分別由 Qt runtime / `ApiKeyBar.save_key()` 使用，不判定為 dead code |
| TODO/FIXME | `desktop/app/**/*.py` 全部 0 |
| 複雜度熱點 | `design_memory.py` branch 72、`pdf_exporter.py` branch 43、`markdown_exporter.py` branch 31 |

程式碼觀察：

| 模組 | 健康度 | 說明 |
|---|---:|---|
| `design_memory.py` | B+ | v2.5 6 區塊 + v3 optional 欄位相容性好；parser 邏輯集中但 446 行已接近需要拆 parser/serializer 的門檻 |
| `image_edit_panel.py` | B+ | QThread cleanup 有處理；export 按鈕 busy disable 正確；但 UI 與 export attribution hardcode 在 widget 內 |
| `pdf_exporter.py` | B+ | `_default_font_path()` 有 `_MEIPASS`、`Contents/Resources`、dev path 三段 fallback；但中文換行與 font register 仍需 frozen app 實測 |
| `markdown_exporter.py` | A- | API 與 PDF 大致一致；sidecar PNG 行為簡單可測 |
| `main_window.py` | A- | gallery path fallback 已補；目前 gallery tab 仍是 placeholder，不影響核心 generate/edit |

決策摘要：桌面 codebase 乾淨，下一次 refactor 應只抽 exporters/common helper，不需要大重構。

### 2.2 Web 版（`forma-studio.html` 3422 行）

| 指標 | 數值 |
|---|---:|
| 目前 HTML 行數 | 3422 |
| 目前 HTML 大小 | 344 KB |
| `v2.5-tier1-sprint1` 行數 | 3154 |
| `v2.5-sprint-1.5` 行數 | 3422 |
| `v3.0-sprint-3c` 行數 | 3422 |
| `<script>` tags | 8 |
| Babel JSX block | 1 block / 3357 行 / 193 KB |
| `useState(...)` 次數 | 98 |
| top-level `function` 數 | 25 |
| 未用 state 掃描 | 未掃出明顯 `value/setter` 僅宣告不用的 state |

風險：

| 風險 | 說明 |
|---|---|
| Runtime Babel | 仍依賴 `babel-standalone` + CDN React/Tailwind，適合單檔工具，不適合嚴格 production web app |
| 單檔維護 | 3422 行可接受但已偏大；再加 comment mode 會顯著惡化 |
| Playwright spec 過期 | `.playwright/sprint1-verify.spec.js` 仍有 `expect(meta.total).toBe(66)`，不適合直接當最新 regression suite |
| Service worker | 只在 http/https 註冊；`file://` silent fail 合理 |

決策摘要：Web 版作為單檔工具仍健康；若要做 v3.1 Web export / comment mode，應先把 Playwright spec 更新到 116 條並拆測試策略。

### 2.3 `exporters/` 套件

| 項目 | Markdown | PDF | 評估 |
|---|---|---|---|
| module-level API | `export_markdown(...)` | `export_pdf(...)` | 一致 |
| class API | `MarkdownExporter().export(...)` | `PDFExporter().export(...)` | 一致 |
| metadata | `ExportMetadata` | `PDFExportMetadata` | 名稱不一致但欄位接近 |
| schema version | `SCHEMA_VERSION = 1` | `SCHEMA_VERSION = 1` | 一致 |
| attribution | `source_attribution: list[str]` | `source_attribution: list[str]` | 一致 |
| image handling | sidecar `.png` | embedded image | 符合格式差異 |
| helper 缺口 | `_now_iso`、memory summary、suffix validation、default attribution 重複 | 同左 | 後續可抽 `common.py` |
| test 覆蓋 | `test_exporters.py` 10 tests | `test_pdf_exporter.py` 7 tests | 夠 MVP |

缺漏 helper：

| Helper | 現況 | 建議 |
|---|---|---|
| `default_attribution()` | hardcode 在 `ImageEditPanel` | 抽到 `exporters/common.py`，Web/PPTX 可共用 |
| `summarize_memory()` | Markdown/PDF 各寫一次 | 抽共用，但保留格式層負責 rendering |
| `ensure_suffix()` | 各 exporter 自己檢查 | 可抽 |
| `safe_export_stem()` | PLAN 有寫，未做 | v3.0.5 可補，避免 `forma-export.*` 過於固定 |

決策摘要：exporters 已可用，下一階段只做小型 common helper，不急著引入大型 ExportModel。

### 2.4 設計記憶 schema

| Schema | 現況 |
|---|---|
| v2.5 stable | Brand Identity、Color Tokens、Typography、Visual Rules、Prompt Defaults、Negative Constraints |
| v3 optional | Spacing & Layout、Components、Motion、Voice & Copy |
| 向後相容 | `test_v25_design_md_still_parses` PASS；新欄位 default 為空容器 |
| warning 策略 | typo / empty motion value warning-only，不 crash |
| serializer | v3 optional 有值才 emit，避免空 section |

殘留問題：

| 問題 | 等級 | 說明 |
|---|---:|---|
| doc 寫 9-section，但實際是 10 個 heading（含 Brand Identity） | Low | PLAN 用「v2.5 6 + v3 4 optional」描述較準 |
| Components / Voice 可含 `:`，parser 已修 | Closed | 有專用 `_parse_text_lines()` |
| Motion 空值 warning 已測 | Closed | `test_parse_warns_on_motion_empty_value` |
| GUI 沒有真正 collapsible | Low | PyQt6 用 `QGroupBox + QScrollArea` 折衷，文件若寫 collapsible 需降調 |

決策摘要：schema 相容性健康；不需要 migration，後續只需改善文件措辭與 GUI 易用性。

---

## 三、測試覆蓋

### 3.1 67 pytest 分布

本次實跑命令：

```bash
PYTHONDONTWRITEBYTECODE=1 QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest desktop/tests -q -p no:cacheprovider
```

結果：

```text
67 passed in 0.59s
```

收集命令：

```bash
PYTHONDONTWRITEBYTECODE=1 QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest desktop/tests --collect-only -q -p no:cacheprovider
```

結果：

```text
67 tests collected in 0.22s
```

| Test file | 數量 | 覆蓋主題 | Test names |
|---|---:|---|---|
| `test_design_memory.py` | 9 | v2.5 parser / validate / save-load / prompt inject | `test_parse_design_memory_minimal`, `test_parse_design_memory_three_column_table`, `test_validate_design_memory_requires_brand_name`, `test_save_design_memory_roundtrip`, `test_load_design_memory_missing`, `test_build_system_prompt_injects_negative_constraints`, `test_apply_design_memory_to_prompt`, `test_memory_to_markdown_roundtrip_idempotent`, `test_parse_handles_empty_and_garbage` |
| `test_design_memory_v3.py` | 10 | v3 schema / roundtrip / warnings / back compat | `test_v25_design_md_still_parses`, `test_v3_full_schema_parse`, `test_v3_full_schema_roundtrip`, `test_serializer_skips_empty_v3_sections`, `test_serializer_emits_only_filled_v3_sections`, `test_build_system_prompt_includes_v3_fields`, `test_apply_design_memory_to_prompt_v3`, `test_parse_warns_on_section_typo`, `test_parse_warns_on_motion_empty_value`, `test_parse_with_warnings_back_compat_no_typos` |
| `test_exporters.py` | 10 | Markdown exporter + ImageEditPanel MD button | `test_markdown_export_requires_prompt`, `test_markdown_export_requires_md_extension`, `test_markdown_export_writes_frontmatter`, `test_markdown_export_writes_image_sidecar`, `test_markdown_export_includes_v3_memory`, `test_markdown_export_includes_attribution`, `test_render_markdown_handles_no_memory`, `test_image_edit_panel_export_md_button_state`, `test_markdown_export_includes_prompt_defaults`, `test_markdown_export_overwrites_sidecar` |
| `test_image_edit_panel.py` | 5 | generate/edit validation、quality、memory injection | `test_image_edit_requires_reference`, `test_image_edit_requires_prompt`, `test_image_generate_requires_prompt`, `test_image_generate_uses_quality`, `test_image_panel_set_design_memory` |
| `test_openai_client.py` | 9 | generations/edits/chat body、API error mapping | `test_generate_image_calls_correct_url`, `test_edit_image_uses_edits_endpoint`, `test_edit_image_rejects_zero_or_too_many`, `test_edit_image_rejects_non_png_mask`, `test_generate_image_401_friendly_error`, `test_generate_image_413_friendly_error`, `test_generate_image_429_friendly_error`, `test_enhance_prompt_calls_chat_completions`, `test_init_rejects_empty_key` |
| `test_pdf_exporter.py` | 7 | PDF exporter、font missing、v3 memory、PDF button | `test_pdf_export_requires_prompt`, `test_pdf_export_requires_pdf_suffix`, `test_pdf_export_missing_font_friendly_error`, `test_pdf_export_writes_file`, `test_pdf_export_includes_v3_memory`, `test_pdf_export_metadata_table_optional_rows`, `test_image_edit_panel_export_pdf_button_state` |
| `test_quality_dial.py` | 8 | quality options、cost、suggestion、widget state | `test_quality_options_three_levels`, `test_estimate_image_cost`, `test_estimate_image_cost_unknown`, `test_suggest_quality_for_zh_poster`, `test_suggest_quality_keeps_when_already_high`, `test_suggest_quality_no_change_for_neutral_prompt`, `test_quality_dial_defaults_to_medium`, `test_quality_dial_set_quality_and_cost` |
| `test_smoke.py` | 2 | MainWindow / BrandSettingsTab smoke | `test_main_window_smoke`, `test_brand_settings_tab_smoke` |
| `test_widgets.py` | 7 | mask alpha validation、reference limit、invalid suffix | `test_validate_png_alpha_rejects_non_png`, `test_validate_png_alpha_handles_missing`, `test_validate_png_alpha_rejects_non_alpha_png`, `test_validate_png_alpha_accepts_alpha_png`, `test_reference_drop_zone_limits_to_four`, `test_reference_drop_zone_skips_invalid_suffix`, `test_mask_uploader_clears_on_invalid` |

決策摘要：pytest 覆蓋足以支撐 beta；production 還缺 frozen app 與真機手動流程。

### 3.2 PLAN 提過但沒做的 test 缺口

| 缺口 | 來源 | 風險 |
|---|---|---|
| `.app` frozen launch + export PDF/MD smoke | Sprint 2D / 3C production gate | 字型路徑與 hiddenimports 只能靠 build 後驗證 |
| Keychain 第一次寫入系統對話框 | `keyring.backends.macOS` | pytest mock 無法覆蓋 macOS prompt UX |
| Web Playwright 28 步最新回歸 | Sprint 1.5 | 舊 spec 部分過期；本次 sandbox 無法 launch Chromium |
| PDF 中文 line-break / 長 prompt 視覺 QA | PLAN 3C risk | 目前 test 驗檔存在與內容，不檢查排版品質 |
| Markdown/PDF export file overwrite UX | 已有 Markdown overwrite test；PDF 無同級 UX 測試 | 使用者覆蓋檔案時只靠 QFileDialog |
| GitHub Actions 真跑 | workflow 存在但本次未 trigger | CI 可能因 PyQt6/reportlab/PyInstaller 變更才暴露問題 |

決策摘要：測試缺口集中在整合與發佈，不在單元邏輯。

### 3.3 整合測試 vs 單元測試比例

粗分：

| 類型 | Tests | 比例 | 說明 |
|---|---:|---:|---|
| 單元測試 | 約 52 | 78% | parser、exporter render、client body、quality/mask helper |
| widget / GUI smoke | 約 13 | 19% | Qt widget 狀態、button enable、MainWindow smoke |
| 整合 / E2E | 約 2 | 3% | app smoke；沒有 frozen `.app` E2E |

決策摘要：v3.0.5 應補「少量高價值 E2E」，不是增加更多 parser unit test。

### 3.4 Web 版 28 步 Playwright 是否仍 PASS

本次嘗試：

1. `python3 -m http.server 8765`：失敗，sandbox 不允許 bind port。
2. Node + Playwright `file://.../web/forma-studio.html`：失敗，Chromium launch 被 macOS sandbox 擋住。

錯誤摘要：

```text
PermissionError: [Errno 1] Operation not permitted
browserType.launch: Target page, context or browser has been closed
FATAL: mach_port_rendezvous_mac.cc ... bootstrap_check_in ... Permission denied (1100)
```

因此本次不能客觀宣稱「仍 PASS」。可宣稱的是：**已嘗試執行，但受本次 Codex sandbox 限制，未跑到頁面層。**

建議用戶在一般 Terminal 重跑：

```bash
cd /Users/jeyengjau/Desktop/APP/forma-studio-v2.5
cd web
python3 -m http.server 8765
```

另一個 Terminal：

```bash
cd /Users/jeyengjau/Desktop/APP/forma-studio-v2.5
npx --prefix .playwright playwright test .playwright/sprint1.5A-verify.spec.js .playwright/sprint1.6-verify.spec.js
```

注意：`.playwright/sprint1-verify.spec.js` 目前仍含 `expect(meta.total).toBe(66)`，需更新為 116 或以新 spec 取代，否則會誤報。

決策摘要：Web regression gate 未關閉；release 前必須在非 sandbox 環境重跑或修 spec 後重跑。

---

## 四、Production readiness

### 4.1 `.app` 打包狀態

| 項目 | 狀態 |
|---|---|
| `desktop/build_mac.sh` | 存在；會刪 `build dist` 並重跑 PyInstaller |
| `desktop/forma-studio.spec` | 存在；datas 含 `web/prompt-library`、`assets/fonts` |
| 既有 build artifact | `desktop/dist/Forma Studio.app` 存在，80 MB |
| 本次是否重 build | 否，遵守 audit 要求 |
| dist 總大小 | `desktop/dist` 161 MB |
| build 目錄大小 | `desktop/build` 24 MB |

風險：Sprint 3C 後加入 `reportlab` 與 11.9 MB TTF；雖然 spec 已更新，但沒有本次 build log 不能保證 frozen app 完整。

決策摘要：`.app` 有歷史 build，但 v3.0.5 release 前必須重 build 並手動 export PDF。

### 4.2 字型 bundling path resolve

`_default_font_path()` fallback：

| 順序 | Path | 用途 |
|---:|---|---|
| 1 | `sys._MEIPASS/assets/fonts/NotoSansTC-Regular.ttf` | PyInstaller one-folder / runtime extraction |
| 2 | `Path(_MEIPASS).parent/Resources/assets/fonts/NotoSansTC-Regular.ttf` | macOS `.app` BUNDLE datas |
| 3 | `desktop/assets/fonts/NotoSansTC-Regular.ttf` | 開發環境 |

字型檔案：

| 檔案 | 存在 | 大小 |
|---|---:|---:|
| `desktop/assets/fonts/NotoSansTC-Regular.ttf` | 是 | 11,942,800 bytes / 約 11 MB |

決策摘要：路徑設計合理；唯一未關閉的是 frozen `.app` 實測。

### 4.3 PyInstaller hidden imports

目前 spec hiddenimports：

| 類別 | Hidden imports | 評估 |
|---|---|---|
| app modules | `app.*`、widgets/pages/utils/api | 足夠 |
| keyring | `keyring.backends.macOS`, `Windows`, `SecretService` | 對三平台常見 keyring backend 有覆蓋 |
| reportlab | `reportlab`, `reportlab.pdfbase`, `reportlab.pdfbase.ttfonts` | 基本足夠；Pillow/charset-normalizer 為 reportlab deps 需 build 實測 |

疑點：

| 疑點 | 說明 |
|---|---|
| Windows build 使用同一 macOS `.app` spec | PyInstaller `BUNDLE` 在 Windows job 可能不是理想設計；workflow path 上傳 `desktop/dist/forma-studio`，但 spec 同時定義 `BUNDLE` |
| transitive deps | `httpx`、`anyio`、`httpcore`、`certifi`、`pillow` 未手列；PyInstaller 通常可分析，但需 CI build log |
| icon | `icon=None`，dock icon 不是 production 品質 |

決策摘要：hiddenimports 沒有明顯缺口，但跨平台 build 需 CI 實跑確認，Windows spec 應單獨檢查。

### 4.4 真機 launch 風險

| 風險 | 等級 | 說明 |
|---|---:|---|
| Gatekeeper | Critical | unsigned / unnotarized 外部下載會被攔 |
| Keychain dialog | Major | 第一次 `keyring.set_password` 會有 macOS 系統對話框，需 UX 指引 |
| Dock icon | Minor | `icon=None`，正式產品觀感不足 |
| API key invalid/error | Medium | client error mapping 有 401/413/429，OK |
| Export file permission | Medium | QFileDialog 選路徑後 exporter 會寫檔，OSError 有捕捉 |
| Frozen font path | Major | 未重 build 前不能保證 |

決策摘要：真機風險可控，但必須由用戶手動 launch + export 驗收。

### 4.5 GitHub Actions CI workflow

| 項目 | 狀態 |
|---|---|
| Workflow file | `.github/workflows/desktop-build.yml` |
| Trigger | `workflow_dispatch` only |
| macOS runner | `macos-14` |
| Windows runner | `windows-2022` |
| Python | 3.12 |
| pytest | macOS job 跑 `cd desktop && python -m pytest tests/ -q` |
| artifact retention | 14 days |

能 trigger：**是，手動 trigger 可用**。  
缺口：沒有 push/tag release trigger；沒有 signing/notarize secrets；Windows job 未跑 pytest。

決策摘要：CI 是 artifact build workflow，不是 release workflow。

### 4.6 簽名 + notarize 缺什麼

| 需要資源 | 狀態 | 用途 |
|---|---|---|
| Apple Developer Program | 用戶提供 | Developer ID Application certificate |
| Developer ID Application cert | 缺 | `codesign` |
| App-specific password 或 App Store Connect API key | 缺 | `xcrun notarytool submit` |
| Team ID | 缺 | notarize config |
| Hardened runtime entitlements | 未定義 | 正式 notarize 常需明確設定 |
| `.icns` | 缺 | Dock/Finder icon |
| Release DMG/ZIP 包裝 | 未做 | 對外交付 |

決策摘要：簽名 notarize 不是 code 問題，是用戶資源 + release pipeline 問題。

---

## 五、依賴與授權審計

### 5.1 `desktop/requirements.txt` direct deps

依據：`desktop/requirements.txt` 與 `.venv/bin/python -m pip show ...` metadata。

| Package | Version | License metadata | 角色 | Production 風險 |
|---|---:|---|---|---|
| PyQt6 | 6.11.0 | `GPL-3.0-only` | Desktop GUI | **高**：closed-source / 商業分發需商業授權或改策略 |
| httpx | 0.28.1 | BSD-3-Clause | OpenAI HTTP client | 低 |
| keyring | 25.7.0 | MIT | API key storage | 低；UX 需處理 Keychain prompt |
| reportlab | 4.5.0 | BSD license | PDF export | 低 |
| pytest | 9.0.3 | MIT | test only | 不應打包到 app |
| pytest-qt | 4.5.0 | MIT | test only | 不應打包到 app |
| pytest-asyncio | 1.3.0 | Apache-2.0 | test only | 不應打包到 app |
| pytest-mock | 3.15.1 | MIT | test only | 不應打包到 app |
| respx | 0.22.0 | BSD-3-Clause | test only HTTP mock | 不應打包到 app |

決策摘要：最大授權 blocker 是 PyQt6，不是 reportlab 或 Noto。

### 5.2 第三方 prompt 來源 attribution

| Source | License | 數量 | Attribution 狀態 |
|---|---|---:|---|
| `wuyoscar/gpt_image_2_skill` | CC BY 4.0 | 66 | `gallery-index.json` sources + category/source 欄位 |
| `EvoLinkAI/awesome-gpt-image-2-prompts` | CC BY 4.0 | 50 | `gallery-index.json` sources + per-entry `source.author` |

本次 JSON 掃描：17 個 category JSON 的 prompt 均有可解析 `repo` + `license`，missing count 為 0。

風險：

| 風險 | 說明 |
|---|---|
| Export attribution 太寬 | `ImageEditPanel` export 目前固定列兩個 source；若使用者完全手寫 prompt，PDF/MD 也會列來源，合規上保守但精準度不足 |
| README attribution 未列 EvoLinkAI | README 表格只列 wuyoscar 與 open-codesign；應補 EvoLinkAI |
| CC BY 4.0 作者 | EvoLinkAI 每筆有作者，但 export 預設只列 repo/license，未列具體 author |

決策摘要：repo 內資料 attribution 基本完整；export attribution 應從「固定雙來源」改成「由 prompt/gallery selection 帶出」。

### 5.3 Noto Sans TC TTF（OFL 1.1）

| 項目 | 狀態 |
|---|---|
| 檔案 | `desktop/assets/fonts/NotoSansTC-Regular.ttf` |
| 大小 | 11,942,800 bytes |
| 程式註記 | `pdf_exporter.py` docstring 寫 OFL 1.1 |
| bundle | spec datas 包 `desktop/assets/fonts` |

風險：repo 目前未看到字型 license text 檔隨附；嚴格 audit 時建議加入 `desktop/assets/fonts/LICENSE-OFL.txt` 或在第三方 notices 補來源與授權。

決策摘要：OFL 可散布，但 production 應補明確 notices。

### 5.4 reportlab 4.5.0 授權

`.venv` metadata：

```text
reportlab 4.5.0
License: BSD license (see license.txt for details), Copyright (c) 2000-2025, ReportLab Inc.
```

評估：可接受，需保留 license notice。若打包 `.app`，第三方 notices 應列 reportlab 與其 transitive dependency `pillow` 等。

決策摘要：reportlab 不是 blocker。

### 5.5 嚴格 audit 可能不過的點

| 風險 | 等級 | 補救 |
|---|---:|---|
| PyQt6 GPL-3.0-only | Critical | 取得 commercial license、改 PySide6/LGPL 策略、或將 desktop 發佈模式調整為 GPL-compatible |
| README 未列 EvoLinkAI attribution | Major | 文件補齊 |
| Noto Sans TC 未附 license text | Major | 補 `OFL.txt` / THIRD_PARTY_NOTICES |
| Export attribution 不精準 | Medium | gallery selection 帶 source metadata |
| Test deps 可能被 PyInstaller 收進包 | Medium | build 後檢查 dist、必要時 excludes |

決策摘要：production readiness 的第一張清單應是 legal/readme/notices，不是新功能。

---

## 六、文件健康度

### 6.1 DEVLOG / HANDOFF 是否同步真實狀態

| 文件 | 狀態 | 問題 |
|---|---:|---|
| `DEVLOG.md` | A- | 最新 v3.0 3A/3B/3C 記錄完整；歷史 `ForumaStudio` typo 只作為修復紀錄存在 |
| `HANDOFF.md` | B | 上方表格有 v3.0 67 PASS，但下方仍保留舊「下次繼續 Sprint 1.5 / Sprint 2」內容，讀者可能混淆 |
| `README.md` | C+ | 仍寫 Tier 2 24 PASS、目錄標示待實作；未反映 v3.0 67 PASS / exporters |
| `desktop/README.md` | C | 仍是「Tier 2 待實作」 |
| `web/README.md` | C | 仍是「Tier 1 Sprint 1 待實作」 |

決策摘要：文件不是不可用，但對外 README 已不可信；release 前必修。

### 6.2 PLAN-sprint-1.5 / 2 / 3 是否還是真實 reference

| 文件 | 作為 reference 的有效性 | 說明 |
|---|---:|---|
| `docs/PLAN-sprint-1.5.md` | B | 可作歷史計劃與驗收清單；Playwright spec 需更新到 116 |
| `docs/PLAN-sprint-2.md` | B | 可作桌面 v2.5 設計依據；實作已超過 24 PASS 狀態 |
| `docs/PLAN-sprint-3.md` | A- | 3A-3C 與實作吻合；3D/3E 保持 outline only 正確 |
| `docs/research/v3.0-backlog-evaluation.md` | A- | 路線判斷仍有效，但「PDF/Markdown 待做」已變成「已完成」 |

決策摘要：PLAN 可留作歷史 reference；README/HANDOFF 要承接最新狀態。

### 6.3 README 對外用戶清晰度

優點：

| 優點 | 說明 |
|---|---|
| 快速啟動命令清楚 | Web / desktop / build 命令都有 |
| v1.x 關係說明清楚 | 不會混淆凍結 repo 與 v2.5 repo |
| Attribution 有基本表格 | 但缺 EvoLinkAI |

問題：

| 問題 | 影響 |
|---|---|
| 狀態停在 2026-04-29，未納入 v3.0 完成 | 對外低估功能 |
| Tier 2 寫 24 pytest PASS，實際 67 PASS | 測試基線錯 |
| 目錄結構寫 prompt-library / desktop app 待實作 | 明顯過期 |
| 未提 Markdown/PDF export | 產品價值缺一大塊 |
| 未揭露 PyQt6 授權注意 | production/legal 風險 |

決策摘要：README 應在簽名打包 sprint 第一小時更新，但本 audit 按要求不修改。

### 6.4 殘留 reference 衝突

掃描結果：

| Token | 位置 | 判斷 |
|---|---|---|
| `ForumaStudio` | `DEVLOG.md:173` | 歷史 typo 修復紀錄，可保留 |
| `3137 行` | `DEVLOG.md:605`, `DEVLOG.md:623` | 歷史數字；目前 HTML 3422 行 |
| `24 PASS` | README/HANDOFF/舊 research | 過期，應改為 67 PASS 或標註歷史 |
| `40 PASS` | PLAN 3 baseline | 歷史 baseline，v3 完成後已是 67 |
| `待實作` | README/web README/desktop README | 對外文件需修 |

決策摘要：文件衝突不影響 code，但會影響交付可信度。

---

## 七、下一個 sprint 候選評估（給用戶選）

### 7.1 候選 A：簽名打包（推薦 P0）

| 項目 | 評估 |
|---|---|
| 工時 | 12-24h；若 Apple Developer ID / cert 已備妥，可 1 週內完成 release candidate |
| ROI | 高；直接讓桌面版從 beta 走向可交付 |
| 風險 | PyQt6 授權、notarize entitlements、frozen font path、CI artifact |
| 產出 | signed + notarized `.app`、release checklist、THIRD_PARTY_NOTICES、README 更新 |
| 優先順序 | 1 |

決策摘要：A 是唯一能移除 production blocker 的 sprint。

### 7.2 候選 B：Sprint 3D Comment mode

| 項目 | 評估 |
|---|---|
| 工時 | 36-58h |
| ROI | 中；對「局部修改難描述」有價值 |
| 風險 | element id 不穩、patch 越界、E2E flaky、會擴大 Web 單檔負擔 |
| 啟動條件 | 至少 3 個真實使用者回饋同樣抱怨局部修改 |
| 優先順序 | 4 |

決策摘要：沒有真實回饋前不做。

### 7.3 候選 C：Sprint 3E PPTX export

| 項目 | 評估 |
|---|---|
| 工時 | 20-34h |
| ROI | 中高；教師/行銷/顧問可能需要可編輯簡報 |
| 風險 | layout fidelity、中文字型跨平台、圖片裁切、使用者期待 1:1 還原 |
| 啟動條件 | PDF/Markdown 實機穩定 + 使用者明確要求可編輯 PPTX |
| 優先順序 | 3 |

決策摘要：PPTX 可以做 spike，但不應早於 production hardening。

### 7.4 候選 D：collected user feedback / 實機驗收後再決定

| 項目 | 評估 |
|---|---|
| 工時 | 4-8h 準備問卷/驗收腳本；1-2 週收集 |
| ROI | 高；避免 3D/3E 做錯方向 |
| 風險 | 節奏變慢、需要真實用戶 |
| 產出 | 5-10 份 export 樣本、3-5 位使用者痛點、功能排序 |
| 優先順序 | 2 |

決策摘要：D 應與 A 並行，作為下一個功能 sprint 的依據。

### 7.5 候選 E：v3.1 一般化 Forma Web 版

| 項目 | 評估 |
|---|---|
| 工時 | 40-80h，視是否拆出 build system |
| ROI | 中；可讓 Web 也有 export，降低桌面依賴 |
| 風險 | 單檔 HTML 已大；browser PDF/PPTX/export 權限與檔案處理複雜 |
| 未做項 | 把 desktop Markdown/PDF export model 移植回 Web；更新 Playwright；可能需要 bundler |
| 優先順序 | 5 |

決策摘要：E 是產品方向，不是 immediate sprint；需先決定 Web 是否仍維持單檔。

總排序：**A > D > C > B > E**。

---

## 八、立即動作項（next 1-3 hours）

### 8.1 用戶手動 launch + 操作 export 驗收

```bash
cd /Users/jeyengjau/Desktop/APP/forma-studio-v2.5
source .venv/bin/activate
python desktop/main.py
```

手動檢查：

| 步驟 | 預期 |
|---|---|
| 設定 API Key | macOS Keychain dialog 可理解 |
| 生成新圖 | 成功後 Markdown/PDF button enable |
| 匯出 Markdown | `.md` + sidecar `.png` |
| 匯出 PDF | 中文不亂碼、含 prompt/memory/attribution/footer |
| 關閉 app | 無 QThread destroyed warning |

決策摘要：這是目前最高價值的 30 分鐘驗收。

### 8.2 重 build `.app` 驗證 frozen mode

不要在 audit 中執行；用戶本機執行：

```bash
cd /Users/jeyengjau/Desktop/APP/forma-studio-v2.5
bash desktop/build_mac.sh
open "desktop/dist/Forma Studio.app"
```

PDF 字型驗證：

```bash
find "desktop/dist/Forma Studio.app" -name "NotoSansTC-Regular.ttf" -print
```

如要看 unsigned Gatekeeper 狀態：

```bash
spctl --assess --type execute -vv "desktop/dist/Forma Studio.app"
codesign -dv --verbose=4 "desktop/dist/Forma Studio.app"
```

決策摘要：3C 後 frozen path 未驗證前，不要發 release。

### 8.3 跑一次 Web 版 Playwright 28 步

先修或避開舊 66 條 spec。建議：

```bash
cd /Users/jeyengjau/Desktop/APP/forma-studio-v2.5
cd web
python3 -m http.server 8765
```

另一個 Terminal：

```bash
cd /Users/jeyengjau/Desktop/APP/forma-studio-v2.5
npx --prefix .playwright playwright test .playwright/sprint1.5A-verify.spec.js .playwright/sprint1.6-verify.spec.js
```

若要完整 28 步，需更新 `.playwright/sprint1-verify.spec.js`：

```bash
# 把舊 expect 66 改為 116，並確認 window/global 檢查使用 lexical FORMA_GALLERY
npx --prefix .playwright playwright test .playwright/sprint1-verify.spec.js .playwright/sprint1.5A-verify.spec.js .playwright/sprint1.6-verify.spec.js
```

決策摘要：Web gate 要先修 spec，否則測試結果不可採信。

---

## 九、結論

一句話：**v2.5 + v3.0 整體狀態是 B+；下一步推薦 v3.0.5 production hardening：授權確認、簽名 notarize、frozen `.app` export 驗收、文件同步。**

