# NSE Stock Analysis Claude Skills — Design Specification

**Date:** 2026-03-26
**Author:** Sumin Pillai (AlphaQuantix Analytics)
**Repo:** https://github.com/SuminPillai/NSE-STOCK-ANALYSIS-CLAUDE-SKILLS
**Status:** Draft

---

## 1. Overview

A suite of 10 Claude Code skills for analyzing stocks in the Indian stock market. Each skill is invocable via `/skill-name` in Claude Code, providing AI-assisted interactive analysis tailored to India-specific market structures, regulations, and data sources.

### Target Audience

Developers and quantitative analysts with financial literacy — assumes knowledge of derivatives, institutional flows, SEBI regulations, and Indian tax structure.

### Key Decisions

- **Architecture:** Modular skills with shared core (Approach B)
- **Data sources:** Self-contained using public APIs/libraries only (yfinance, NSE/BSE websites, AMFI, SEBI). No dependency on private infrastructure.
- **Output:** Rich terminal analysis by default (markdown tables, heatmaps, sparklines), with export to CSV, JSON, or standalone Python code.

---

## 2. Repository Structure

```
NSE-STOCK-ANALYSIS-CLAUDE-SKILLS/
├── core/
│   ├── __init__.py
│   ├── data_sources.py       # Fetchers for NSE, BSE, AMFI, SEBI, RBI, yfinance
│   ├── formatters.py         # Terminal tables, markdown, heatmaps, sparklines
│   ├── exporters.py          # CSV, JSON, Python code generation
│   ├── constants.py          # Indian market constants (holidays, lot sizes, tax slabs)
│   └── cache.py              # Response caching with configurable TTL
├── skills/
│   ├── nse-screener/
│   │   ├── nse-screener.md
│   │   └── screener.py
│   ├── fii-dii-tracker/
│   │   ├── fii-dii-tracker.md
│   │   └── tracker.py
│   ├── nse-options-chain/
│   │   ├── nse-options-chain.md
│   │   └── options_chain.py
│   ├── sebi-deal-scanner/
│   │   ├── sebi-deal-scanner.md
│   │   └── deal_scanner.py
│   ├── promoter-analyzer/
│   │   ├── promoter-analyzer.md
│   │   └── promoter.py
│   ├── fo-strategy/
│   │   ├── fo-strategy.md
│   │   └── strategy.py
│   ├── mf-flow-analyzer/
│   │   ├── mf-flow-analyzer.md
│   │   └── mf_flows.py
│   ├── sector-rotation/
│   │   ├── sector-rotation.md
│   │   └── rotation.py
│   ├── tax-calculator/
│   │   ├── tax-calculator.md
│   │   └── tax_calc.py
│   └── smallcap-discovery/
│       ├── smallcap-discovery.md
│       └── discovery.py
├── tests/
│   ├── test_core/
│   │   ├── test_data_sources.py
│   │   ├── test_formatters.py
│   │   └── test_exporters.py
│   └── test_skills/
│       ├── test_nse_screener.py
│       ├── test_fii_dii_tracker.py
│       └── ... (one per skill)
├── requirements.txt
├── setup.py
├── README.md
├── LICENSE
└── .gitignore
```

---

## 3. Shared Core

### 3.1 Data Sources (`core/data_sources.py`)

| Source | Provides | Method | Cache TTL |
|--------|----------|--------|-----------|
| **yfinance** | Historical prices, fundamentals, corporate actions | Python library (`.NS`/`.BO` suffixes) | 15 min (prices), 24h (fundamentals) |
| **NSE India** | Options chain, FII/DII data, bulk/block deals, bhavcopy, index constituents | HTTP with session management and rotating User-Agent headers | 15 min |
| **BSE India** | Corporate filings, SME listings, promoter shareholding patterns | REST API + scraping | 1 hour |
| **AMFI** | MF NAVs, AUM, SIP data, category-wise flows | Public CSV endpoints | 24 hours |
| **SEBI Corporate Filings** | Insider trading (SAST) disclosures, takeover announcements | SEBI website (sebi.gov.in) + NSE/BSE corporate announcements API | 24 hours |
| **RBI** | USD/INR reference rates, FPI limits, monetary policy dates | Public data feeds | 24 hours |

Each fetcher class provides:
- Built-in rate limiting (NSE: max 3 req/sec, BSE: max 5 req/sec)
- Automatic retry with exponential backoff (max 3 retries)
- Response caching with configurable TTL
- Standardized output: pandas DataFrames with consistent column naming
- Error handling: clear messages when source is down or data unavailable

