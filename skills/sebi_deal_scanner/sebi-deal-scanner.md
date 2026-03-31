---
name: sebi-deal-scanner
description: Surface SEBI insider and bulk deal activity that most retail investors miss.
---

# SEBI Insider & Bulk Deal Scanner

## Purpose
Surfaces insider trading activity, open market deals, and bulk/block deals tracked by SEBI. It detects patterns like repeated buying by promoters, accumulation at 52-week lows, or PE/VC fund exits to identify potential liquidity impacts.

## Instructions
Step-by-step instructions for Claude Code on how to execute this skill:
1. Parse user parameters (`deal_type`, `period`, `symbol`, `min_value`, `export`). 
2. Call the Python module `skills/sebi_deal_scanner/deal_scanner.py`, passing parameters to evaluate deals on NSE/BSE and SEBI portals.
3. Compute the deal value as a percentage of Average Daily Traded Value (ADTV), group by entity, and identify pattern flags (like "Promoter increasing stake").
4. Output a formatted deal table with entity classification, pattern flags, and liquidity impact assessment.
5. Offer export (CSV, JSON, Python) if `export` is provided.

## Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `deal_type` | string | bulk/block/insider/all | all |
| `period` | string | 1d/1w/1m | 1w |
| `symbol` | string | Filter for specific stock | None (all) |
| `min_value` | float | Minimum deal value in Cr | 1.0 |
| `export` | string | csv/json/python/none | none |

## Example Usage
- **Example 1:** Find any bulk/block/insider deals over 5 Cr made in the last week
  `/sebi-deal-scanner min_value=5.0 period="1w"`
  *Expected Output:* A table grouping transactions above 5 Cr, highlighting which entity made the transaction.

- **Example 2:** Check only insider trades over the past month
  `/sebi-deal-scanner deal_type="insider" period="1m"`
  *Expected Output:* Details of promoter or high level executive activity on shares of their company over 1 month.
