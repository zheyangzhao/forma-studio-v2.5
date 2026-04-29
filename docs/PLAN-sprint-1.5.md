# Forma Studio v2.5 · Sprint 1.5 實作計劃書

**版本**：v2.5 Sprint 1.5  
**日期**：2026-04-29  
**工作目錄**：`/Users/jeyengjau/Desktop/APP/forma-studio-v2.5`  
**輸出檔案**：`docs/PLAN-sprint-1.5.md`  
**基準狀態**：Tier 1 Sprint 1 已完成，`FORMA_GALLERY.total_count = 66`，但尚未接到 React 4 區塊 UI。  

---

## 一、Sprint 1.5 範圍與優先順序

### 1.1 為什麼需要 Sprint 1.5

Sprint 1 已完成資料層、Skill 文件與 HTML loader，但 Web 主流程還沒有使用 gallery 資料。現在 `web/forma-studio.html` 只做到：

| 層 | 現況 | 缺口 | Sprint 1.5 處理 |
|---|---|---|---|
| Gallery loader | `<script id="forma-gallery">` 已 inline | React UI 未消費資料 | B |
| `FORMA_GALLERY` | 全域可讀，66 條 | 沒有 hook / filter | B |
| 4 區塊 glow | v1.0 流程可用 | prompt 範例無法注入 textarea | B |
| 上游資料 | wuyoscar 66 條 | EvoLinkAI 尚未整合 | A |
| Prompt 輸出 | 只有複製 | 沒有 craft.md §19 一鍵增強 | Tier 1.6 |

Sprint 1.5 的定位不是重寫 Web 版，而是把 Sprint 1 已完成的資料接上既有使用流程，再做第二資料源擴充與一個小型文字增強能力。

可執行檢查：

```bash
cd /Users/jeyengjau/Desktop/APP/forma-studio-v2.5
python3 -m http.server 8765 -d web
# browser: http://localhost:8765/forma-studio.html
```

### 1.2 範圍 vs scope-out

| 優先序 | 項目 | Sprint 1.5 狀態 | 主要檔案 | 說明 |
|---:|---|---|---|---|
| 1 | B：gallery 接 UI | 必做 | `web/forma-studio.html` | 驗證 Sprint 1 成果是否真正可用 |
| 2 | A：EvoLinkAI 整合 | 必做 | `tools/build_gallery_evolink.py`, `web/prompt-library/*.json` | 擴充 gallery 到 100-115 條 |
| 3 | Tier 1.6：AI 增強鈕 | 必做但排第三 | `web/forma-studio.html` | 小型文字 API 能力，不阻塞 gallery |
| - | PyQt6 桌面版 | Scope out | `desktop/**` | 移到 Tier 2 Sprint 2 |
| - | Comment mode | Scope out | TBD | v3.0 評估 |
| - | 多格式匯出 | Scope out | TBD | v3.0 評估 |
| - | 多 Provider BYOK | Scope out | TBD | v3.0 評估 |
| - | 實際 GitHub commit/tag | 本計劃書不執行 | git | 本文件只列建議順序 |

Sprint 1.5 預期改動樹：

```text
forma-studio-v2.5/
├── web/
│   ├── forma-studio.html                  # B + Tier 1.6 實作點
│   └── prompt-library/
│       ├── gallery-index.json             # A 更新
│       ├── evolink-ecommerce.json         # A 新增
│       ├── evolink-ad-creative.json       # A 新增
│       ├── evolink-comparison.json        # A 新增
│       ├── evolink-poster.json            # A 新增
│       └── evolink-ui.json                # A 新增
├── tools/
│   ├── build_gallery.py                   # 既有 schema 參考，不改核心行為
│   ├── build_gallery_evolink.py           # A 新增
│   └── inline_gallery.py                  # A 後重跑
└── .playwright/
    ├── sprint1-verify-01.png
    └── sprint1-verify-11.png
```

### 1.3 預估工時與里程碑

| 里程碑 | 範圍 | 預估 | 產出 | Gate |
|---|---|---:|---|---|
| M1 | B：UI 接線 | 1.0-1.5 天 | hook、chips、library tab、注入、Playwright 11 圖 | JSX parse + 0 console error |
| M2 | A：EvoLinkAI parsing | 1.0 天 | parser + 5 個 JSON + index | total_count 100-115 |
| M3 | A：inline + UI 驗證 | 0.5 天 | HTML inline 到約 280KB | 兩個 source 都可 filter |
| M4 | Tier 1.6 | 0.5-1.0 天 | `EnhanceBtn` + flag + fallback | API key gating + 0 console error |
| M5 | 收尾 | 0.5 天 | DEVLOG/HANDOFF 後續更新、tag | 不在本計劃書執行 |

建議總工時：3.5-4.5 天。B 必須先完成，因為 A 只是增加資料量；如果 UI filter 沒先驗證，新增資料只會增加 debug 面積。

---

## 二、B：Sprint 1 verification（gallery 接 UI）

### 2.1 useGallery() hook 設計

`useGallery()` 放在 `web/forma-studio.html` 的 `<script type="text/babel">` 區塊內，與 `CopyBtn`、`OutBox`、`SubTab` 同層級。不得放在 `DesignTab()` 內部，符合 v1.0「禁止 nested component with hooks」規範。

| 項目 | 規格 |
|---|---|
| 函數位置 | 頂層函數，`const ENABLE_PROMPT_GALLERY` 之後 |
| 輸入 | 無，讀全域 `FORMA_GALLERY` |
| 回傳 | `enabled`, `categories`, `prompts`, `filterByIndustries`, `filterBySub` |
| fallback | `ENABLE_PROMPT_GALLERY=false` 時回傳空陣列 |
| schema | category 層 industries，prompt 層補上 category metadata |

