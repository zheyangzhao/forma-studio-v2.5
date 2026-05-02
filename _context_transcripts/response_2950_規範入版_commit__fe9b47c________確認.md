規範入版（commit `fe9b47c`）。

## 確認的工作流程（CLAUDE.md 已寫入）

```
1. Codex 寫規格書（docs/PLAN-*.md）
   ├─ 不寫程式碼，只寫範圍、決策、驗收
   ├─ 必須含 A/B/C 方案 + Codex 推薦
   └─ 必須含 §驗收清單（Playwright 步驟）

         ↓

2. 你看規格書後決策
   ├─ 選方案 / 改方向
   └─ 確認 §待用戶確認 的點

         ↓

3. Claude 依規格書執行
   ├─ 建 git tag 還原點（≥ 5h sprint）
   ├─ 拆 sub-task（TaskCreate）
   ├─ 實作 + Playwright 驗證
   ├─ JSX 檢查 + v1.1 git diff 檢查
   └─ commit（含旅程驗收結果）
```

## 例外（不需走 Codex 規劃）

- 文案微調 / typo / 1 行 bug fix（< 30 分鐘）
- 你明確說「直接動手」「不用 Codex」
- 純 docs 更新（README / CHANGELOG）

## 附歷史教訓在文件裡（讓未來不再犯）

- 早期 Claude 直接動手做桌面版 → 你說「差十萬八千里」
- 你兩次明確要求「請 Codex CLI 先規劃」
- Codex 自己有否決能力（8 領域方向被自己否決並重寫）

---

接下來你想做什麼，我會嚴格按這個流程：
1. 你說想要 X
2. 我寫 Codex prompt → Codex 產 `docs/PLAN-X.md`
3. 你看規格書點頭
4. 我才動手做 + Playwright 驗證 + commit

如果只是文案 / 小 bug fix，我會問你「這個算例外嗎，要直接做還是走 Codex」。