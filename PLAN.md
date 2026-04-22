# NeuroFamilies.org — Build Plan
## Autism & Neurodiverse Family Resource Directory

**Mission:** Centralize the scattered world of autism/neurodiverse resources so families spend minutes finding help, not weeks.

**Domain:** neurofamilies.org  
**Budget:** $0 (domain ~$7.50/yr is only cost)  
**Tech Stack:** Python scrapers → JSON data → Static site (GitHub Pages) → Gumroad products  

---

## Phase 1: MVP (Week 1-2)
**Goal:** Live site with searchable directory for 5 states

### 1.1 Data Schema
```json
{
  "id": "uuid",
  "name": "Bright Horizons ABA Center",
  "category": "aba-therapy",
  "subcategory": "center-based",
  "description": "Center-based ABA therapy for ages 2-18",
  "address": "123 Main St",
  "city": "Austin",
  "state": "TX",
  "zip": "78701",
  "phone": "512-555-0100",
  "website": "https://...",
  "email": "contact@...",
  "insurance_accepted": ["Medicaid", "Blue Cross", "Aetna"],
  "ages_served": "2-18",
  "specialties": ["autism", "developmental delays"],
  "source": "autismspeaks.org",
  "last_verified": "2026-04-21",
  "rating": null
}
```

### 1.2 Categories
| Category ID | Label | Icon |
|-------------|-------|------|
| aba-therapy | ABA Therapy | 🧩 |
| speech-therapy | Speech Therapy | 🗣️ |
| occupational-therapy | Occupational Therapy | 🖐️ |
| physical-therapy | Physical Therapy | 🏃 |
| respite-care | Respite Care | 🏠 |
| support-groups | Support Groups | 👥 |
| schools | Schools & Programs | 🏫 |
| government | Government Programs | 🏛️ |
| funding | Grants & Funding | 💰 |
| sensory-products | Sensory Products & Tools | 🎯 |
| camps | Camps & Recreation | ⛺ |
| legal | Legal & Advocacy | ⚖️ |
| mental-health | Mental Health | 💚 |
| adult-services | Adult Services | 🧑 |

### 1.3 Data Sources (Scraping Targets)
| Source | What We Get | Method |
|--------|------------|--------|
| Autism Speaks Resource Guide | ABA, therapy, support groups | Web scrape |
| SAMHSA Treatment Locator | Mental health, substance abuse | API available |
| Psychology Today Therapist Finder | Therapists with autism specialty | Web scrape |
| State Medicaid/IDEA Sites | Government programs, waivers | Web scrape per state |
| 211.org | Local social services | Web scrape |
| Easter Seals / ARC chapters | Respite, programs | Web scrape |
| ABLE Accounts (state-specific) | Financial programs | Manual compile |

### 1.4 Site Architecture
```
neurofamilies/
├── data/
│   ├── national/          # Federal resources
│   ├── states/
│   │   ├── tx.json        # Texas resources
│   │   ├── ca.json
│   │   └── ...
│   └── index.json         # Master lookup
├── scrapers/
│   ├── autism_speaks.py
│   ├── psychology_today.py
│   ├── samhsa.py
│   ├── state_medicaid.py
│   └── run_all.py         # Master scraper runner
├── site/
│   ├── index.html         # Search page
│   ├── state/
│   │   └── [state].html   # State landing pages
│   ├── category/
│   │   └── [cat].html     # Category pages
│   ├── about.html
│   └── assets/
│       ├── css/
│       ├── js/
│       └── img/
├── scripts/
│   ├── build.py           # JSON → static HTML
│   └── validate.py        # Data quality checks
└── .github/
    └── workflows/
        └── deploy.yml     # Auto-build on data update
```

### 1.5 Site Features (MVP)
- [ ] Search by zip code, city, state, or keyword
- [ ] Filter by category
- [ ] State landing pages with resource counts
- [ ] Mobile-responsive
- [ ] Accessible (WCAG basics)
- [ ] "Suggest a Resource" form (Google Form → manual review)
- [ ] Footer: copyright, about, privacy

### 1.6 Monetization (Day 1)
- [ ] Gumroad: "Complete Autism Resource Guide by State" ($15 PDF)
- [ ] Amazon affiliate links for sensory/recommended products
- [ ] Google AdSense (after 1K+ resources, apply)
- [ ] "Sponsored Listing" option for providers ($50/yr, marked clearly)