資料正規化：

```javascript
function useGallery() {
  const gallery = ENABLE_PROMPT_GALLERY ? FORMA_GALLERY : null;

  const categories = gallery?.categories || [];
  const prompts = categories.flatMap(cat =>
    (cat.prompts || []).map(p => ({
      ...p,
      category_slug: cat.slug,
      category: cat.category,
      title_zh: cat.title_zh,
      industries: cat.industries || [],
      source: p.source || gallery.source || cat.source || null,
    }))
  );

  const filterByIndustries = (industries = []) => {
    if (!industries.length) return prompts;
    return prompts.filter(p => p.industries.some(x => industries.includes(x)));
  };

  const filterBySub = (sub, list = prompts) => {
    const slugs = SUB_TO_GALLERY_SLUGS[sub] || [];
    return list.filter(p => slugs.includes(p.category_slug));
  };

  return {
    enabled: !!gallery,
    categories,
    prompts,
    filterByIndustries,
    filterBySub,
  };
}
```

子頁籤對應表：

```javascript
const SUB_TO_GALLERY_SLUGS = {
  image: [
    'photography',
    'product-and-food',
    'cinematic-and-animation',
    'scientific-and-educational',
    'typography-and-posters',
  ],
  proto: [
    'ui-ux-mockups',
    'brand-systems-and-identity',
  ],
  info: [
    'infographics-and-field-guides',
    'data-visualization',
    'technical-illustration',
    'scientific-and-educational',
  ],
  brand: [
    'brand-systems-and-identity',
    'edit-endpoint-showcase',
    'typography-and-posters',
  ],
};
```

驗證指令：

```bash
npx --yes @babel/parser web/forma-studio.html --plugins jsx
```

如果直接 parse HTML 不合工具預期，改抽出 Babel script 後 parse：

```bash
node - <<'NODE'
const fs = require('fs');
const parser = require('@babel/parser');
const html = fs.readFileSync('web/forma-studio.html', 'utf8');
const m = html.match(/<script type="text\/babel">([\s\S]*?)<\/script>/);
parser.parse(m[1], { sourceType: 'script', plugins: ['jsx'] });
console.log('JSX parse ok');
NODE
```

### 2.2 區塊 2：industries chip

在 `DesignTab()` 的 Section 2「受眾與基調」內新增一排跨行業 chip，狀態放在 `DesignTab()` 頂層 state。

| UI label | industry value | 預期主要命中 |
|---|---|---|
| 律師 | `legal` | infographics, UI, education/general |
| 教師 | `education` | scientific, infographics, posters |
| 會計師 | `accounting` | data visualization, infographics |
| 設計 | `design` | UI, brand, poster |
| 行銷 | `marketing` | poster, photography, product |
| 產品 | `product` | UI, data visualization |
| 不動產 | `real_estate` | architecture, photography |
| 餐旅 | `hospitality` | product food, architecture, photography |
| 研究 | `research` | scientific, data visualization |
| 通用 | `general` | 所有通用 fallback |

新增 state：

```javascript
const [industries, setIndustries] = useState([]);
```

chip 範例：

```jsx
<div className="mb-4">
  <div className="flex items-center gap-1.5 mb-2">
    <span className="text-xs font-bold text-slate-300">適用行業</span>
    <span className="text-xs text-slate-500">可多選 · 影響範例庫過濾</span>
    {industries.length > 0 && (
      <span className="ml-auto text-xs text-emerald-400">{industries.length} 項</span>
    )}
  </div>
  <div className="flex flex-wrap gap-1.5">
    {INDUSTRY_CHIPS.map(o => (
      <button
        key={o.id}
        onClick={() => setIndustries(prev =>
          prev.includes(o.id) ? prev.filter(x => x !== o.id) : [...prev, o.id]
        )}
        className={industries.includes(o.id) ? '...' : '...'}
      >
        {o.label}
      </button>
    ))}
  </div>
</div>
```

實作約束：

| 約束 | 原因 |
|---|---|
| 不移除既有 `who/feel/hasRef` | 保留 v1.0 受眾與基調流程 |
| industry chip 是 additive | 不改既有分析器輸出 |
| `general` 不預設自動選 | 避免一開始結果過多 |
| 多選使用 OR filter | 任一 industry 命中即顯示 |

### 2.3 區塊 3：範例庫子分頁

在 Section 3 既有 4 個子頁籤下方新增 `📚 範例庫` 分頁。不要把主子頁籤改成 5 個；做成每個子頁籤內的 secondary mode，避免破壞目前 `sub` 決策。

建議 state：

```javascript
const [showGallery, setShowGallery] = useState(false);
```

Section 3 視覺結構：

```text
Section 3 選擇製圖方式
├── primary tabs
│   ├── image  圖像生成
│   ├── proto  設計稿/原型
│   ├── info   資訊圖表
│   └── brand  品牌與評審
├── secondary controls
│   ├── 手動設定
│   └── 📚 範例庫
└── content
    ├── existing pane
    └── GalleryPromptList
```

新增元件建議放頂層：

```jsx
function GalleryPromptList({ prompts, onUse }) {
  if (!prompts.length) {
    return (
      <div className="rounded-xl border border-slate-700 bg-slate-900/50 p-4 text-xs text-slate-500">
        目前條件沒有符合的範例。請調整適用行業或切換製圖方式。
      </div>
    );
  }

  return (
    <div className="grid gap-2">
      {prompts.map(p => (
        <div key={p.id} className="rounded-xl border border-slate-700 bg-slate-900/50 p-3">
          <div className="flex items-start justify-between gap-3">
            <div className="min-w-0">
              <div className="text-sm font-bold text-slate-100">{p.title}</div>
              <div className="text-xs text-slate-500 mt-0.5">
                {p.size || 'size n/a'} · {p.pixel || 'pixel n/a'} · {p.credit || 'credit n/a'}
              </div>
            </div>
            <div className="flex gap-1.5 shrink-0">
              <button onClick={() => onUse(p)} className="...">套用</button>
              <CopyBtn text={p.prompt} sm />
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-2 leading-relaxed">
            {p.prompt.slice(0, 80)}{p.prompt.length > 80 ? '...' : ''}
          </p>
        </div>
      ))}
    </div>
  );
}
```

