"""
inline_gallery.py — 把 web/prompt-library/*.json 內容注入 web/forma-studio.html
                    的 <script id="forma-gallery"> 區塊，產出 self-contained 單檔。

Usage:
    python3 tools/inline_gallery.py [--source <html>] [--lib <dir>]

預設：
    source = web/forma-studio.html
    lib    = web/prompt-library/

執行後會就地覆寫 source HTML 的 forma-gallery script tag 內容。
原檔變更前先在 stderr 印出舊 size / 新 size 與 prompt 條數，方便檢查。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

GALLERY_TAG_PATTERN = re.compile(
    r'<script id="forma-gallery" type="application/json">.*?</script>',
    re.DOTALL,
)


def build_inline_payload(lib_dir: Path) -> dict:
    """讀 gallery-index.json，把每個類別的 prompts 內聯進去。"""
    index_path = lib_dir / "gallery-index.json"
    if not index_path.exists():
        raise FileNotFoundError(f"gallery-index.json 不存在於 {lib_dir}")

    index = json.loads(index_path.read_text(encoding="utf-8"))

    inlined_categories = []
    for cat_meta in index.get("categories", []):
        cat_path = lib_dir / cat_meta["file"]
        if not cat_path.exists():
            print(f"  warn: {cat_meta['file']} 不存在，略過", file=sys.stderr)
            continue
        cat_data = json.loads(cat_path.read_text(encoding="utf-8"))
        inlined_categories.append(
            {
                "slug": cat_meta["slug"],
                "category": cat_meta["category"],
                "title_zh": cat_meta["title_zh"],
                "industries": cat_meta["industries"],
                "use_cases": cat_meta["use_cases"],
                "count": cat_meta["count"],
                "prompts": cat_data.get("prompts", []),
            }
        )

    return {
        "schema_version": index.get("schema_version", 1),
        "source": index.get("source", {}),
        "categories": inlined_categories,
        "total_count": index.get("total_count", 0),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "web" / "forma-studio.html",
        help="目標 HTML（預設 web/forma-studio.html）",
    )
    parser.add_argument(
        "--lib",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "web" / "prompt-library",
        help="prompt library 目錄（預設 web/prompt-library/）",
    )
    args = parser.parse_args()

    src: Path = args.source
    lib: Path = args.lib

    if not src.exists():
        print(f"error: source HTML 不存在：{src}", file=sys.stderr)
        return 2

    payload = build_inline_payload(lib)

    # 產出最小化 JSON（不縮排、ensure_ascii=False 保留中文）
    payload_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

    # 安全處理：JSON 內若含 </script> 會破壞 HTML parser，做 backslash 轉義
    safe_json = payload_json.replace("</script>", r"<\/script>")

    new_tag = (
        f'<script id="forma-gallery" type="application/json">{safe_json}</script>'
    )

    html_old = src.read_text(encoding="utf-8")
    if not GALLERY_TAG_PATTERN.search(html_old):
        print(
            "error: 找不到 <script id=\"forma-gallery\"> 區塊，"
            "請確認 source HTML 已加 placeholder",
            file=sys.stderr,
        )
        return 3

    # 注意：用 lambda 包住，避免 re.sub 把 replacement 內的 \n / \\ 當 backref 解釋
    html_new, count = GALLERY_TAG_PATTERN.subn(lambda _m: new_tag, html_old, count=1)

    src.write_text(html_new, encoding="utf-8")

    old_size = len(html_old)
    new_size = len(html_new)
    delta_kb = (new_size - old_size) / 1024
    print(f"  注入完成：{count} 個 tag")
    print(f"  HTML size：{old_size:,} → {new_size:,} bytes (+{delta_kb:.1f} KB)")
    print(
        f"  Gallery：{len(payload['categories'])} 類別、"
        f"{payload['total_count']} 條 prompt"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
