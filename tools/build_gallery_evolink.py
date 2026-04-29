"""
build_gallery_evolink.py — Forma Studio v2.5 Tier 1.5 EvoLinkAI 整合

從 EvoLinkAI/awesome-gpt-image-2-prompts 的 README.md 解析 case 條目，
按 section 分 5 類輸出到 web/prompt-library/evolink-*.json，
並把 wuyoscar 既有 gallery-index 升級為多 source 索引。

Usage:
    python3 tools/build_gallery_evolink.py [--readme <path>] [--out <dir>]
                                            [--max-per-category 10]

預設讀 /tmp/upstream-galleries/evolink-README.md，
寫 web/prompt-library/evolink-*.json，並 in-place 更新 gallery-index.json。

對應 PLAN-sprint-1.5 §三規格。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

UPSTREAM_REPO = "EvoLinkAI/awesome-gpt-image-2-prompts"
UPSTREAM_LICENSE = "CC BY 4.0"
UPSTREAM_URL = "https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts"

# README section → 輸出規格（依 PLAN-sprint-1.5 §3.2）
SECTION_MAP: dict[str, dict] = {
    "E-commerce Cases": {
        "slug": "evolink-ecommerce",
        "category": "EvoLinkAI · E-commerce",
        "title_zh": "電商與商品素材",
        "industries": ["marketing", "retail", "hospitality", "general"],
        "use_cases": ["電商主圖", "商品包裝", "廣告主圖"],
    },
    "Ad Creative Cases": {
        "slug": "evolink-ad-creative",
        "category": "EvoLinkAI · Ad Creative",
        "title_zh": "廣告創意素材",
        "industries": ["marketing", "design", "general"],
        "use_cases": ["廣告 visual", "品牌活動素材", "促銷文宣"],
    },
    "Poster & Illustration Cases": {
        "slug": "evolink-poster",
        "category": "EvoLinkAI · Poster & Illustration",
        "title_zh": "海報與插畫",
        "industries": ["marketing", "events", "design"],
        "use_cases": ["活動海報", "宣傳插畫", "視覺主視覺"],
    },
    "UI & Social Media Mockup Cases": {
        "slug": "evolink-ui",
        "category": "EvoLinkAI · UI & Social Media",
        "title_zh": "UI 與社群素材",
        # PLAN §3.2 規定 UI Mockup industries = product/design（不含 marketing）
        "industries": ["product", "design"],
        "use_cases": ["App / Web mockup", "社群圖卡"],
    },
    "Comparison & Community Examples": {
        "slug": "evolink-comparison",
        "category": "EvoLinkAI · Comparison & Community",
        "title_zh": "比較與社群範例",
        "industries": ["marketing", "education", "product"],
        "use_cases": ["A/B 對照", "Before/After", "社群示範"],
    },
    # 排除（PLAN §3.2 已決議）
    "Portrait & Photography Cases": None,
    "Character Design Cases": None,
}

# 從 README heading 推 size 預設（無明確 metadata 時）
DEFAULT_SIZE_BY_SLUG = {
    "evolink-ecommerce":  "square",
    "evolink-ad-creative":"square",
    "evolink-poster":     "portrait",
    "evolink-ui":         "portrait",
    "evolink-comparison": "landscape",
}

SECTION_RE = re.compile(r"^##\s+(.+?)\s*$")
CASE_RE = re.compile(
    r"^###\s+Case\s+(\d+):\s+\[([^\]]+)\]\([^)]+\)\s+\(by\s+\[(@[A-Za-z0-9_]+)\]"
)
CODE_FENCE_RE = re.compile(r"^```")


@dataclass
class EvoEntry:
    id: str
    no: int
    title: str
    size: str
    pixel: str
    credit: str
    prompt: str
    industries: list
    source: dict


def parse_readme(readme_path: Path) -> list[dict]:
    """解析 README → list of dict：section / case_no / title / author / prompt"""
    if not readme_path.exists():
        raise FileNotFoundError(f"README 不存在：{readme_path}")
    text = readme_path.read_text(encoding="utf-8")
    lines = text.split("\n")

    cases: list[dict] = []
    current_section: str | None = None
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        sec_match = SECTION_RE.match(line)
        if sec_match:
            current_section = sec_match.group(1).strip()
            i += 1
            continue

        case_match = CASE_RE.match(line)
        if case_match and current_section:
            case_no = int(case_match.group(1))
            title = case_match.group(2).strip()
            author = case_match.group(3)

            # 從本行往後找第一個 ``` 開始的區塊（可能不只一個，取第一個）
            j = i + 1
            prompt: str | None = None
            while j < n:
                if CASE_RE.match(lines[j]) or SECTION_RE.match(lines[j]):
                    break
                if CODE_FENCE_RE.match(lines[j]):
                    # 起始 fence
                    fence_start = j + 1
                    j += 1
                    body: list[str] = []
                    while j < n and not CODE_FENCE_RE.match(lines[j]):
                        body.append(lines[j])
                        j += 1
                    # j 落在結尾 fence 上
                    prompt = "\n".join(body).strip()
                    j += 1
                    break
                j += 1

            cases.append({
                "section": current_section,
                "case_no": case_no,
                "title": title,
                "author": author,
                "prompt": prompt or "",
            })
            i = j
            continue

        i += 1

    return cases


def make_entry(raw: dict, slug: str, idx_in_cat: int) -> EvoEntry:
    case_no = raw["case_no"]
    short = slug.replace("evolink-", "")
    entry_id = f"evolink-{short}-{case_no:03d}"
    size = DEFAULT_SIZE_BY_SLUG.get(slug, "square")
    industries = SECTION_MAP[raw["section"]]["industries"]

    return EvoEntry(
        id=entry_id,
        no=case_no,
        title=raw["title"],
        size=size,
        pixel="",
        credit=f"Author: {raw['author']}",
        prompt=raw["prompt"],
        industries=industries,
        source={
            "repo": UPSTREAM_REPO,
            "license": UPSTREAM_LICENSE,
            "author": raw["author"],
            "url": UPSTREAM_URL,
        },
    )


def build_category_json(slug: str, meta: dict, entries: list[EvoEntry]) -> dict:
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
            "url": UPSTREAM_URL,
        },
        "count": len(entries),
        "prompts": [asdict(e) for e in entries],
    }


def merge_index(out_dir: Path, new_categories: list[dict]) -> dict:
    """讀既有 gallery-index.json，新增 sources 欄位，append 新 categories。"""
    idx_path = out_dir / "gallery-index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))

    # 先移除既有 evolink-* 條目（重跑穩定性）
    idx["categories"] = [c for c in idx.get("categories", []) if not c["slug"].startswith("evolink-")]

    # 再統計剩下的 wuyoscar source count（避免把舊的 evolink count 算進來）
    wuyo_count = sum(c.get("count", 0) for c in idx["categories"])

    # append 新 categories
    new_total = 0
    for cat in new_categories:
        idx["categories"].append({
            "slug": cat["slug"],
            "category": cat["category"],
            "title_zh": cat["title_zh"],
            "industries": cat["industries"],
            "use_cases": cat["use_cases"],
            "count": cat["count"],
            "file": f"{cat['slug']}.json",
        })
        new_total += cat["count"]

    # sources 多 source 標頭（PLAN §3.4）
    idx["sources"] = [
        {
            "repo": "wuyoscar/gpt_image_2_skill",
            "license": "CC BY 4.0",
            "count": wuyo_count,
        },
        {
            "repo": UPSTREAM_REPO,
            "license": UPSTREAM_LICENSE,
            "count": new_total,
        },
    ]
    idx["total_count"] = wuyo_count + new_total
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return idx


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readme", type=Path,
                        default=Path("/tmp/upstream-galleries/evolink-README.md"))
    parser.add_argument("--out", type=Path,
                        default=Path(__file__).resolve().parent.parent / "web" / "prompt-library")
    parser.add_argument("--max-per-category", type=int, default=10,
                        help="每個 EvoLink category 最多保留多少條")
    args = parser.parse_args()

    readme: Path = args.readme
    out_dir: Path = args.out
    cap: int = args.max_per_category

    cases = parse_readme(readme)
    print(f"  上游解析：{len(cases)} 個 case")

    # 按 section 分桶
    bucket: dict[str, list[dict]] = {}
    skipped = 0
    for c in cases:
        meta = SECTION_MAP.get(c["section"])
        if meta is None:
            skipped += 1
            continue
        if not c["prompt"]:
            print(f"  warn: case {c['case_no']} ({c['section']}) 無 prompt，略過", file=sys.stderr)
            continue
        bucket.setdefault(c["section"], []).append(c)

    print(f"  收：{sum(len(v) for v in bucket.values())} / 不收：{skipped}")

    # 對每個 bucket 取前 N 條（避免條目太多）
    new_categories = []
    for section_name, items in bucket.items():
        meta = SECTION_MAP[section_name]
        slug = meta["slug"]
        chosen = items[:cap]
        entries = [make_entry(c, slug, i) for i, c in enumerate(chosen)]
        cat_json = build_category_json(slug, meta, entries)
        out_path = out_dir / f"{slug}.json"
        out_path.write_text(
            json.dumps(cat_json, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"  ok  {slug}: {len(entries)} 條 -> {out_path.name}")
        new_categories.append(cat_json)

    # 更新 gallery-index.json（含 sources）
    final_idx = merge_index(out_dir, new_categories)

    new_count = sum(c["count"] for c in new_categories)
    print()
    print(f"完成：EvoLink 新增 {len(new_categories)} 類別、{new_count} 條 prompt")
    print(f"全 gallery：{len(final_idx['categories'])} 類別、{final_idx['total_count']} 條")
    print(f"輸出：{out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