過濾邏輯：

```javascript
const gallery = useGallery();
const industryFiltered = gallery.filterByIndustries(industries);
const visibleGalleryPrompts = gallery.filterBySub(sub, industryFiltered);
```

驗收用 count：

| 條件 | 預期 |
|---|---|
| 未選 industry + `sub=image` | 顯示 image 對應類別 prompt |
| 選 `legal` + `sub=info` | 顯示 legal + info 類別，約 7 條上下 |
| 選 `design` + `sub=proto` | 顯示 UI/brand 類別 |
| `ENABLE_PROMPT_GALLERY=false` | 不顯示範例庫入口 |

### 2.4 點 prompt 注入 textarea

點 prompt 後要填進該區塊既有需求描述 textarea：

| sub | 目標 state / textarea | 現況 |
|---|---|---|
| `image` | `desc` | Section 3 圖像描述 |
| `proto` | `ProtoPane` 內部 state | 目前獨立元件，需開放 prop 或保守只注入 `desc` 後切 image |
| `info` | `InfoPane` 內部 state | 同上 |
| `brand` | `BrandPane` 內部 state | 同上 |

建議 Sprint 1.5 最小安全策略：

| 階段 | 做法 | 原因 |
|---|---|---|
| B1 | 所有 gallery prompt 先注入 `DesignTab.desc` | 不改 `ProtoPane/InfoPane/BrandPane` 內部 state 邊界 |
| B1 | `sub` 維持當前頁籤 | 使用者可看 prompt，再生成對應指令 |
| B2 | 如時間足夠，再把 `ProtoPane/InfoPane/BrandPane` 改為 controlled props | 改動較大，需回歸測試 |

注入 handler：

```javascript
const applyGalleryPrompt = p => {
  setDesc(p.prompt);
  setCategory(mapGallerySlugToCategory(p.category_slug));
  if (p.size) setSize(mapGallerySizeToRatio(p.size));
  if (p.category_slug && SUB_TO_GALLERY_SLUGS[sub]?.includes(p.category_slug)) {
    setShowGallery(false);
  }
  goStep(3);
};
```

size mapping：

```javascript
const GALLERY_SIZE_TO_RATIO = {
  square: '1:1',
  portrait: '9:16',
  tall: '9:16',
  landscape: '16:9',
  wide: '16:9',
  '1k': '1:1',
  '2k': '1:1',
  '4k': '16:9',
};
```

複製按鈕直接沿用 `CopyBtn`，不新增第二份 clipboard 實作。

### 2.5 Playwright 11 步測試清單

測試檔建議臨時放 `.playwright/sprint1-verify.spec.js`，驗證後可不納入 commit；截圖依需求保留在 `.playwright/sprint1-verify-XX.png`。

| Step | 操作 | 驗證 | 截圖 |
|---:|---|---|---|
| 01 | 載入 `http://localhost:8765/forma-studio.html` | page title + no console error | `sprint1-verify-01.png` |
| 02 | 輸入 API key | UI 顯示 key 已填，session only | `sprint1-verify-02.png` |
| 03 | 區塊 1 輸入描述 | `textarea` value 正確 | `sprint1-verify-03.png` |
| 04 | 前往區塊 2 | glow 移到 Section 2 | `sprint1-verify-04.png` |
| 05 | 選 industries：`legal` | chip active | `sprint1-verify-05.png` |
| 06 | 前往區塊 3 | primary tab 可切換 | `sprint1-verify-06.png` |
| 07 | 開 `📚 範例庫` | visible prompt count > 0 | `sprint1-verify-07.png` |
| 08 | 切 `info` 子頁籤 | count 約 7 條，含 legal | `sprint1-verify-08.png` |
| 09 | 點第一筆 prompt 套用 | `desc` textarea 填入 prompt | `sprint1-verify-09.png` |
| 10 | 前往區塊 4 選風格並生成 | `OutBox` 出現 | `sprint1-verify-10.png` |
| 11 | 點複製 | button 顯示已複製 | `sprint1-verify-11.png` |

Playwright 骨架：

```javascript
const { test, expect } = require('@playwright/test');

test('Sprint 1.5 gallery UI verification', async ({ page }) => {
  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });

  await page.goto('http://localhost:8765/forma-studio.html');
  await expect(page).toHaveTitle(/Forma Studio/);
  await page.screenshot({ path: '.playwright/sprint1-verify-01.png', fullPage: true });

  await page.evaluate(() => ({
    total: window.FORMA_GALLERY?.total_count,
    enabled: window.ENABLE_PROMPT_GALLERY,
  }));

  /* 後續依實際 selector 補齊。 */
  expect(errors).toEqual([]);
});
```

啟動指令：

```bash
python3 -m http.server 8765 -d web
npx playwright test .playwright/sprint1-verify.spec.js --headed
```

### 2.6 驗收標準與回滾

