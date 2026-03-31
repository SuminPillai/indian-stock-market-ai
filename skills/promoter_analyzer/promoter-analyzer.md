---
name: promoter-analyzer
description: Track promoter holding percentages and pledge behaviors, a key signal for Indian long-term performance.
---

# Promoter Holding & Pledge Analyzer

## Purpose
Tracks promoter holding percentages, public holdings, and the proportion of shares pledged by promoters. In the Indian market, changes in promoter behavior (e.g., increasing pledges or reducing stake) correlate heavily with long-term stock performance. This skill flags good patterns (creeping acquisition) and danger signs (pledge increasing 3+ quarters).

## Instructions
Step-by-step instructions for Claude Code on how to execute this skill:
1. Prompt interactively for the `symbol` parameter if it is not provided. Parse `quarters` and `export` as well.
2. Call `skills/promoter_analyzer/promoter.py`.
3. Fetch quarterly shareholding from BSE/NSE APIs to compute changes in holding blocks (Promoter%, Pledge%, FII%, DII%).
4. Detect red flags (like pledge > 40%) or green flags (promoter buying via open market).
5. Output a quarter-wise trend table with sparklines, red/green flag narratives. Include price overlays if applicable.

## Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `symbol` | string | NSE stock symbol | Required |
| `quarters` | int | Number of quarters to analyze | 8 |
| `export` | string | csv/json/python/none | none |

## Example Usage
- **Example 1:** Check RELIANCE for the past 8 quarters of promoter activity
  `/promoter-analyzer symbol="RELIANCE"`
  *Expected Output:* A table output of RELIANCE's promoter holding vs pledge amounts over 8 quarters, generating trend lines to spot patterns.

- **Example 2:** Analyze ADANIENT over 12 quarters
  `/promoter-analyzer symbol="ADANIENT" quarters=12`
  *Expected Output:* Trend table, with specific flags pointing to periods where pledge percentage increased heavily.
