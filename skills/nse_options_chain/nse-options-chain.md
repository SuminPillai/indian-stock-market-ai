---
name: nse-options-chain
description: Options chain analysis tuned specifically to the NSE structure, tracking OI buildup and PCR.
---

# NSE Options Chain Analyzer

## Purpose
Performs options chain analysis tuned to the National Stock Exchange (NSE) unique structure. Helps investors and traders identify open interest (OI) buildup, maximum pain levels, put-call ratio (PCR), and F&O ban risks.

## Instructions
Step-by-step instructions for Claude Code on how to execute this skill:
1. Parse user parameters (`symbol`, `expiry`, `strikes`, `analysis`, `export`). If required parameters like `symbol` are missing, ask the user.
2. Call the appropriate Python analysis module (`skills/nse_options_chain/options_chain.py`).
3. Identify support/resistance, compute PCR/Max Pain, and assign OI buildups (bullish/bearish flags) to each strike. 
4. Format and present results as a strike-wise OI table with color-coded buildup, max pain level, and PCR gauge.
5. Offer to export the output to CSV, JSON, or Python code based on the `export` argument.

## Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `symbol` | string | NIFTY/BANKNIFTY/FINNIFTY/stock | NIFTY |
| `expiry` | string | nearest/next_week/monthly/date | nearest |
| `strikes` | int | Number of strikes around ATM | 10 |
| `analysis` | string | oi_buildup/max_pain/iv_skew/pcr/all | all |
| `export` | string | csv/json/python/none | none |

## Example Usage
- **Example 1:** Analyze NIFTY options chain for the nearest expiry
  `/nse-options-chain symbol="NIFTY" expiry="nearest"`
  *Expected Output:* A table displaying the 10 strikes around the ATM for NIFTY, highlighting short covering or long unwinding for calls and puts.

- **Example 2:** Look closely at HDFCBANK options for monthly OI buildup
  `/nse-options-chain symbol="HDFCBANK" expiry="monthly" analysis="oi_buildup" strikes=5`
  *Expected Output:* A localized OI buildup table of 5 strikes around HDFCBANK's ATM targeting the monthly expiry.
