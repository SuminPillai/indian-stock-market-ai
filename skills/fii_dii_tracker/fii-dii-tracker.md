---
name: fii-dii-tracker
description: Decode institutional money flow and identify institutional rotation or risk-off sentiment in the Indian market.
---

# FII/DII Flow Tracker

## Purpose
Decodes institutional money flow — the single biggest driver of Indian market direction. This skill helps users identify whether Foreign Institutional Investors (FII) and Domestic Institutional Investors (DII) are accumulating or offloading stocks, providing insights into short-to-mid-term market bullishness or bearishness.

## Instructions
Step-by-step instructions for Claude Code on how to execute this skill:
1. Parse user parameters (`period`, `segment`, `correlation`, `export`). Prompt interactively for any required parameters if missing.
2. Call the appropriate Python analysis module (`skills/fii_dii_tracker/tracker.py`).
3. Format and present the results: generate a daily flow heatmap, display trend sparklines, flag divergences, and provide a short narrative interpretation.
4. If the `export` parameter is specified, export the output accordingly.

## Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `period` | string | 1d/1w/1m/3m/custom | 1m |
| `segment` | string | cash/fo/both | both |
| `correlation` | bool | Show Nifty correlation | true |
| `export` | string | csv/json/python/none | none |

## Example Usage
- **Example 1:** Track 1 month FII/DII inflows in Cash segment
  `/fii-dii-tracker period="1m" segment="cash"`
  *Expected Output:* Heatmap of the last 1 month's FII and DII buying/selling in the cash market, highlighting divergence patterns and Nifty correlation.

- **Example 2:** Analyze both cash and F&O data over 1 week, omitting correlation chart
  `/fii-dii-tracker period="1w" segment="both" correlation=false`
  *Expected Output:* Formatted table and sparkline showing the rolling cash vs F&O institutional flow over the past week.
