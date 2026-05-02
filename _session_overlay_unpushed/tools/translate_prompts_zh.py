#!/usr/bin/env python3
"""
v2.0 Sprint 1.7: 用 GPT-4o-mini 把 116 條 English prompt 翻譯成中文。

讀取 web/prompt-library/translations-zh.json，補入 prompts 欄位（id → 中文翻譯）。
跳過已翻譯的條目（重跑安全）。並行 5 條加速。

需要環境變數 OPENAI_API_KEY。
"""
import json
import os
import sys
import glob
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    sys.exit("缺 OPENAI_API_KEY 環境變數")

MODEL = "gpt-4o-mini"
ENDPOINT = "https://api.openai.com/v1/chat/completions"
TRANSLATIONS_FILE = "web/prompt-library/translations-zh.json"

SYSTEM_PROMPT = """你是專業中譯英設計／攝影 prompt 翻譯員。把英文圖像生成 prompt 完整翻譯成繁體中文。

規則：
1. 輸出純繁體中文，每個英文設計詞後面用括號附原文（如「攝影棚柔光（studio softbox lighting）」）只在第一次出現時附上
2. in-image 文字（用引號標出的內容如 "AURAE", "Total balance $12,480.36"）必須完整保留原引號內容，不翻譯
3. 尺寸（1290x2796）、技術參數（28mm lens / 4200K）保留原文
4. 品牌名（Apple、Stripe、AURAE 等虛構品牌）保留原文
5. 不要加任何前言或結語，直接輸出翻譯
6. 翻譯要忠實完整，不省略構圖、材質、色彩、光線細節
7. 用繁體中文（台灣用語），不要簡體
"""


def translate_one(client, item):
    """翻譯單一 prompt，回傳 (id, zh_text) 或 (id, None) 失敗"""
    pid = item["id"]
    en = item["prompt"]
    try:
        resp = client.post(
            ENDPOINT,
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "temperature": 0.2,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": en},
                ],
            },
            timeout=60.0,
        )
        resp.raise_for_status()
        data = resp.json()
        zh = data["choices"][0]["message"]["content"].strip()
        return (pid, zh)
    except Exception as e:
        print(f"  ❌ {pid}: {e}", file=sys.stderr)
        return (pid, None)


def main():
    # 讀取所有 prompt
    files = sorted(glob.glob("web/prompt-library/*.json"))
    all_prompts = []
    for f in files:
        if "gallery-index" in f or "translations" in f:
            continue
        with open(f) as fh:
            d = json.load(fh)
        for p in d.get("prompts", []):
            all_prompts.append({"id": p["id"], "prompt": p["prompt"]})
    print(f"讀到 {len(all_prompts)} 條 prompt")

    # 讀取既有翻譯（已翻譯的跳過）
    with open(TRANSLATIONS_FILE) as fh:
        tz = json.load(fh)
    if "prompts" not in tz:
        tz["prompts"] = {}
    existing = set(tz["prompts"].keys())
    print(f"既有 {len(existing)} 條已翻譯，將翻譯剩餘 {len(all_prompts) - len(existing)} 條")

    todo = [p for p in all_prompts if p["id"] not in existing]
    if not todo:
        print("✅ 全部已翻譯，無需動作")
        return

    # 並行翻譯（5 條同時，避免 rate limit）
    success = 0
    fail = 0
    start = time.time()
    with httpx.Client() as client:
        with ThreadPoolExecutor(max_workers=5) as ex:
            futures = [ex.submit(translate_one, client, p) for p in todo]
            for i, fut in enumerate(as_completed(futures), 1):
                pid, zh = fut.result()
                if zh:
                    tz["prompts"][pid] = zh
                    success += 1
                    print(f"  [{i}/{len(todo)}] ✅ {pid} ({len(zh)} 字)")
                else:
                    fail += 1
                # 每 10 條存一次（中斷可恢復）
                if i % 10 == 0:
                    with open(TRANSLATIONS_FILE, "w") as fh:
                        json.dump(tz, fh, ensure_ascii=False, indent=2)

    # 最終存檔
    tz["schema_version"] = 3
    tz["note"] = "中文標題 + 中文摘要 + 中文整段翻譯。實際生圖請用英文 prompt（AI 對英文最精準）；中文版本僅供使用者理解內容。"
    with open(TRANSLATIONS_FILE, "w") as fh:
        json.dump(tz, fh, ensure_ascii=False, indent=2)

    elapsed = time.time() - start
    print(f"\n完成 · 成功 {success} · 失敗 {fail} · 耗時 {elapsed:.1f} 秒")


if __name__ == "__main__":
    main()
