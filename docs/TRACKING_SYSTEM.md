# Alan AI Website — Tracking & Standardization System

**Goal:** All articles go through one pipeline. Every article is tracked (views, AdSense revenue, IG engagement). Data is used to optimize AdSense revenue.

**Created:** 2026-07-12 by 小花 🌸 (per Alan's "standardize + track" mandate)

---

## 📐 Architecture

```
                    ┌─────────────────────────────────┐
                    │   Standardized Pipeline          │
                    │   (tools/new_article.py)         │
                    └────────────┬────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
  Article HTML             Cover Image              IG Feed Post
  (Style A template)       (tools/make_cover.py)    (publish_article_to_ig.py)
        │                        │                        │
        └────────────┬───────────┴────────────┬───────────┘
                     │                        │
                     ▼                        ▼
              GitHub Pages              tracking/articles_tracking.csv
              (alanhorizonteam.org)     (每篇 log: slug/topic/date/views/revenue/IG)
                     │                        │
                     │                        ▼
                     │              ┌────────────────────────┐
                     │              │   Dashboard Section    │
                     │              │   (index.html          │
                     │              │    「📊 數據儀表板」)   │
                     │              └────────────────────────┘
                     │
                     ▼
              CF Counter Worker (per-article view count)
              counter.alanhorizonteam.org
```

---

## 🎯 Standardized Pipeline — Every New Article Goes Through This

### Step 1: Input (from Alan)
- Topic (finance / HK / world / tech / entertainment / philosophy / conspiracy / lifestyle)
- Title (繁體中文, 海底人風格, dramatic)
- Content (~1000-3000字, 繁體香港廣東話)
- Cover image concept (or AI-generated from title)

### Step 2: Build HTML (`articles/<slug>.html`)
- Style A template (verified from `海底人為什麼不能存在.html`):
  - bg gradient `#1a1a2e → #16213e → #0f3460`
  - `.section-title` purple border `#667eea`
  - `.intro` purple border
  - `.quote` gold blockquote
  - `.hashtag-pill` pills
  - Hero full viewport (min-height: 80vh)
- Required meta tags:
  - `<meta property="og:image" content="FREEIMAGE_URL">` ← **ASCII URL only!**
  - `<meta name="twitter:image" content="FREEIMAGE_URL">`
  - `<meta property="og:url" content="ARTICLE_URL">`
  - `<meta property="og:title" content="TITLE">`
  - `<meta property="og:description" content="...">`
- GA4 already embedded in index.html (no per-article work needed)

### Step 3: Build Cover Image (`articles/<slug>_cover.jpg`)
- Tool: `tools/make_cover.py`
- Spec (verified from 海底人 cover v4):
  - 1024×1024, 1:1 JPG quality 92
  - 深 navy + 金色 (#0a0a1a / #0f3460 / #ffd700)
  - PIL watermark: 28pt bold, -30° tilt, 3 columns, opacity 155 (~60%)
  - **NO left-bottom gold brand mark** (per Alan 2026-07-12 feedback)
- Upload to freeimage.host → ASCII URL for og:image
- Local copy committed to repo for backup

### Step 4: Update index.html
- Insert new article card 喺 articles section 頂部 (最新嘅擺最前)
- Include view counter SVG: `<img src="https://counter.alanhorizonteam.org/counter.svg?path=%2Farticles%2F<urlencoded_slug>.html&mode=peek">`
- Update `<p class="section-desc">原創研究 · 深度思考 · 創意遊戲 — 共 N 篇</p>`

### Step 5: Update sitemap.xml
- Add `<url><loc>ARTICLE_URL</loc>...</url>` entry
- ⚠️ Chinese URL 必須 percent-encode inside `<loc>` element

### Step 6: Commit + Push (deploy)
```powershell
cd repo
git add -A
git commit -m "[article] <title> + cover"
git push origin main
```

### Step 7: Append tracking CSV
- `tracking/articles_tracking.csv` 加一行 entry
- Fields: slug, title_zh, topic, publish_date, cover_filename, cover_freeimage_url, article_url, ig_post_id, ig_published_at, view_count, adsense_revenue_usd, rpm_usd, keywords, notes

### Step 8: Publish IG Feed Post (1:1, NO Story — Alan AI rule)
- Per confirm-first rule: re-show image + caption draft, wait for Alan OK
- Tool: `tools/publish_article_to_ig.py` (imports BUFFER_API_KEY from `projects/instagram-news/publish.py`)
- Caption format (per Alan 2026-07-12): 簡短 廣東話
  ```
  {emoji} Alan AI 文章：{title}

  {1-2 句 teaser}

  閱讀全文：{article_url}

  #HorizonTeam #AlanAI #{topic} #{keyword1} #{keyword2}
  ```

---

## 📊 Dashboard Section (Homepage)

位置: `index.html` 加 `<section class="section" id="dashboard">`

**4 metric cards (順序由 Alan most-important first):**
1. 📊 **AdSense 累計收益** (USD) — `[TBD: OAuth AdSense API]`
2. 👥 **IG 追蹤者** — `[TBD: Buffer profile API / IG Graph]`
3. 🌐 **總瀏覽者** (30 日) — `[TBD: GA4 Reporting API]`
4. 📖 **總文章 view** (累計) — `[TBD: CF Counter Worker aggregate]`

**Top earners table:**
- Top 10 articles by RPM
- Slug / topic / views / revenue / RPM

---

## 📁 File Structure

```
projects/alan-ai-website/
├── README.md
├── docs/
│   ├── design.md
│   ├── decisions.md
│   └── TRACKING_SYSTEM.md      ← this file
├── scripts/
│   └── deploy.ps1              ← (TBD) commit + push helper
├── tools/
│   ├── make_cover.py           ← cover image gen + watermark
│   ├── upload_to_freeimage.py  ← freeimage anonymous upload
│   └── publish_article_to_ig.py ← Buffer Feed Post publish
├── tracking/
│   ├── articles_tracking.csv   ← every article logged
│   └── metrics/                ← (TBD) cached API responses
├── repo/
│   ├── index.html
│   ├── articles/
│   │   ├── 海底人為什麼不能存在.html
│   │   ├── 海底人為什麼不能存在_cover.jpg
│   │   └── ... (13 articles total)
│   └── sitemap.xml
└── config/
    └── (TBD) pipeline config — topic keywords, IG caption template, etc
```

---

## 🔌 API Connections Required (TODO)

| Source | Purpose | Auth Method | Status |
|---|---|---|---|
| CF Counter Worker | Per-article view count | Public endpoint | ✅ Live |
| GA4 (G-32X6WDJM63) | Site visitors, page views, source | Service Account JSON | ⏳ Need creds |
| AdSense (ca-pub-8953374000835577) | Revenue, CTR, RPM | OAuth client | ⏳ Need creds |
| Buffer | IG followers, post engagement | BUFFER_API_KEY | ✅ Live (in publish.py) |
| freeimage.host | Image CDN upload | FREEIMAGE_API_KEY | ✅ Live (in publish.py) |

**Credentials storage:** `projects/alan-ai-website/.env` (chmod 600), python-dotenv load. **NEVER paste in Telegram chat** (per MEMORY.md security rule).

---

## 📈 AdSense Revenue Optimization Playbook

**Formula:** Revenue = Impressions × CTR × CPC

### Phase 1 — Measure (this week)
1. Backfill articles_tracking.csv with all 13 articles ✓ (done)
2. Pull AdSense API daily → record per-article revenue
3. Pull GA4 daily → record views
4. Compute RPM (revenue per 1000 views) per article

### Phase 2 — Analyze (next week)
1. Rank articles by RPM (highest first)
2. Identify high-RPM topics (finance > conspiracy? lifestyle > philosophy?)
3. Identify high-CTR titles (subject line A/B test candidates)
4. Identify seasonal trends (monthly RPM curve)

### Phase 3 — Optimize (ongoing)
1. **More of what works:** write more high-RPM topic articles
2. **Better titles:** A/B test, learn from winners
3. **Better covers:** high CTR cover = more clicks = more impressions
4. **Better timing:** publish when RPM peaks (weekday vs weekend, hour)
5. **SEO boost:** target high-CPC keywords (insurance, mortgage, lawyer)
6. **Internal linking:** cross-link related articles, increase dwell time → more ad impressions
7. **Ad placement:** test more ads above fold, in-article after P2

### Phase 4 — Scale (later)
1. Auto-generate article topic ideas from trending keywords (Google Trends API)
2. Auto-schedule publishing for peak RPM hours
3. Auto-A/B test titles via Buffer (publish 2 IG variants, pick winner)

---

## ⚙️ Quick Commands (Alan BB Cheat Sheet)

```
# 寫新文章 (full pipeline)
python tools/new_article.py "海底人為什麼不能存在" --topic philosophy --keywords "海底人,UFO,達爾文"

# Update dashboard data (after credentials)
python tools/refresh_dashboard.py

# View tracking CSV
type tracking\articles_tracking.csv

# Pull current view counts (no creds needed — CF Worker public)
curl https://counter.alanhorizonteam.org/counter.svg?path=%2Farticles%2F海底人為什麼不能存在.html&mode=peek
```

---

## 🎓 Lessons Learned (2026-07-12)

1. **OG image 永遠用 ASCII URL** — 中文 filename og:image 喺 FB/Telegram preview scrape 唔到。Always upload to freeimage first, use the iili.io URL.
2. **Watermark spec 跟 IG-news** — 28pt, -30°, opacity 155 (per Alan 2026-07-12 final tuning).
3. **Import existing config > duplicate** — `publish_article_to_ig.py` 從 `projects/instagram-news/publish.py` import BUFFER_API_KEY.
4. **Per-article view counter** — CF Worker mode=peek (read), mode=view (increment). Index 用 peek, article HTML 入面用 view.
5. **Style A template** — verified from 海底人: gradient bg + purple borders + gold blockquote + hashtag pills. **Freeze this as canonical.**