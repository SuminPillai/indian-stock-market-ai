# NSE Stock Analysis Claude Skills

A suite of 10 Claude Code skills for analyzing stocks in the Indian stock market. Each skill is invocable via `/skill-name` in Claude Code, providing AI-assisted interactive analysis tailored to India-specific market structures, regulations, and data sources.

## Overview

This repository contains modular skills with a shared core that allow you to analyze Indian stocks using public APIs and libraries (yfinance, NSE/BSE websites, AMFI, SEBI). The skills output rich terminal analysis including markdown tables, heatmaps, sparklines, and offer export options.

## Features

- **Self-contained Data Sources:** Uses public APIs and libraries, avoiding dependencies on private infrastructure.
- **Rich Output:** Colored terminal tables, markdown tables, ANSI color-coded heatmaps, and inline ASCII sparklines.
- **Export Options:** Export analysis results to CSV, JSON, or standalone Python code.
- **Configurable Settings:** Configurable caching, tax rules, lot sizes, and SEBI categories.

## Skills Included

1. **`/nse-screener`** - Multi-factor stock screening with India-specific filters.
2. **`/fii-dii-tracker`** - Decode institutional money flow (FII/DII).
3. **`/nse-options-chain`** - Options chain analysis tuned to NSE's unique structure.
4. **`/sebi-deal-scanner`** - Surface insider & bulk deal activity.
5. **`/promoter-analyzer`** - Track promoter behavior, holding, and pledge patterns.
6. **`/fo-strategy`** - Build and evaluate derivative strategies using India's specific F&O structure.
7. **`/mf-flow-analyzer`** - Track mutual fund flows and SIP trends.
8. **`/sector-rotation`** - Map Indian sectoral cycles to India-specific macro triggers.
9. **`/tax-calculator`** - Indian tax-aware P&L calculator with STCG, LTCG, and STT considerations.
10. **`/smallcap-discovery`** - Uncover quality small/micro caps in India's under-researched segments.

## Installation & Setup

### Step 1: Clone the repository
```bash
git clone https://github.com/SuminPillai/NSE-STOCK-ANALYSIS-CLAUDE-SKILLS.git
cd NSE-STOCK-ANALYSIS-CLAUDE-SKILLS
```

*(Note: Ensure you have your `core/`, `tests/`, `config/`, and required Python scripts set up in your local copy.)*

### Step 2: Register skills with Claude Code
Add the skill paths to your project's `.claude/settings.json` (or global `~/.claude/settings.json`):

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

## Disclaimer
Users should review NSE's Terms of Service. This tool is intended for personal analysis and research.

With love from https://alphaquantixanalytics.com/
