# Web 版（v2.5 待實作）

## 狀態

🟡 **Tier 1 Sprint 1 待實作**

## 規格

依 [`../docs/SDD-v2.5-integration-upgrade.md`](../docs/SDD-v2.5-integration-upgrade.md) 章節 3 實作。

## v1.0 凍結版本

實作前可參考 v1.0 穩定版：
- [zheyangzhao/forma-studio · `web/forma-studio.html`](https://github.com/zheyangzhao/forma-studio/blob/v1.0-stable/web/forma-studio.html)
- 4 區塊 glow 流程已完成
- 20 種設計哲學 + 12 個設計品牌完整

## v2.5 增量

| 項目 | 變更 |
|---|---|
| `forma-studio.html` | 從 v1.0 移植 + 加 prompt gallery loader |
| `prompt-library/*.json` | 新增：50-80 條跨行業 prompt（CC BY 4.0 attribution） |
| Feature flag | `ENABLE_PROMPT_GALLERY = true` |

## 移植順序

1. 從 v1.0 凍結 repo `git show v1.0-stable:web/forma-studio.html > web/forma-studio.html`
2. 在 HTML 內加 `fetch('prompt-library/gallery-index.json')` 動態載入
3. 加 feature flag 與 fallback：載入失敗自動回退 v1.0 行為
4. 用 `@babel/parser` 驗證 JSX 語法
5. Playwright smoke test 通過後 commit
