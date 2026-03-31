---
name: smallcap-discovery
description: Uncover quality small/micro cap value traps and gems in under-researched Indian SME segments.
---

# Smallcap & Microcap Discovery

## Purpose
A unique discovery scanner structured for investigating Indian small caps across the BSE SME, NSE Emerge, and standard exchange boards. Specifically built to detect strong governance structures, quality cash flow backing, and Piotroski F-score reliability among highly volatile assets.

## Instructions
Step-by-step instructions for Claude Code on how to execute this skill:
1. Parse user parameters (`market_cap_max`, `market_cap_min`, `exchange`, `quality_filters`, `sector`, `limit`, `export`). 
2. Call Module `skills/smallcap_discovery/discovery.py`.
3. Fetch standard and SME Indian market data falling within the market cap thresholds.
4. Eliminate candidates failing basic viability markers (Average Daily Traded Value < 10 Lacs, incomplete financial data). 
5. Scan data and score quality using Piotroski F-Scores (Ind-AS Adjusted), emerging-market-adapted Altman Z-scores, cash flow validation, and governance checklists (auditor changes, insider transactions).
6. Rank remaining entries and generate an output highlighting the composite discovery scores, governance flags, and present a watchlist-ready format.

## Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `market_cap_max` | float | Upper limit in Cr | 1000 |
| `market_cap_min` | float | Lower limit in Cr | 50 |
| `exchange` | string | nse/bse/bse_sme/nse_emerge/all | all |
| `quality_filters` | dict | Piotroski, Altman Z, cash flow, governance | All enabled |
| `sector` | string | Sector filter | None (all) |
| `limit` | int | Number of results | 15 |
| `export` | string | csv/json/python/none | none |

## Example Usage
- **Example 1:** Filter discovery purely focused on BSE SME with max limit
  `/smallcap-discovery limit=10 exchange="bse_sme" market_cap_max=500`
  *Expected Output:* Top 10 BSE SME listings ranked by their discovery score (A mix of quality parameters like Piotroski alongside momentum and liquidity).

- **Example 2:** Discovery across standard NSE for small caps
  `/smallcap-discovery exchange="nse" market_cap_min=500 market_cap_max=3000`
  *Expected Output:* Discover new companies lying right under the standard market cap boundaries. Includes warnings regarding any found governance issues on selected companies.
