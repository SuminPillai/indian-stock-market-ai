---
name: fo-strategy
description: Build and evaluate derivative strategies specific to India's F&O structure (lot setups, span margin, STT).
---

# Indian F&O Strategy Builder

## Purpose
Builds and evaluates derivative strategies tailored to India's specific Futures & Options structure. Ensures the user is aware of margin requirements (SPAN-like estimation) and physical settlement risks or STT impacts unique to the Indian market.

## Instructions
Step-by-step instructions for Claude Code on how to execute this skill:
1. Parse user parameters (`symbol`, `outlook`, `capital`, `strategy`, `expiry`, `export`). Demand `symbol` and `outlook` if missing.
2. Call the module at `skills/fo_strategy/strategy.py`.
3. Build optimal strategies (e.g. iron condor, spread) based on live NSE options data, calculating lot sizes, and maximum probable losses.
4. If `strategy="auto"`, recommend 2-3 strategies complementing the `outlook` and IV percentile.
5. Provide STT impact analysis (per `config/stt_rates.yaml`).
6. Present a strategy summary table, an ASCII payoff diagram, margin estimation, and probability analysis.

## Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `symbol` | string | F&O stock or index | Required |
| `outlook` | string | bullish/bearish/neutral/high_vol/low_vol | Required |
| `capital` | float | Available margin in INR | Optional |
| `strategy` | string | auto/straddle/strangle/spread/iron_condor/butterfly/etc | auto |
| `expiry` | string | nearest/next_week/monthly | nearest |
| `export` | string | csv/json/python/none | none |

## Example Usage
- **Example 1:** Suggest an auto F&O strategy for NIFTY assuming a bullish outlook.
  `/fo-strategy symbol="NIFTY" outlook="bullish"`
  *Expected Output:* Two bullish strategy recommendations (e.g., Bull Call Spread, Naked Put) with margin/STT tables and ASCII payoff diagrams.

- **Example 2:** Analyze an Iron Condor for BANKNIFTY next week
  `/fo-strategy symbol="BANKNIFTY" outlook="neutral" strategy="iron_condor" expiry="next_week" capital=300000.0`
  *Expected Output:* Complete strategy summary mapped against available capital, highlighting risk-reward ratio probability in an ASCII diagram.