| Gate | 指令 / 檢查 | 通過標準 |
|---|---|---|
| JSX parse | `@babel/parser` | 無 syntax error |
| console | Playwright console listener | `errors.length === 0` |
| loader | `window.FORMA_GALLERY.total_count` | `66` |
| flag | 手動改 `ENABLE_PROMPT_GALLERY=false` 測試 | 4 區塊可正常跑 |
| legal filter | `filterByIndustries(['legal'])` | 約 7 條，且每筆含 `legal` |
| UI flow | 11 步截圖 | 每步有圖，無卡死 |

回滾策略：

```text
回滾單位：只回退 web/forma-studio.html 中 B 相關區塊
保留：<script id="forma-gallery"> inline JSON
保留：tools/inline_gallery.py
關閉方式：const ENABLE_PROMPT_GALLERY = false;
```

---

## 三、A：EvoLinkAI 整合

### 3.1 上游資料源與 license

EvoLinkAI 作為第二 prompt source。主要資料源是 repo 根目錄機讀 JSON。

| 項目 | 值 |
|---|---|
| repo | `EvoLinkAI/awesome-gpt-image-2-prompts` |
| license | `CC BY 4.0` |
| upstream file | `gpt_image_2_prompt.json` |
| 預估上游量 | 167+ cases |
| Sprint 1.5 保留量 | 30-50 條 |
| 必填 attribution | 每筆 `source.author` |

抓取指令：

```bash
mkdir -p /tmp/upstream-galleries
curl -sL https://raw.githubusercontent.com/EvoLinkAI/awesome-gpt-image-2-prompts/main/gpt_image_2_prompt.json \
  -o /tmp/upstream-galleries/evolink-prompts.json
```

授權欄位落點：

```json
{
  "source": {
    "repo": "EvoLinkAI/awesome-gpt-image-2-prompts",
    "license": "CC BY 4.0",
    "author": "@example_handle",
    "url": "https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts"
  }
}
```

實作備註：上游「今天還在更新」，不要把 2026-04-29 的 count 寫死進 parser。parser 應以分類與規則篩選，最後由驗收檢查 `total_count` 區間。

### 3.2 篩選規則（收／不收對照表）

| EvoLinkAI 類別 | 收／不收 | 輸出檔 | industries | 原因 |
|---|---|---|---|---|
| E-commerce Cases | 收 | `evolink-ecommerce.json` | `marketing`, `retail`, `hospitality`, `general` | 電商主圖、包裝、商品頁可泛用 |
| Ad Creative Cases | 收 | `evolink-ad-creative.json` | `marketing`, `design`, `general` | 廣告素材可補足現有 poster 類 |
| Comparison Cases | 收 | `evolink-comparison.json` | `marketing`, `education`, `product` | 比較圖適合簡報與教材 |
| Poster & Illustration | 收 | `evolink-poster.json` | `marketing`, `events`, `design` | 與 wuyoscar poster 類互補 |
| UI Mockup | 收 | `evolink-ui.json` | `product`, `design` | 補強 product / design 流程 |
| Portrait & Photography | 不收 | - | - | 人物肖像權與臉部權利風險 |
| Character Sheet | 不收 | - | - | 同上，且偏角色設計 |
| Korean Idol | 不收 | - | - | 名人/偶像權利風險 |
| Cosplay | 不收 | - | - | 肖像與 IP 風險 |
| AI Self-Perception | 不收 | - | - | 不符合商務 prompt library |

篩選規則落成常數：

```python
EVOLINK_CATEGORY_MAP = {
    "E-commerce Cases": {
        "slug": "evolink-ecommerce",
        "category": "E-commerce Cases",
        "title_zh": "電商與商品素材",
        "industries": ["marketing", "retail", "hospitality", "general"],
        "file": "evolink-ecommerce.json",
        "keep": True,
    },
    "Portrait & Photography": {"keep": False, "reason": "人物肖像權風險"},
}
```

### 3.3 build_gallery_evolink.py 規格

新增 parser：`tools/build_gallery_evolink.py`。輸入為 `/tmp/upstream-galleries/evolink-prompts.json`，輸出 5 個 category JSON，並更新 `gallery-index.json`。

CLI：

```bash
python3 tools/build_gallery_evolink.py \
  --input /tmp/upstream-galleries/evolink-prompts.json \
  --out web/prompt-library \
  --max-per-category 10
```

程式結構：

```text
tools/build_gallery_evolink.py
├── constants
│   ├── UPSTREAM_REPO
│   ├── UPSTREAM_LICENSE
│   └── EVOLINK_CATEGORY_MAP
├── parse_author(raw)
├── normalize_size(raw)
├── normalize_prompt(raw)
├── build_entry(raw, category_meta, no)
├── build_category_json(slug, entries)
├── merge_gallery_index(existing_index, new_categories)
└── main()
```

資料處理規則：

| 欄位 | 規則 |
|---|---|
| `id` | `evolink-{category_short}-{no:03d}` |
| `no` | 上游 case 編號；沒有就用 category 內序號 |
| `title` | 上游 title；沒有就用 prompt 前 48 字壓縮 |
| `size` | 上游尺寸若無，依類別 fallback |
| `pixel` | 若無明確 pixel，留空字串，不編造 |
| `credit` | `by @handle` 轉 `Author: @handle` |
| `prompt` | 原 prompt 去掉 attribution 行，但保留主要 prompt |
| `industries` | prompt entry 層補一份，方便 UI filter |
| `source.author` | 必填；無法解析則 `Unknown` 並列入 warn |

作者解析：

```python
AUTHOR_RE = re.compile(r"\bby\s+(@[A-Za-z0-9_]+)", re.IGNORECASE)

def parse_author(text: str) -> str:
    match = AUTHOR_RE.search(text or "")
    return match.group(1) if match else "Unknown"
```

### 3.4 schema 對齊（與既有 build_gallery.py）

既有 `tools/build_gallery.py` 的 category JSON：

