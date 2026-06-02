# Trading Journal Risk Analyzer

A dependency-free Python CLI for reviewing trades before or after execution. It converts a journal entry into:

- position risk in dollars and percent of equity
- R-multiple target and realized result
- reward-to-risk ratio
- stop-loss distance
- simple behavior flags
- a structured review note

This is designed for traders who want a lightweight, repeatable checklist without connecting to a broker or exchange.

## Install

```bash
git clone https://github.com/jiamicuisi-a11y/trading-journal-risk-analyzer.git
cd trading-journal-risk-analyzer
python -m pip install -e .
```

## Quick start

Analyze a planned long trade:

```bash
trade-risk analyze \
  --symbol BTC-USDT \
  --side long \
  --entry 68000 \
  --stop 66400 \
  --target 72000 \
  --size 0.2 \
  --equity 50000 \
  --reason "breakout retest with market structure support"
```

Example output:

```text
BTC-USDT long review
Risk: $320.00 / 0.64% equity
Reward: $800.00
R multiple: 2.50R
Verdict: acceptable

Notes:
- Risk is inside the default 1.00% limit
- Reward-to-risk is healthy
- Journal reason supplied
```

## Commands

### Analyze a single trade

```bash
trade-risk analyze --symbol ETH-USDT --side short --entry 3500 --stop 3600 --target 3200 --size 1 --equity 20000
```

### Export JSON

```bash
trade-risk analyze --symbol BTC --side long --entry 100 --stop 90 --target 130 --size 2 --equity 10000 --json
```

### Create a review template

```bash
trade-risk template --symbol BTC-USDT
```

## Default checks

| Check | Default | Meaning |
|---|---:|---|
| Max account risk | 1.0% | Warns when position risk exceeds this |
| Minimum R multiple | 1.5R | Warns when target reward is too low |
| Stop distance | Informational | Highlights unusually tight/wide plans |
| Journal reason | Required for clean review | Empty reasons are flagged |

## Development

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
```

## Disclaimer

This tool is for journaling, simulation, and risk review only. It does not place trades and is not financial advice.
