from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .core import TradePlan, analyze_trade


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="trade-risk", description="Trading journal risk analyzer")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze = sub.add_parser("analyze", help="Analyze a trade plan or journal entry")
    analyze.add_argument("--symbol", required=True)
    analyze.add_argument("--side", required=True, choices=["long", "short"])
    analyze.add_argument("--entry", required=True, type=float)
    analyze.add_argument("--stop", required=True, type=float)
    analyze.add_argument("--target", required=True, type=float)
    analyze.add_argument("--size", required=True, type=float)
    analyze.add_argument("--equity", required=True, type=float)
    analyze.add_argument("--reason", default="")
    analyze.add_argument("--max-risk-pct", default=1.0, type=float)
    analyze.add_argument("--min-r", default=1.5, type=float)
    analyze.add_argument("--json", action="store_true")

    template = sub.add_parser("template", help="Print a journal review template")
    template.add_argument("--symbol", default="")
    return parser


def render_review(review) -> str:
    lines = [
        f"{review.symbol} {review.side} review",
        f"Risk: ${review.risk_usd:.2f} / {review.risk_pct:.2f}% equity",
        f"Reward: ${review.reward_usd:.2f}",
        f"R multiple: {review.r_multiple:.2f}R",
        f"Stop distance: {review.stop_distance_pct:.2f}%",
        f"Verdict: {review.verdict}",
        "",
        "Notes:",
    ]
    lines.extend(f"- {note}" for note in review.notes)
    return "\n".join(lines)


def render_template(symbol: str) -> str:
    label = symbol or "SYMBOL"
    return f"""# Trade Review — {label}

## Plan
- Side:
- Entry:
- Stop:
- Target:
- Position size:
- Account equity:
- Setup reason:
- Invalidation condition:

## Risk
- Max allowed risk %:
- Actual risk %:
- R multiple:

## Behavior checklist
- [ ] I am not chasing after a missed move
- [ ] Stop is defined before entry
- [ ] Position size matches risk limit
- [ ] News/event risk checked
- [ ] Take-profit or management rule defined

## Review
- Result:
- What worked:
- What failed:
- Next adjustment:
"""


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "analyze":
        review = analyze_trade(
            TradePlan(
                symbol=args.symbol,
                side=args.side,
                entry=args.entry,
                stop=args.stop,
                target=args.target,
                size=args.size,
                equity=args.equity,
                reason=args.reason,
                max_risk_pct=args.max_risk_pct,
                min_r_multiple=args.min_r,
            )
        )
        print(json.dumps(asdict(review), indent=2) if args.json else render_review(review))
        return 0
    if args.command == "template":
        print(render_template(args.symbol))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