```json
{
  "schema_version": 1,
  "slug": "ui-ux-mockups",
  "category": "UI/UX Mockups",
  "title_zh": "UI/UX 介面設計",
  "industries": ["product", "design", "marketing", "legal", "education", "general"],
  "use_cases": ["產品 mockup", "提案展示"],
  "source": {
    "repo": "wuyoscar/gpt_image_2_skill",
    "license": "CC BY 4.0",
    "url": "..."
  },
  "count": 5,
  "prompts": [
    {
      "id": "ui-ux-mockups-102",
      "no": 102,
      "title": "Mobile Budgeting App Mockup",
      "size": "portrait",
      "pixel": "1024x1536",
      "credit": "Curated",
      "prompt": "..."
    }
  ]
}
```

EvoLinkAI category JSON 必須向後相容，但允許 entry 多 `industries/source`：

```json
{
  "schema_version": 1,
  "slug": "evolink-ui",
  "category": "UI Mockup",
  "title_zh": "EvoLinkAI UI Mockup",
  "industries": ["product", "design"],
  "use_cases": ["產品概念稿", "App 介面", "SaaS mockup"],
  "source": {
    "repo": "EvoLinkAI/awesome-gpt-image-2-prompts",
    "license": "CC BY 4.0",
    "url": "https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts"
  },
  "count": 8,
  "prompts": [
    {
      "id": "evolink-ui-001",
      "no": 1,
      "title": "Dashboard UI Mockup",
      "size": "landscape",
      "pixel": "",
      "credit": "Author: @example",
      "prompt": "Create ...",
      "industries": ["product", "design"],
      "source": {
        "repo": "EvoLinkAI/awesome-gpt-image-2-prompts",
        "license": "CC BY 4.0",
        "author": "@example",
        "url": "https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts"
      }
    }
  ]
}
```

`gallery-index.json` 由單一 source 改為多 source。建議保留舊 `source` 欄位，新增 `sources`，避免舊 loader 斷掉：

```json
{
  "schema_version": 1,
  "source": {
    "repo": "wuyoscar/gpt_image_2_skill",
    "license": "CC BY 4.0",
    "base_url": "..."
  },
  "sources": [
    {
      "repo": "wuyoscar/gpt_image_2_skill",
      "license": "CC BY 4.0",
      "count": 66
    },
    {
      "repo": "EvoLinkAI/awesome-gpt-image-2-prompts",
      "license": "CC BY 4.0",
      "count": 30
    }
  ],
  "categories": [],
  "total_count": 104
}
```

### 3.5 重新 inline 流程

產出 JSON 後重跑既有 pipeline：

```bash
python3 tools/inline_gallery.py
```

預期輸出：

```text
注入完成：1 個 tag
HTML size：約 217KB → 約 280KB
Gallery：17 類別、100-115 條 prompt
```

驗證 HTML 內資料：

```bash
node - <<'NODE'
const fs = require('fs');
const html = fs.readFileSync('web/forma-studio.html', 'utf8');
const m = html.match(/<script id="forma-gallery" type="application\/json">([\s\S]*?)<\/script>/);
const data = JSON.parse(m[1]);
const repos = new Set();
for (const c of data.categories) {
  if (c.source?.repo) repos.add(c.source.repo);
  for (const p of c.prompts || []) {
    if (p.source?.repo) repos.add(p.source.repo);
  }
}
console.log({ total_count: data.total_count, categories: data.categories.length, repos: [...repos] });
NODE
```

### 3.6 驗收標準

| Gate | 通過標準 |
|---|---|
| parser | `python3 tools/build_gallery_evolink.py ...` exit 0 |
| 檔案 | 5 個 `evolink-*.json` 產出 |
| count | `gallery-index.json.total_count` 從 66 增至 100-115 |
| attribution | EvoLinkAI 每筆 entry 有 `source.author` |
| license | category 與 entry 都保留 `CC BY 4.0` |
| inline | `python3 tools/inline_gallery.py` exit 0 |
| HTML size | 約 217KB → 約 280KB，偏差可接受但不得縮小 |
| UI filter | wuyoscar + EvoLinkAI entries 都可依 industries 顯示 |
| console | 0 console error |

額外檢查指令：

```bash
python3 - <<'PY'
import json
from pathlib import Path

idx = json.loads(Path("web/prompt-library/gallery-index.json").read_text())
assert 100 <= idx["total_count"] <= 115, idx["total_count"]
for cat in idx["categories"]:
    data = json.loads(Path("web/prompt-library", cat["file"]).read_text())
    for p in data["prompts"]:
        if cat["slug"].startswith("evolink-"):
            assert p.get("source", {}).get("author"), p["id"]
print("gallery index ok", idx["total_count"])
PY
```

---

## 四、Tier 1.6：Claude 一鍵增強鈕

### 4.1 EnhanceBtn 元件規格

新增頂層元件 `EnhanceBtn`，放在 `OutBox` 附近，不能在 `OutBox` 內宣告 hook component。`OutBox` 接受可選 prop：`onTextChange` 或 `enhanceable`。

| 項目 | 規格 |
|---|---|
| 元件 | `EnhanceBtn` |
| 位置 | prompt 輸出框「複製」按鈕旁 |
| key | `useContext(ApiCtx)` |
| flag | `ENABLE_AI_ENHANCE` |
| model | `gpt-4o-mini` |
| loading | 按鈕 disabled，文字 `增強中...` |
| 失敗 | 保留原 prompt，toast 錯誤 |
| 無 key | disabled + tooltip |

元件骨架：