### 3.2 Formatters (`core/formatters.py`)

- **Terminal tables** — Using `rich` library for colored, sortable tables
- **Markdown tables** — For Claude Code's native rendering
- **Heatmaps** — ANSI color-coded cells (green = positive/bullish, red = negative/bearish)
- **Sparklines** — Inline ASCII trend charts (e.g., `▁▂▃▅▇▅▃` for price movement)
- **Narrative generator** — Template-based natural language summaries for each skill's output

### 3.3 Exporters (`core/exporters.py`)

- **CSV** — Timestamped file (`nse_screener_2026-03-26_143022.csv`)
- **JSON** — Structured with metadata (query params, timestamp, source)
- **Python code** — Generates a standalone `.py` script that reproduces the analysis using only `yfinance` + `pandas`
- **DataFrame** — Returns raw pandas DataFrame for pipeline integration

### 3.4 Constants & Configuration (`core/constants.py` + `config/`)

Frequently-changing data is stored in **editable YAML config files** (not hardcoded in Python):

```
config/
├── holidays.yaml          # NSE/BSE trading holidays (update annually)
├── lot_sizes.yaml         # F&O lot sizes (update quarterly from NSE circulars)
├── tax_rules.yaml         # STCG/LTCG rates, exemptions (update after each Union Budget)
├── stt_rates.yaml         # STT rates by instrument type (update after Budget)
└── sebi_categories.yaml   # MF category definitions, MWPL thresholds
```

Each config file includes a `last_updated` and `effective_from` field so users know if their data is stale. Python constants that rarely change (Nifty sectoral index constituents, grandfathering date 31-Jan-2018) remain in `constants.py`.

**Current values (post-Union Budget 2024):**
- Tax: STCG 20%, LTCG 12.5% above Rs 1.25L exemption
- SEBI MF categories: Large Cap = top 100 by mcap, Mid = 101-250, Small = 251+
- Tax rates must be reviewed and updated after each Union Budget

### 3.5 Cache (`core/cache.py`)

- File-based cache using `platformdirs.user_cache_dir("nse-skills")` for cross-platform support (Windows, Linux, macOS)
- Override via `NSE_SKILLS_CACHE_DIR` environment variable
- Configurable TTL per data type
- Cache invalidation on trading day boundaries (auto-detects holidays)
- Max cache size with LRU eviction

### 3.6 Timezone Handling

All date/time logic uses **IST (Asia/Kolkata, UTC+5:30)** regardless of system timezone. "Today" and trading day boundaries are always computed in IST. Timestamps in output and cache keys use IST.

### 3.7 Data Source Authentication (`core/auth.py`)

Some endpoints may require API keys or throttle aggressively. Configuration via environment variables or `~/.nse-skills/credentials.yaml`:

```yaml
# Optional — skills work without these but with reduced data availability
bse_api_key: ""        # BSE API key (if required for certain endpoints)
amfi_api_key: ""       # For granular AMFI flow data
```

When authentication is needed but not provided, skills degrade gracefully with a message indicating what additional data would be available with credentials.

---

## 4. Skill Specifications

### 4.1 `/nse-screener` — NSE Stock Screener

**Purpose:** Multi-factor stock screening with India-specific filters unavailable in global screeners.

**Parameters (all optional, interactive prompting if omitted):**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `sector` | string | Nifty sectoral classification | All |
| `market_cap` | string | Large/Mid/Small/Micro or range in Cr | All |
| `filters` | dict | PE, PB, ROE, ROCE, D/E, div yield, rev growth | None |
| `india_filters` | dict | Promoter %, FII %, DII %, pledge %, free float | None |
| `sort_by` | string | Any metric | composite_score |
| `limit` | int | Number of results | 20 |
| `export` | string | csv/json/python/none | none |

**Data flow:**
1. Fetch universe from NSE (index constituents or full listed stocks)
2. Pull fundamentals from yfinance (PE, PB, ROE, etc.)
3. Pull shareholding patterns from NSE/BSE (promoter, FII, DII, pledge)
4. Apply filters, compute composite score, rank
5. Format output with red/green flags

**Composite score formula:**
- Quality: ROE (25%) + ROCE (25%)
- Value: PE percentile within sector (20%)
- Safety: Low debt/equity (15%) + Low pledge (15%)
- FII trend adjustment: +5 bonus points if FII holding increased in last 2 quarters, -5 if decreased, 0 otherwise. Final score = base (0-100) + adjustment, capped at [0, 100]

