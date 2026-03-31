---
name: sector-rotation
description: Map Indian sectoral cycles to India-specific macro triggers (e.g. Monsoon, RBI policy, USD/INR).
---

# India Sector Rotation Tracker

## Purpose
Maps Indian sectoral cycles to India-specific macro triggers that global models often miss. Analyzes money allocation movements and macro triggers (Monsoon data from IMD, Union budget spending, RBI policies) to identify early-, mid-, or late-cycle transitions for various segments of the Indian market.

## Instructions
Step-by-step instructions for Claude Code on how to execute this skill:
1. Parse user parameters (`period`, `benchmark`, `triggers`, `export`). 
2. Call `skills/sector_rotation/rotation.py`.
3. Fetch all Nifty sectoral indices up against the chosen `benchmark`.
4. Run momentum metrics and evaluate India-specific macro triggers across sectors (e.g., how the repo rate impacts Banks/NBFCs).
5. Output a performance table indicating relative strength, provide a macro trigger matrix, and output a narrative detailing capital flow rotation.

## Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `period` | string | 3m/6m/1y | 6m |
| `benchmark` | string | nifty_50/nifty_500 | nifty_50 |
| `triggers` | bool | Show macro trigger overlay | true |
| `export` | string | csv/json/python/none | none |

## Example Usage
- **Example 1:** View the 6 month rotation across all sectors vs NIFTY 100
  `/sector-rotation period="6m" benchmark="nifty_100"`
  *Expected Output:* Tells the user what sectors have outperformed the NIFTY 100 benchmark through money allocation mapping over the past 6 months.

- **Example 2:** Analyze Sector Rotation based off only Nifty 50 with no macro triggers
  `/sector-rotation triggers=false`
  *Expected Output:* Simple performance table evaluating rotation exclusively on standard price momentum logic.