```jsx
function EnhanceBtn({ text, onEnhanced }) {
  const { key } = useContext(ApiCtx);
  const [loading, setLoading] = useState(false);
  const disabled = !ENABLE_AI_ENHANCE || !key.trim() || !text?.trim() || loading;

  const run = async () => {
    if (disabled) return;
    setLoading(true);
    try {
      const next = await enhancePromptWithOpenAI(text, key);
      onEnhanced(next || text);
    } catch (e) {
      showToast('AI 增強失敗，已保留原 prompt');
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={run}
      disabled={disabled}
      title={!key.trim() ? '需要先輸入 OpenAI API key' : '用 craft.md §19 增強 prompt'}
      className={disabled ? '...' : '...'}
    >
      {loading ? '增強中...' : '✨ AI 增強'}
    </button>
  );
}
```

OpenAI call：

```javascript
async function enhancePromptWithOpenAI(promptText, apiKey) {
  const resp = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: 'gpt-4o-mini',
      temperature: 0.2,
      messages: [
        { role: 'system', content: ENHANCE_SYSTEM_PROMPT },
        { role: 'user', content: promptText },
      ],
    }),
  });
  if (!resp.ok) throw new Error(`enhance failed: ${resp.status}`);
  const data = await resp.json();
  return data.choices?.[0]?.message?.content?.trim();
}
```

### 4.2 system prompt 設計（接 craft.md §19）

system prompt 要用 `skills/forma-studio/references/craft.md` §19 的 final audit 精神，但不能在 runtime fetch markdown。先把必要 audit 摘要寫進常數。

```javascript
const ENHANCE_SYSTEM_PROMPT = `你是 Forma Studio 的 prompt 增強器。
依 craft.md §19 final audit 把使用者 prompt 改寫得更完整。
輸出僅包含改寫後 prompt，不含說明。

必須補強：
1. 任務意圖：image / edit / infographic / prototype / brand。
2. 受眾、渠道、決策情境。
3. 核心訊息一句話。
4. 構圖、版面、typography、color system、material / lighting。
5. in-image text 必須用引號逐字列出。
6. size、quality、negative constraints。
7. 反 AI Slop：禁紫漸變、generic card wall、emoji 圖標、假 logo、不可讀文字。
8. 若原 prompt 含 source attribution，必須保留。

不要新增未提供的具體品牌、人物、日期、法規或產品版本。若缺資訊，用 [PLACEHOLDER: ...] 標記。`;
```

輸出約束：

| 條件 | 行為 |
|---|---|
| 原 prompt 已有 attribution | 保留 source line |
| 涉及具體品牌但未驗證 | 加 `[VERIFY: ...]` |
| 缺素材 | 用 `[PLACEHOLDER: ...]` |
| 原 prompt 是中文 | 輸出繁體中文 |
| 原 prompt 是英文 | 可保留英文，但 audit label 可用英文 |

### 4.3 feature flag 與 fallback

新增 flag：

```javascript
const ENABLE_AI_ENHANCE = true;
```

fallback table：

| 狀況 | UI 行為 | 資料行為 |
|---|---|---|
| `ENABLE_AI_ENHANCE=false` | 不顯示或 disabled | 不呼叫 API |
| 無 API key | disabled + tooltip | 原 prompt 不變 |
| API 401/429/500 | toast | 原 prompt 不變 |
| response 空 | toast | 原 prompt 不變 |
| user 複製中 | copy 不受影響 | `CopyBtn` 使用目前文字 |

`OutBox` 改造建議：

```jsx
function OutBox({ text, label, hint, badge='yellow', onTextChange }) {
  if (!text) return null;
  return (
    <div className="fade-in mb-4">
      <div className="flex items-center justify-between mb-1.5">
        <span className={`text-sm font-bold ${badge==='teal'?'text-teal-400':'text-yellow-400'}`}>{label}</span>
        <div className="flex gap-1.5">
          {onTextChange && <EnhanceBtn text={text} onEnhanced={onTextChange} />}
          <CopyBtn text={text} />
        </div>
      </div>
      {/* ... */}
    </div>
  );
}
```

驗收：

```bash
node - <<'NODE'
/* 只檢查常數存在，實際 API 由 Playwright manual key 測 */
const fs = require('fs');
const html = fs.readFileSync('web/forma-studio.html', 'utf8');
for (const token of ['ENABLE_AI_ENHANCE', 'function EnhanceBtn', 'ENHANCE_SYSTEM_PROMPT']) {
  if (!html.includes(token)) throw new Error(`${token} missing`);
}
console.log('enhance hooks present');
NODE
```

---

## 五、實作順序與里程碑

### 5.1 第一個 commit：B 完成

建議 commit：

```bash
git add web/forma-studio.html
git commit -m "feat: 接通 prompt gallery 與四區塊 UI"
```

工作順序：

| Step | 動作 | 檔案 | Gate |
|---:|---|---|---|
| 1 | 加 `useGallery()` 與 mapping 常數 | `web/forma-studio.html` | JSX parse |
| 2 | Section 2 加 industries chips | `web/forma-studio.html` | state 多選可用 |
| 3 | Section 3 加 `📚 範例庫` | `web/forma-studio.html` | prompt list 可顯示 |
| 4 | 點 prompt 注入 `desc` | `web/forma-studio.html` | textarea 更新 |
| 5 | Playwright 11 步 | `.playwright/*.png` | 0 console error |

不納入 commit 的暫存：

```text
.playwright/sprint1-verify.spec.js
.playwright/sprint1-verify-*.png
```

如果團隊需要保留截圖證據，可另開 `test-artifacts/`；Sprint 1.5 預設不增加 repo 體積。

### 5.2 第二個 commit：A 完成

建議 commit：

```bash
git add tools/build_gallery_evolink.py web/prompt-library gallery-index.json web/forma-studio.html
git commit -m "feat: 整合 EvoLinkAI prompt gallery"
```

