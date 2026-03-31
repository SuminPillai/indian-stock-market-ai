---
name: nse-screener
description: Multi-factor stock screening with India-specific filters unavailable in global screeners.
---

# NSE Stock Screener

## Purpose
This skill provides multi-factor stock screening with India-specific filters unavailable in global screeners. It ranks Indian stocks based on a composite score representing quality, value, safety, and institutional flow trends, making it an essential tool for Indian market analysis.

## Instructions
Step-by-step instructions for Claude Code on how to execute this skill:
1. Parse user parameters (`sector`, `market_cap`, `filters`, `india_filters`, `sort_by`, `limit`, `export`). Prompt interactively for any required parameters if missing or unclear.
2. Call the appropriate Python analysis module (`skills/nse_screener/screener.py`) with the provided parameters.
3. Format and present results as a ranked table and provide a narrative summary highlighting red/green flags.
4. Offer export options (CSV, JSON, Python code) if requested by the user.

## Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `sector` | string | Nifty sectoral classification | All |
| `market_cap` | string | Large/Mid/Small/Micro or range in Cr | All |
| `filters` | dict | PE, PB, ROE, ROCE, D/E, div yield, rev growth | None |
| `india_filters` | dict | Promoter %, FII %, DII %, pledge %, free float | None |
| `sort_by` | string | Any metric | `composite_score` |
| `limit` | int | Number of results | 20 |
| `export` | string | csv/json/python/none | none |

## Example Usage
- **Example 1:** Find high ROE smallcap IT stocks
  `/nse-screener sector="IT" market_cap="Small" filters={"ROE": ">20%"} limit=10`
  *Expected Output:* Ranks IT small caps filtering by ROE, displaying quality, value, safety scores and holding adjustments in a terminal-readable table.

- **Example 2:** Top 5 banks with high FII holding
  `/nse-screener sector="Banking" india_filters={"FII": ">15%"} limit=5`
  *Expected Output:* A table outputting 5 Banking stocks meeting the criteria, sorted by the composite score.