**Output:** Ranked table + narrative summary highlighting flags.

---

### 4.2 `/fii-dii-tracker` — FII/DII Flow Tracker

**Purpose:** Decode institutional money flow — the single biggest driver of Indian market direction.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `period` | string | 1d/1w/1m/3m/custom | 1m |
| `segment` | string | cash/fo/both | both |
| `correlation` | bool | Show Nifty correlation | true |
| `export` | string | csv/json/python/none | none |

**Analysis logic:**
1. Fetch daily FII/DII buy/sell from NSE
2. Compute net flows, 5-day and 20-day rolling averages
3. Detect divergence patterns:
   - FII selling + DII buying = institutional rotation (historically mid-term bullish)
   - Both selling = risk-off (bearish signal)
   - FII buying + Nifty flat = accumulation before breakout
4. Correlate with USD/INR movement (FII flows are FX-sensitive)
5. Compute cumulative flow vs Nifty return for the period

**Output:** Daily flow heatmap + trend sparklines + divergence flags + narrative interpretation.

---

### 4.3 `/nse-options-chain` — NSE Options Chain Analyzer

**Purpose:** Options chain analysis tuned to NSE's unique structure.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `symbol` | string | NIFTY/BANKNIFTY/FINNIFTY/stock | NIFTY |
| `expiry` | string | nearest/next_week/monthly/date | nearest |
| `strikes` | int | Number of strikes around ATM | 10 |
| `analysis` | string | oi_buildup/max_pain/iv_skew/pcr/all | all |
| `export` | string | csv/json/python/none | none |

**Analysis logic:**
1. Fetch live options chain from NSE (requires session cookie handling)
2. Compute: PCR (volume-based and OI-based), max pain strike, IV percentile for each strike
3. OI buildup classification per strike:
   - Price up + OI up = Long buildup (bullish)
   - Price down + OI up = Short buildup (bearish)
   - Price up + OI down = Short covering (bullish, weak)
   - Price down + OI down = Long unwinding (bearish, weak)
4. Identify highest OI concentration on CE/PE side (resistance/support)
5. Track change in OI vs previous close
6. Flag stocks near/in F&O ban (OI > 95% of MWPL)

**Output:** Strike-wise OI table with color-coded buildup, max pain level, PCR gauge, support/resistance levels.

---

### 4.4 `/sebi-deal-scanner` — SEBI Insider & Bulk Deal Scanner

**Purpose:** Surface insider activity most retail investors miss.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `deal_type` | string | bulk/block/insider/all | all |
| `period` | string | 1d/1w/1m | 1w |
| `symbol` | string | Filter for specific stock | None (all) |
| `min_value` | float | Minimum deal value in Cr | 1.0 |
| `export` | string | csv/json/python/none | none |

**Analysis logic:**
1. Fetch bulk/block deals from NSE/BSE
2. Fetch SAST disclosures from SEBI corporate filings portal and NSE/BSE corporate announcements
3. Classify entities: Promoter / FII / DII / HNI / Unknown
4. Pattern detection:
   - Repeated buying by same entity across days
   - Promoter buying at/near 52-week low
   - PE/VC fund exits (large block deals)
   - Multiple insiders buying simultaneously
5. Compute deal value as % of ADTV (Average Daily Traded Value)

**Output:** Deal table with entity classification + pattern flags + liquidity impact assessment.

---

### 4.5 `/promoter-analyzer` — Promoter Holding & Pledge Analyzer

**Purpose:** Track promoter behavior — the signal most correlated with long-term stock performance in India.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `symbol` | string | NSE stock symbol | Required |
| `quarters` | int | Number of quarters to analyze | 8 |
| `export` | string | csv/json/python/none | none |

**Analysis logic:**
1. Fetch quarterly shareholding patterns from BSE
2. Track: promoter %, pledge %, FII %, DII %, public %
3. Compute QoQ changes for each category
4. Red flag detection:
   - Pledge > 40% of promoter holding
   - Pledge increasing 3+ consecutive quarters
   - Promoter stake declining + pledge increasing (double red flag)
   - Entity reclassification from promoter to public
   - Related party transactions > 10% of revenue
5. Green flag detection:
   - Promoter increasing stake via open market purchase
   - Pledge reduction trend (3+ quarters)
   - Creeping acquisition toward SEBI thresholds (25%, 49%, 75%)