工作順序：

```text
抓 upstream JSON
  ↓
實作 build_gallery_evolink.py
  ↓
產出 5 個 evolink JSON
  ↓
merge gallery-index.json
  ↓
python3 tools/inline_gallery.py
  ↓
Playwright 驗證 FORMA_GALLERY.total_count
```

指令：

```bash
mkdir -p /tmp/upstream-galleries
curl -sL https://raw.githubusercontent.com/EvoLinkAI/awesome-gpt-image-2-prompts/main/gpt_image_2_prompt.json \
  -o /tmp/upstream-galleries/evolink-prompts.json
python3 tools/build_gallery_evolink.py \
  --input /tmp/upstream-galleries/evolink-prompts.json \
  --out web/prompt-library
python3 tools/inline_gallery.py
```

### 5.3 第三個 commit：Tier 1.6 完成

建議 commit：

```bash
git add web/forma-studio.html
git commit -m "feat: 新增 prompt AI 增強按鈕"
```

工作順序：

| Step | 動作 | Gate |
|---:|---|---|
| 1 | 加 `ENABLE_AI_ENHANCE` | flag 可關閉 |
| 2 | 加 `ENHANCE_SYSTEM_PROMPT` | 不含 runtime markdown fetch |
| 3 | 加 `enhancePromptWithOpenAI()` | 401/429/500 throw |
| 4 | 加 `EnhanceBtn` | 無 key disabled |
| 5 | `OutBox` 支援 `onTextChange` | copy 不破 |
| 6 | 在主要 output state 接 `setOut` | 增強後替換內容 |

手動測試：

```text
1. 不輸入 API key → 按鈕 disabled。
2. 輸入 API key → 生成 prompt → 點 AI 增強。
3. response 回來後 OutBox 文字被替換。
4. 點複製 → clipboard 是增強後 prompt。
```

### 5.4 整體 Sprint 1.5 收尾 commit + tag v2.5-sprint-1.5

收尾應更新 `DEVLOG.md` 與 `HANDOFF.md`，但這不屬於本計劃書執行範圍。實作完成時建議：

```bash
git add DEVLOG.md HANDOFF.md
git commit -m "docs: 更新 Sprint 1.5 交接紀錄"
git tag v2.5-sprint-1.5
```

收尾檢查表：

| 檢查 | 標準 |
|---|---|
| `FORMA_GALLERY.total_count` | 100-115 |
| `ENABLE_PROMPT_GALLERY=false` | 4 區塊 fallback 可用 |
| `ENABLE_AI_ENHANCE=false` | 不影響複製與生成 |
| Playwright | 0 console error |
| attribution | wuyoscar + EvoLinkAI 保留 license |

---

## 六、風險與回滾

### 6.1 風險清單（每個任務至少 2 個）

#### B：gallery 接 UI

| 風險 | 影響 | 預防 | 回滾 |
|---|---|---|---|
| hook 放進 component 內造成 nested-with-hooks 風險 | JSX 可過但維護性壞 | `useGallery()` 頂層宣告 | 移回頂層 |
| Section 3 子頁籤 state 與現有 `sub` 衝突 | 4 區塊流程卡住 | `showGallery` 獨立於 `sub` | 關閉 gallery secondary mode |
| `ProtoPane/InfoPane/BrandPane` state 不可注入 | prompt 注入只對 image 生效 | B1 先統一注入 `desc` | 不改子元件 |
| category-level industries 與 entry-level industries 混用 | filter count 不準 | normalize 時補 `p.industries` | 只讀 category industries |
| `ENABLE_PROMPT_GALLERY=false` 未測 | fallback 失效 | Playwright 加 flag 測試 | flag 關閉整段 UI |

#### A：EvoLinkAI 整合

| 風險 | 影響 | 預防 | 回滾 |
|---|---|---|---|
| 上游 JSON schema 改變 | parser 失敗 | parser 做 key fallback + warn | 不產 EvoLinkAI JSON |
| 作者 attribution 解析不到 | license 不合格 | `source.author` 必填，不足列 warn | 該 entry 不收 |
| 人物肖像類漏進來 | 權利風險 | category denylist + prompt keyword denylist | 刪除對應 JSON entry |
| total_count 超過 115 | HTML 變大、UI 過長 | `--max-per-category` | 下調 per category 上限 |
| index 多 source 破壞 inline | loader 無法讀 | 保留舊 `source`，新增 `sources` | 回退 index schema |

#### Tier 1.6：AI 增強鈕

| 風險 | 影響 | 預防 | 回滾 |
|---|---|---|---|
| OpenAI API CORS / endpoint 失敗 | 按鈕不可用 | failure 保留原 prompt | `ENABLE_AI_ENHANCE=false` |
| 無 key 時仍可點 | 401 噪音 | disabled + tooltip | 加硬阻擋 |
| 增強結果覆蓋 attribution | CC BY 標註遺失 | system prompt 要求保留 | 若缺 source，回退原 prompt |
| prompt 被模型加入未驗證品牌 | 事實風險 | 要求 `[VERIFY]` placeholder | 手動移除增強結果 |
| `OutBox` 改造破壞 copy | 核心 UX 退化 | copy 與 enhance 分離 | 還原 OutBox，只保留 CopyBtn |

### 6.2 回滾策略

回滾單位用 feature flag 優先，不先刪 code：

```javascript
const ENABLE_PROMPT_GALLERY = false;
const ENABLE_AI_ENHANCE = false;
```

回滾矩陣：

