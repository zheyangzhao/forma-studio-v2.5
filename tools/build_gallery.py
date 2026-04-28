"""
build_gallery.py — Forma Studio v2.5 Tier 1 prompt gallery builder

從 wuyoscar/gpt_image_2_skill 上游 gallery-*.md 解析出 prompt 條目，
加上跨行業 `industries` 標籤後輸出到 web/prompt-library/*.json。

Usage:
    python3 tools/build_gallery.py [--upstream <dir>] [--out <dir>]

預設讀 /tmp/upstream-galleries/，寫到 web/prompt-library/。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

UPSTREAM_REPO = "wuyoscar/gpt_image_2_skill"
UPSTREAM_LICENSE = "CC BY 4.0"
UPSTREAM_BASE_URL = (
    "https://github.com/wuyoscar/gpt_image_2_skill/blob/main/skills/gpt-image/references"
)

CATEGORY_META: dict[str, dict] = {
    "ui-ux-mockups": {
        "category": "UI/UX Mockups",
        "title_zh": "UI/UX 介面設計",
        "industries": ["product", "design", "marketing", "legal", "education", "general"],
        "use_cases": ["產品 mockup", "提案展示", "App 概念稿", "Web 平台 demo"],
    },
    "typography-and-posters": {
        "category": "Typography & Posters",
        "title_zh": "排版與海報",
        "industries": ["marketing", "events", "design", "education", "general"],
        "use_cases": ["活動海報", "展覽宣傳", "課程招募", "品牌主視覺"],
    },
    "infographics-and-field-guides": {
        "category": "Infographics & Field Guides",
        "title_zh": "資訊圖表與圖鑑",
        "industries": ["education", "legal", "accounting", "research", "general"],
        "use_cases": ["流程圖", "年報視覺", "教材插圖", "研究摘要圖"],
    },
    "brand-systems-and-identity": {
        "category": "Brand Systems & Identity",
        "title_zh": "品牌系統與識別",
        "industries": ["design", "marketing", "general"],
        "use_cases": ["品牌指引展示", "Logo 系統", "識別頁"],
    },
    "edit-endpoint-showcase": {
        "category": "Edit Endpoint Showcase",
        "title_zh": "圖像編修示範",
        "industries": ["design", "marketing", "general"],
        "use_cases": ["既有海報換場景", "多參考圖合成", "局部 inpaint"],
    },
    "photography": {
        "category": "Photography",
        "title_zh": "商業攝影",
        "industries": ["marketing", "real_estate", "hospitality", "retail", "general"],
        "use_cases": ["產品攝影", "空間氛圍", "場景情境"],
    },
    "product-and-food": {
        "category": "Product & Food",
        "title_zh": "產品與食物",
        "industries": ["marketing", "retail", "hospitality", "general"],
        "use_cases": ["商品包裝", "餐飲菜單", "電商素材"],
    },
    "data-visualization": {
        "category": "Data Visualization",
        "title_zh": "資料視覺化",
        "industries": ["accounting", "research", "education", "product", "general"],
        "use_cases": ["年報圖表", "研究數據", "儀表板示意"],
    },
    "architecture-and-interior": {
        "category": "Architecture & Interior",
        "title_zh": "建築與室內",
        "industries": ["real_estate", "design", "hospitality", "general"],
        "use_cases": ["建案概念", "空間提案", "氛圍渲染"],
    },
    "technical-illustration": {
        "category": "Technical Illustration",
        "title_zh": "技術插圖",
        "industries": ["engineering", "manufacturing", "education", "general"],
        "use_cases": ["產品爆炸圖", "原理示意", "操作手冊插畫"],
    },
    "cinematic-and-animation": {
        "category": "Cinematic & Animation",
        "title_zh": "電影感與動畫",
        "industries": ["marketing", "entertainment", "general"],
        "use_cases": ["廣告分鏡", "形象短片靜幀", "活動主視覺"],
    },
    "scientific-and-educational": {
        "category": "Scientific & Educational",
        "title_zh": "科學與教育",
        "industries": ["education", "research", "general"],
        "use_cases": ["教材插圖", "概念示意", "知識圖卡"],
    },
}


@dataclass
class PromptEntry:
    id: str
    no: int
    title: str
    size: str
    pixel: str
    credit: str
    prompt: str


ENTRY_HEAD = re.compile(r"^###\s+No\.\s+(\d+)\s+·\s+(.+?)\s*$", re.MULTILINE)
META_LINE = re.compile(r"^-\s+Metadata:\s+(.+?)\s*$", re.MULTILINE)
SIZE_TOKEN = re.compile(r"`(portrait|landscape|square|wide|tall|1k|2k|4k)`")
PIXEL_TOKEN = re.compile(r"`(\d{3,4}x\d{3,4})`")
TEXT_BLOCK = re.compile(r"```text\s*\n([\s\S]*?)\n```", re.MULTILINE)


def parse_metadata(meta_line: str) -> tuple[str, str, str]:
    size_match = SIZE_TOKEN.search(meta_line)
    pixel_match = PIXEL_TOKEN.search(meta_line)
    size = size_match.group(1) if size_match else ""
    pixel = pixel_match.group(1) if pixel_match else ""

    if "Curated" in meta_line:
        credit = "Curated"
    elif "Author:" in meta_line:
        author_match = re.search(r"Author:\s*([^·\n]+?)(?:\s*·|$)", meta_line)
        credit = f"Author: {author_match.group(1).strip()}" if author_match else "Author"
    else:
        credit = "Unspecified"

    return size, pixel, credit


def parse_gallery_md(md_path: Path) -> list[PromptEntry]:
    text = md_path.read_text(encoding="utf-8")
    entries: list[PromptEntry] = []

    heads = list(ENTRY_HEAD.finditer(text))
    for i, head in enumerate(heads):
        no = int(head.group(1))
        title = head.group(2).strip()

        start = head.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[start:end]

        meta_match = META_LINE.search(body)
        if not meta_match:
            print(f"  No.{no} 缺 Metadata，略過", file=sys.stderr)
            continue
        size, pixel, credit = parse_metadata(meta_match.group(1))

        text_match = TEXT_BLOCK.search(body)
        if not text_match:
            print(f"  No.{no} 缺 prompt text，略過", file=sys.stderr)
            continue
        prompt_text = text_match.group(1).strip()

        slug = md_path.stem.replace("gallery-", "")
        entry_id = f"{slug}-{no:03d}"

        entries.append(
            PromptEntry(
                id=entry_id,
                no=no,
                title=title,
                size=size,
                pixel=pixel,
                credit=credit,
                prompt=prompt_text,
            )
        )

    return entries


def build_category_json(slug: str, entries: list[PromptEntry]) -> dict:
    meta = CATEGORY_META[slug]
    return {
        "schema_version": 1,
        "slug": slug,
        "category": meta["category"],
        "title_zh": meta["title_zh"],
        "industries": meta["industries"],
        "use_cases": meta["use_cases"],
        "source": {
            "repo": UPSTREAM_REPO,
            "license": UPSTREAM_LICENSE,
            "url": f"{UPSTREAM_BASE_URL}/gallery-{slug}.md",
        },
        "count": len(entries),
        "prompts": [asdict(e) for e in entries],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--upstream",
        type=Path,
        default=Path("/tmp/upstream-galleries"),
        help="上游 gallery-*.md 來源目錄",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "web" / "prompt-library",
        help="輸出目錄",
    )
    args = parser.parse_args()

    upstream: Path = args.upstream
    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    if not upstream.is_dir():
        print(f"upstream dir not found: {upstream}", file=sys.stderr)
        return 1

    index = {
        "schema_version": 1,
        "source": {
            "repo": UPSTREAM_REPO,
            "license": UPSTREAM_LICENSE,
            "base_url": UPSTREAM_BASE_URL,
        },
        "categories": [],
        "total_count": 0,
    }

    total = 0
    for slug, meta in CATEGORY_META.items():
        md_path = upstream / f"gallery-{slug}.md"
        if not md_path.exists():
            print(f"  skip {slug}: 上游檔案不存在")
            continue

        entries = parse_gallery_md(md_path)
        if not entries:
            print(f"  skip {slug}: 解析後 0 條")
            continue

        out_path = out_dir / f"{slug}.json"
        cat_data = build_category_json(slug, entries)
        out_path.write_text(
            json.dumps(cat_data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"  ok  {slug}: {len(entries)} 條 -> {out_path.name}")

        index["categories"].append(
            {
                "slug": slug,
                "category": meta["category"],
                "title_zh": meta["title_zh"],
                "industries": meta["industries"],
                "use_cases": meta["use_cases"],
                "count": len(entries),
                "file": f"{slug}.json",
            }
        )
        total += len(entries)

    index["total_count"] = total
    index_path = out_dir / "gallery-index.json"
    index_path.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print()
    print(f"完成：{len(index['categories'])} 個類別、{total} 條 prompt")
    print(f"輸出：{out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
