# 桌面版（v2.5 Tier 2 待實作）

## 狀態

🟡 **Tier 2 Sprint 2 待實作**（Tier 1 完成後啟動）

## 規格

依 [`../docs/SDD-v2.5-integration-upgrade.md`](../docs/SDD-v2.5-integration-upgrade.md) 章節 4 實作。

## v1.0 凍結版本

桌面版 v2.0 規格書與初版骨架保存於：
- [zheyangzhao/forma-studio · `desktop/main.py`](https://github.com/zheyangzhao/forma-studio/blob/v2.0-spec-frozen/desktop/main.py)
- [zheyangzhao/forma-studio · `docs/SDD-desktop-v2.0.md`](https://github.com/zheyangzhao/forma-studio/blob/v2.0-spec-frozen/docs/SDD-desktop-v2.0.md)

## v2.5 增量（v2.0 → v2.5）

| 項目 | 規格章節 | 新增內容 |
|---|---|---|
| GPT Image 2 edits / inpaint | 4.1 | 多參考圖（最多 4 張）+ PNG alpha mask |
| `--quality` 預算撥盤 | 4.2 | low / medium / high 三段成本估算 |
| DESIGN.md 共享記憶 | 4.3 | 品牌 tokens 跨對話注入 system prompt |

## 待實作元件清單

```
desktop/
├── main.py                              # 從 v2.0 移植
├── requirements.txt                     # 從 v2.0 移植 + 新增依賴
└── app/
    ├── api/
    │   └── openai_client.py             # 擴充 client.images.edit() 支援
    ├── pages/
    │   └── brand_settings_tab.py        # DESIGN.md GUI 編輯器
    ├── utils/
    │   └── design_memory.py             # DESIGN.md parse / save / validate
    └── widgets/
        ├── reference_drop_zone.py       # 最多 4 張 reference images 拖放
        ├── mask_uploader.py             # PNG alpha mask 上傳 + 預覽
        ├── image_edit_panel.py          # 整合 drop zone + mask + endpoint 切換
        └── quality_dial.py              # 三段成本撥盤
```

## 實作順序（Sprint 2）

1. `openai_client.py` edit endpoint 擴充
2. `quality_dial.py` 與成本估算函數（先寫，因為 widget 都要用到）
3. `reference_drop_zone.py` + `mask_uploader.py`
4. `image_edit_panel.py` 整合
5. `design_memory.py` parser
6. `brand_settings_tab.py` GUI

## API Key 規範

- 使用 `keyring` 存系統鑰匙圈
- service: `"Forma Studio"`、account: `"openai_api_key"`
- 詳見 [`../CLAUDE.md`](../CLAUDE.md)