**Output:** Quarter-wise trend table with sparklines + red/green flag narrative + price overlay.

---

### 4.6 `/fo-strategy` — Indian F&O Strategy Builder

**Purpose:** Build and evaluate derivative strategies using India's specific F&O structure.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `symbol` | string | F&O stock or index | Required |
| `outlook` | string | bullish/bearish/neutral/high_vol/low_vol | Required |
| `capital` | float | Available margin in INR | Optional |
| `strategy` | string | auto/straddle/strangle/spread/iron_condor/butterfly/etc | auto |
| `expiry` | string | nearest/next_week/monthly | nearest |
| `export` | string | csv/json/python/none | none |

**Analysis logic:**
1. Fetch current options prices, lot size, and MWPL from NSE
2. If `strategy=auto`: recommend top 2-3 strategies based on outlook + IV percentile + capital
3. Build strategy legs with live market prices
4. Compute:
   - Margin requirement (SPAN-like estimation using NSE's margin calculator logic)
   - Max profit, max loss, breakeven points
   - Risk-reward ratio
   - Probability of profit (using IV-derived normal distribution)
5. STT impact analysis:
   - STT on exercised ITM options (rate per `config/stt_rates.yaml`) — unique to India
   - Warning if strategy involves legs likely to expire ITM
6. Generate ASCII payoff diagram

**Output:** Strategy summary, legs table, ASCII payoff diagram, margin/STT breakdown, probability analysis.

---

### 4.7 `/mf-flow-analyzer` — Mutual Fund & SIP Flow Analyzer

**Purpose:** Track where India's domestic savings flow through mutual funds.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `period` | string | 1m/3m/6m/12m/custom | 3m |
| `category` | string | equity/debt/hybrid/all/specific sub-category | all |
| `analysis` | string | net_flows/sip_trends/nfo/aum_changes/all | all |
| `export` | string | csv/json/python/none | none |

**Analysis logic:**
1. Fetch AMFI monthly data — category-wise inflows/outflows
2. Track SIP book size trend (structural market floor indicator)
3. Identify sector rotation via category flow direction:
   - Large cap vs Mid vs Small cap flows
   - Thematic fund launches (signal of AMC conviction)
4. NFO analysis: themes AMCs are launching = forward-looking sector bets
5. Compare MF flow direction with FII flows:
   - MF buying when FII selling = strong domestic conviction
   - Both buying = broad rally fuel
6. Compute total industry AUM and growth rate

**Output:** Category flow heatmap, SIP trend sparkline, sector rotation matrix, FII-vs-MF divergence chart, narrative.

---

### 4.8 `/sector-rotation` — India Sector Rotation Tracker

**Purpose:** Map Indian sectoral cycles to India-specific macro triggers global models miss.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `period` | string | 3m/6m/1y | 6m |
| `benchmark` | string | nifty_50/nifty_500 | nifty_50 |
| `triggers` | bool | Show macro trigger overlay | true |
| `export` | string | csv/json/python/none | none |

**Analysis logic:**
1. Fetch all Nifty sectoral indices, compute relative performance vs benchmark
2. Compute momentum: 1M, 3M, 6M relative strength
3. Overlay India-specific macro triggers:
   - **Monsoon** (IMD data) → Agri, FMCG rural, Fertilizer, Tractor
   - **Govt capex** (Union Budget allocations, order books) → Infra, Defence, Railways
   - **USD/INR** → IT services (positive), Oil & Gas (negative)
   - **RBI policy** (repo rate, liquidity) → Banks, NBFCs, Real Estate
   - **FDA/USFDA approvals/warnings** → Pharma
   - **China+1 diversification** → Chemicals, Electronics, Textiles
4. Sector lifecycle classification: Early cycle / Mid cycle / Late cycle / Defensive
5. Identify rotation direction: money flowing from which sector to which

**Output:** Sector performance table with relative strength ranking, macro trigger matrix, rotation narrative with actionable sector calls.

---

### 4.9 `/tax-calculator` — Indian Tax-Aware P&L Calculator

**Purpose:** Compute Indian capital gains tax — uniquely complex with grandfathering, STT, and dual LTCG/STCG rates.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `holdings` | list/file | (symbol, buy_date, buy_price, qty) or CSV path | Required |
| `sell_price` | string | current/specific price | current |
| `financial_year` | string | FY for computation | Auto-detected from system date (IST) |
| `include_dividends` | bool | Factor in dividend income | false |
| `tax_slab` | string | 0/5/10/15/20/30 (for dividend taxation) | 30 |
| `export` | string | csv/json/python/none | none |

**Analysis logic:**
1. Classify each holding: STCG (held < 12 months) vs LTCG (held >= 12 months)
2. For LTCG:
   - Cost of acquisition: actual cost for post-31-Jan-2018 purchases
   - Grandfathering: for pre-31-Jan-2018 holdings, cost = max(actual cost, FMV as on 31/01/2018, but capped at sale price)
   - Exemption: Rs 1.25 lakh per FY (FY 2024-25 onwards)
   - Tax rate: 12.5% on gains exceeding exemption
3. For STCG:
   - Tax rate: 20% flat (listed equity with STT paid)
4. STT: verify STT was paid on buy-side (required for concessional equity tax treatment)
5. Dividend income: taxable at slab rate, TDS of 10% above Rs 5,000
6. **Tax-loss harvesting:** identify holdings with unrealized losses that can offset gains
7. Optimization: suggest which lots to sell first (FIFO vs specific lot identification)

**Output:** Holding-wise tax breakdown, total liability summary, harvesting recommendations, FY comparison.

---

### 4.10 `/smallcap-discovery` — Smallcap & Microcap Discovery

**Purpose:** Uncover quality small/micro caps in India's under-researched segments.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `market_cap_max` | float | Upper limit in Cr | 1000 |
| `market_cap_min` | float | Lower limit in Cr | 50 |
| `exchange` | string | nse/bse/bse_sme/nse_emerge/all | all |
| `quality_filters` | dict | Piotroski, Altman Z, cash flow, governance | All enabled |
| `sector` | string | Sector filter | None (all) |
| `limit` | int | Number of results | 15 |
| `export` | string | csv/json/python/none | none |

**Analysis logic:**
1. Scan BSE SME, NSE Emerge, and main board stocks within market cap range
2. Quality scoring:
   - **Piotroski F-Score** (0-9, prefer >6): with Ind-AS adjustments:
     - Profitability: ROA, CFO, delta ROA, accruals (accruals computation excludes Ind-AS 116 lease liabilities)
     - Leverage: delta leverage (net debt excluding lease obligations per Ind-AS 116), delta current ratio, equity dilution
     - Efficiency: delta gross margin, delta asset turnover (total assets adjusted for right-of-use assets)
   - **Altman Z-Score** — using the Emerging Markets adaptation (Z'' = 3.25 + 6.56*X1 + 3.26*X2 + 6.72*X3 + 1.05*X4, where X1=Working Capital/TA, X2=Retained Earnings/TA, X3=EBIT/TA, X4=Book Value Equity/Total Liabilities). Thresholds: >2.60 safe, <1.10 distress
   - **Cash flow quality**: CFO/Net Income > 0.8 (earnings backed by cash)
   - **Governance flags**: Related party txns > 10% revenue, auditor changes in last 2 years, qualified audit opinions
3. Liquidity filter: ADTV > Rs 10 lakh (avoid illiquid traps)
   - **Data completeness gate:** Exclude stocks with fewer than 4 quarters of available financial data
4. Momentum overlay: 6M price performance + volume breakout detection
5. Compute composite discovery score (quality 60% + momentum 25% + liquidity 15%)

**Output:** Ranked discovery table with individual scores, governance flags, and watchlist-ready format.

---

## 5. Skill File Structure

Each skill `.md` file follows this template:

```markdown
---
name: skill-name
description: One-line description of what the skill does
---

# Skill Title

## Purpose
What this skill does and why it matters for Indian market analysis.

## Instructions
Step-by-step instructions for Claude Code on how to execute this skill:
1. Parse user parameters (prompt interactively for required params if missing)
2. Call the appropriate Python analysis module
3. Format and present results
4. Offer export options

## Parameters
Table of accepted parameters with types and defaults.

## Example Usage
Show 2-3 example invocations and expected output format.
```

---

## 6. Dependencies

### Python Packages

| Package | Purpose |
|---------|---------|
| `yfinance` | Stock data, fundamentals, corporate actions |
| `pandas` | Data manipulation and analysis |
| `numpy` | Numerical computations |
| `requests` | HTTP requests to NSE/BSE/SEBI |
| `beautifulsoup4` | HTML parsing for NSE/BSE/SEBI pages |
| `rich` | Terminal formatting (tables, colors, progress bars) |
| `platformdirs` | Cross-platform cache/config directory resolution |
| `aiohttp` | Async HTTP for concurrent data fetching |

### System Requirements
- Python 3.10+
- Internet access (all data sourced from public endpoints)

---

## 7. NSE Data Access Strategy

NSE India restricts programmatic access. The data layer uses a **tiered fallback strategy**:

**Tier 1 — yfinance (primary for most data):**
yfinance provides historical prices, fundamentals, corporate actions, and basic options data for `.NS`/`.BO` tickers. This is the default and most reliable source.

**Tier 2 — NSE website session-based access (for NSE-exclusive data):**
Used only when data is unavailable via yfinance (live options chain, FII/DII flows, bhavcopy, bulk deals). Approach:
1. Establish a session with standard browser headers
2. First request to `https://www.nseindia.com` to obtain session cookies
3. Use cookies for subsequent API calls to `https://www.nseindia.com/api/`
4. Rate limit: max 3 requests per second
5. On 403/429: back off 30 seconds, refresh session
6. Cache aggressively to minimize requests

**Tier 3 — Cached/offline data:**
When live sources fail, fall back to most recent cached data with a staleness warning.

**ToS disclaimer:** Users should review NSE's Terms of Service. This tool is intended for personal analysis and research. The data layer is designed as a pluggable backend — if NSE offers official API access (paid or otherwise), it can be swapped in without changing skill logic.

**Concurrency model:** For skills that scan many stocks (nse-screener, smallcap-discovery), use batch endpoints where available (NSE bhavcopy provides all stocks in a single file). For per-stock fetching, use `asyncio` + `aiohttp` with a semaphore-based rate limiter (max 3 concurrent requests to NSE, 5 to BSE). Progress indicator required for scans exceeding 30 seconds.

---

## 8. Error Handling

- **Data source unavailable:** Graceful fallback with clear message ("NSE data currently unavailable, showing cached data from X hours ago" or "Cannot proceed without live data for this analysis")
- **Ticker not found:** Suggest closest matches (fuzzy matching on NSE symbol list)
- **Insufficient data:** State what's missing and what analysis can still be performed
- **Rate limited:** Show cached data if available, otherwise estimate wait time
- **No results for filters:** Suggest relaxing filters, show which filter eliminated most candidates

---

## 9. Testing Strategy

- **Unit tests:** Each core module (data_sources, formatters, exporters) with mocked API responses
- **Integration tests:** Each skill end-to-end with cached sample data (avoid hitting live APIs in CI)
- **Sample data fixtures:** Captured real responses stored as JSON in `tests/fixtures/`
- **Validation tests:** Verify tax calculations against known scenarios, verify F-Score computation against manual calculation

---

## 10. Installation & Setup

### Step 1: Clone and install Python dependencies

```bash
git clone https://github.com/SuminPillai/NSE-STOCK-ANALYSIS-CLAUDE-SKILLS.git
cd NSE-STOCK-ANALYSIS-CLAUDE-SKILLS
pip install -r requirements.txt
```

### Step 2: Register skills with Claude Code

Add skill paths to your project's `.claude/settings.json` (or global `~/.claude/settings.json`):

```json
{
  "skills": {
    "nse-screener": "./skills/nse-screener/nse-screener.md",
    "fii-dii-tracker": "./skills/fii-dii-tracker/fii-dii-tracker.md",
    "nse-options-chain": "./skills/nse-options-chain/nse-options-chain.md",
    "sebi-deal-scanner": "./skills/sebi-deal-scanner/sebi-deal-scanner.md",
    "promoter-analyzer": "./skills/promoter-analyzer/promoter-analyzer.md",
    "fo-strategy": "./skills/fo-strategy/fo-strategy.md",
    "mf-flow-analyzer": "./skills/mf-flow-analyzer/mf-flow-analyzer.md",
    "sector-rotation": "./skills/sector-rotation/sector-rotation.md",
    "tax-calculator": "./skills/tax-calculator/tax-calculator.md",
    "smallcap-discovery": "./skills/smallcap-discovery/smallcap-discovery.md"
  }
}
```

### Step 3: Verify

In Claude Code, type `/nse-screener` — if the skill loads, you're set.

### Optional: Configure credentials

Copy `config/credentials.example.yaml` to `~/.nse-skills/credentials.yaml` and add any optional API keys for enhanced data access.