---

## Phase 2: Growth (Week 3-4)
**Goal:** All 50 states, 5,000+ resources, SEO foundation

### 2.1 Expand Coverage
- [ ] Run scrapers for all 50 states
- [ ] Add user-submitted resources (form → review → add)
- [ ] Partner outreach: ask orgs to verify/update their listings

### 2.2 SEO
- [ ] Individual pages for each resource (unique URLs)
- [ ] State + category landing pages (e.g., /tx/aba-therapy)
- [ ] Schema.org markup for LocalBusiness/MedicalBusiness
- [ ] Blog content: "Finding ABA Therapy in [State]", etc.

### 2.3 Quality
- [ ] Automated link checking (dead links flagged)
- [ ] Monthly re-scrape for data freshness
- [ ] "Last verified" dates on all listings

---

## Phase 3: Premium Features (Month 2-3)
**Goal:** Revenue + differentiation

### 3.1 IEP Analyzer
- Upload IEP document → AI flags issues, suggests accommodations
- Free basic check, $15-25 detailed report
- Built on existing LLM infrastructure

### 3.2 Resource Alerts
- "Notify me when new ABA providers appear in my area"
- Email alerts via free tier (Resend, SendGrid)

### 3.3 Comparison Tool
- Compare 2-3 providers side-by-side (insurance, ages, reviews)

### 3.4 Community
- Parent reviews on resources
- Moderated Q&A

---

## Phase 4: Scale (Month 3+)
**Goal:** Become THE go-to resource

### 4.1 Content Engine
- Blog: resource guides, parent stories, IEP tips
- Social media: share resources, parent tips (existing automation)
- YouTube: walkthroughs of how to find resources

### 4.2 Partnerships
- Autism orgs linking to us as resource provider
- Insurance companies: "Find in-network providers"
- State agencies: embed our search

### 4.3 Products (Gumroad)
- [ ] State Resource Guides (PDF bundles) — $15-25 each
- [ ] IEP Template Pack — $19
- [ ] Meltdown Response Toolkit — $15
- [ ] Visual Schedule Generator (web app) — freemium
- [ ] Annual "NeuroFamilies Guide" — $29

---

## Technical Decisions

### Static Site Generator
**Hugo** — Fast, no JS framework needed, great for data-driven sites.
- Templates pull from JSON data files
- Client-side search via Lunr.js or Pagefind
- GitHub Pages deployment (free)

### Search (Client-Side)
**Pagefind** — Static search that works on GitHub Pages.
- Builds index at deploy time
- Typo-tolerant
- Filter by category/state
- No server needed

### Scraping Schedule
- Full scrape: Monthly (GitHub Actions cron)
- Link validation: Weekly
- Manual additions: Anytime via PR or form

### Hosting
- GitHub Pages (free, custom domain support)
- Cloudflare (free CDN + SSL, if needed)

---

## Revenue Projections (Conservative)

| Stream | Month 1 | Month 3 | Month 6 | Month 12 |
|--------|---------|---------|---------|----------|
| Gumroad PDFs | $0-50 | $100-300 | $300-500 | $500-1000 |
| Affiliate | $0 | $10-50 | $50-150 | $150-400 |
| Sponsored Listings | $0 | $50-100 | $100-300 | $300-800 |
| IEP Analyzer | — | $0-100 | $200-500 | $500-1500 |
| **Total** | **$0-50** | **$160-550** | **$650-1450** | **$1450-3700** |

---

## Immediate Next Steps

1. [ ] Register neurofamilies.org ($7.50/yr)
2. [ ] Create GitHub repo: `UlyasPendragon/neurofamilies`
3. [ ] Build first scraper: Autism Speaks Resource Guide
4. [ ] Define JSON schema, validate with sample data
5. [ ] Set up Hugo site skeleton
6. [ ] Build client-side search (Pagefind)
7. [ ] Deploy to GitHub Pages with custom domain
8. [ ] Scrape first 5 states
9. [ ] Launch MVP
10. [ ] Create first Gumroad product (State Resource Guide PDF)

---

*Plan created: April 21, 2026*  
*Owner: Curtis Reker*  
*Built by: Hermes Agent*
