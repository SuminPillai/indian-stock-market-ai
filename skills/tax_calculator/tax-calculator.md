---
name: tax-calculator
description: Compute Indian capital gains tax handling complex situations like grandfathering, STT, and LTCG/STCG rates.
---

# Indian Tax-Aware P&L Calculator

## Purpose
An intricate calculator necessary for properly computing capital gains taxation in India. Computes taxation thresholds considering historical constraints like 31-Jan-2018 grandfathering rules, short-term/long-term capital gains, security transaction taxes (STT), and tax-loss harvesting recommendations based on the Union Budget constraints.

## Instructions
Step-by-step instructions for Claude Code on how to execute this skill:
1. Call the user locally for `holdings` required if missing. Parse `sell_price`, `financial_year`, `include_dividends`, `tax_slab`, `export`.
2. Call `skills/tax_calculator/tax_calc.py`.
3. Assess the holdings: checking for the 12 month threshold and identifying grandfathering conditions for acquisitions pre Jan-31-2018. Apply the proper exemptions.
4. Verify if STT was paid on buy-sides, calculate dividend slabs to compile tax totals. Identify options to suggest what lots to sell first (Tax-loss harvesting).
5. Return a holding-by-holding tax breakdown, list total liability, recommend harvesting approaches, and present FY comparisons.

## Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `holdings` | list/file | (symbol, buy_date, buy_price, qty) or CSV path | Required |
| `sell_price` | string | current/specific price | current |
| `financial_year` | string | FY for computation | Auto-detected from system date (IST) |
| `include_dividends` | bool | Factor in dividend income | false |
| `tax_slab` | string | 0/5/10/15/20/30 (for dividend taxation) | 30 |
| `export` | string | csv/json/python/none | none |

## Example Usage
- **Example 1:** User uploading CSV file with their holdings to determine overall tax impact.
  `/tax-calculator holdings="portfolio.csv"`
  *Expected Output:* Calculates total LTCG and STCG tax due, incorporating current year exemptions limit, returning the optimal suggestions to handle un-realized losses.
