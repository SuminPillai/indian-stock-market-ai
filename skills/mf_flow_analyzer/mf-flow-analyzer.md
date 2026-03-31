---
name: mf-flow-analyzer
description: Track domestic savings flows through mutual funds and identify sector rotations via SIP books.
---

# Mutual Fund & SIP Flow Analyzer

## Purpose
Tracks how domestic capital flows through mutual funds (via AMFI data), helping users identify the growth of the SIP book (market floor index) and category-level inflows/outflows to predict future sector rotation. 

## Instructions
Step-by-step instructions for Claude Code on how to execute this skill:
1. Parse user parameters (`period`, `category`, `analysis`, `export`). 
2. Call `skills/mf_flow_analyzer/mf_flows.py`.
3. Track AMFI data for SIP book sizes, and plot large vs mid vs small cap flows. Note any new NFO launches as future thematic indicators.
4. Contrast MF flows against FII trends to define market fuel characteristics.
5. Present output through flow heatmaps, SIP trend sparklines, and an FII-vs-MF divergence chart + narrative text.
6. Handle any export requests.

## Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `period` | string | 1m/3m/6m/12m/custom | 3m |
| `category` | string | equity/debt/hybrid/all/specific sub-category | all |
| `analysis` | string | net_flows/sip_trends/nfo/aum_changes/all | all |
| `export` | string | csv/json/python/none | none |

## Example Usage
- **Example 1:** Analyze equity mutual fund flows over 6 months
  `/mf-flow-analyzer period="6m" category="equity"`
  *Expected Output:* A mapping of what equity categories (Small, Mid, Large) are getting the most domestic SIP inflows.

- **Example 2:** Analyze all MF AUM changes over 3 months
  `/mf-flow-analyzer analysis="aum_changes"`
  *Expected Output:* Heatmap detailing the industry total AUM growth.