| 問題 | 第一層回滾 | 第二層回滾 | 需保留 |
|---|---|---|---|
| gallery UI bug | `ENABLE_PROMPT_GALLERY=false` | revert B commit | inline JSON |
| EvoLinkAI parser bug | 不重跑 inline | revert A commit | wuyoscar 66 條 |
| EvoLinkAI license 缺 author | 移除該 entries | revert A commit | parser warn log |
| AI enhance bug | `ENABLE_AI_ENHANCE=false` | revert Tier 1.6 commit | `CopyBtn` |
| HTML parse broken | revert 最新 commit | 回到上一個 passing tag | `tools/inline_gallery.py` |

回滾驗證：

```bash
node - <<'NODE'
const fs = require('fs');
const html = fs.readFileSync('web/forma-studio.html', 'utf8');
if (!html.includes('const ENABLE_PROMPT_GALLERY')) process.exit(1);
console.log('flag exists');
NODE
```

---

## 七、後續 Backlog（不在 Sprint 1.5 範圍）

### 7.1 Tier 2 Sprint 2：PyQt6 桌面版（含子任務細項）

Tier 2 依 SDD 4.1 / 4.2 / 4.3 順序做，不插隊進 Sprint 1.5。

| 順序 | 子任務 | 檔案 | 驗收 |
|---:|---|---|---|
| 1 | OpenAI client 支援 edits endpoint | `desktop/app/api/openai_client.py` | `client.images.edit()` 可送 multipart |
| 2 | 多參考圖 drop zone | `desktop/app/widgets/reference_drop_zone.py` | 最多 4 張，超過阻擋 |
| 3 | mask uploader | `desktop/app/widgets/mask_uploader.py` | PNG alpha mask 檢查 |
| 4 | edit panel 整合 | `desktop/app/widgets/image_edit_panel.py` | generations / edits 按鈕分離 |
| 5 | quality 撥盤 | `desktop/app/widgets/quality_dial.py` | low/medium/high 成本顯示 |
| 6 | DESIGN.md parser | `desktop/app/utils/design_memory.py` | parse/validate/save |
| 7 | 品牌設定頁 | `desktop/app/pages/brand_settings_tab.py` | GUI 編輯 DESIGN.md |
| 8 | keyring | `desktop/app/api/key_store.py` | 不 hardcode API key |

目錄草圖：

```text
desktop/app/
├── api/
│   ├── openai_client.py
│   └── key_store.py
├── widgets/
│   ├── quality_dial.py
│   ├── reference_drop_zone.py
│   ├── mask_uploader.py
│   └── image_edit_panel.py
├── utils/
│   └── design_memory.py
└── pages/
    └── brand_settings_tab.py
```

最小 API 規格：

```python
async def edit_image(
    prompt: str,
    images: list[Path],
    mask: Path | None,
    size: str,
    quality: str,
) -> bytes:
    ...
```

### 7.2 v3.0 評估：nexu-io design-systems markdown 格式借鑑

不在 Sprint 1.5 實作，只做 v3.0 research item。

| 評估項 | 需要回答 |
|---|---|
| markdown schema | 是否比 `DESIGN.md` 更適合描述 design tokens |
| tokens | color/type/spacing/component 是否可機讀 |
| 版本管理 | 是否能 diff 與 merge |
| 匯入路徑 | 是否能轉成 Forma Studio prompt context |

候選輸出：

```text
docs/research/design-systems-markdown-eval.md
```

暫定 schema 借鑑方向：

```markdown
# Design System

## Tokens
- color.primary: oklch(...)
- type.heading: ...
- spacing.4: 16px

## Components
- Button
- Card
- DataTable
```

### 7.3 v3.0 評估：Comment mode

Comment mode 需要 preview target、annotation model、prompt patch 三段能力，不能塞進 Sprint 1.5。

| 子系統 | 需求 |
|---|---|
| hit-test | 點擊畫面元素，取得 DOM/canvas 區域 |
| comment store | pin、comment、resolved state |
| prompt patch | 只重寫指定區域 prompt |
| preview sync | 修改後能對照 before/after |

資料模型草案：

```json
{
  "id": "comment-001",
  "target": {
    "type": "region",
    "x": 0.32,
    "y": 0.18,
    "w": 0.24,
    "h": 0.12
  },
  "body": "標題太弱，增加 hierarchy。",
  "status": "open"
}
```

### 7.4 v3.0 評估：多格式匯出（HTML/PDF/PPTX/ZIP/Markdown）

多格式匯出需要 render pipeline，不只是一個下載按鈕。

| 格式 | 技術需求 | 風險 |
|---|---|---|
| HTML | 單檔 template + assets inline | CSS 隔離 |
| PDF | headless browser render | 字型與分頁 |
| PPTX | slide layout engine | 版面還原度 |
| ZIP | assets packaging | 檔名與相對路徑 |
| Markdown | prompt + metadata export | 圖像資產引用 |

候選 pipeline：

```text
Prompt Output
  ↓
Export Model JSON
  ↓
Renderer Adapters
  ├── HTML adapter
  ├── PDF adapter
  ├── PPTX adapter
  ├── Markdown adapter
  └── ZIP packager
```

v3.0 前置條件：

```bash
# 只作未來評估，不在 Sprint 1.5 安裝
npm view pptxgenjs version
npm view playwright version
```

---

## Sprint 1.5 Definition of Done

| 項目 | 通過標準 |
|---|---|
| B | 4 區塊 UI 可用，gallery 可 filter、可注入、可複製 |
| A | 兩個 CC BY 4.0 source 並存，total_count 100-115 |
| Tier 1.6 | AI 增強鈕有 key 才可用，失敗不破壞原 prompt |
| 測試 | JSX parse + Playwright 11 步 + 0 console error |
| 回滾 | `ENABLE_PROMPT_GALLERY` 與 `ENABLE_AI_ENHANCE` 可獨立關閉 |

