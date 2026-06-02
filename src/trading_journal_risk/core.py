from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TradePlan:
    symbol: str
    side: str
    entry: float
    stop: float
    target: float
    size: float
    equity: float
    reason: str = ""
    max_risk_pct: float = 1.0
    min_r_multiple: float = 1.5


@dataclass(slots=True)
class TradeReview:
    symbol: str
    side: str
    risk_usd: float
    risk_pct: float
    reward_usd: float
    r_multiple: float
    stop_distance_pct: float
    verdict: str
    notes: list[str]


def analyze_trade(plan: TradePlan) -> TradeReview:
    side = plan.side.lower()
    if side not in {"long", "short"}:
        raise ValueError("side must be 'long' or 'short'")
    if plan.entry <= 0 or plan.stop <= 0 or plan.target <= 0 or plan.size <= 0 or plan.equity <= 0:
        raise ValueError("entry, stop, target, size, and equity must be positive")

    if side == "long":
        risk_per_unit = plan.entry - plan.stop
        reward_per_unit = plan.target - plan.entry
    else:
        risk_per_unit = plan.stop - plan.entry
        reward_per_unit = plan.entry - plan.target

    if risk_per_unit <= 0:
        raise ValueError("stop must be on the risk side of entry")
    if reward_per_unit <= 0:
        raise ValueError("target must be on the reward side of entry")

    risk_usd = risk_per_unit * plan.size
    reward_usd = reward_per_unit * plan.size
    risk_pct = risk_usd / plan.equity * 100
    r_multiple = reward_usd / risk_usd
    stop_distance_pct = abs(plan.entry - plan.stop) / plan.entry * 100

    notes: list[str] = []
    if risk_pct <= plan.max_risk_pct:
        notes.append(f"Risk is inside the default {plan.max_risk_pct:.2f}% limit")
    else:
        notes.append(f"Risk exceeds the default {plan.max_risk_pct:.2f}% limit")

    if r_multiple >= plan.min_r_multiple:
        notes.append("Reward-to-risk is healthy")
    else:
        notes.append(f"Reward-to-risk is below {plan.min_r_multiple:.2f}R")

    if stop_distance_pct < 0.2:
        notes.append("Stop is very tight; watch noise and spread")
    elif stop_distance_pct > 8:
        notes.append("Stop is wide; check whether position size is too large")

    if plan.reason.strip():
        notes.append("Journal reason supplied")
    else:
        notes.append("Missing journal reason")

    verdict = verdict_for(risk_pct, r_multiple, bool(plan.reason.strip()), plan.max_risk_pct, plan.min_r_multiple)

    return TradeReview(
        symbol=plan.symbol,
        side=side,
        risk_usd=round(risk_usd, 2),
        risk_pct=round(risk_pct, 4),
        reward_usd=round(reward_usd, 2),
        r_multiple=round(r_multiple, 4),
        stop_distance_pct=round(stop_distance_pct, 4),
        verdict=verdict,
        notes=notes,
    )


def verdict_for(
    risk_pct: float, r_multiple: float, has_reason: bool, max_risk_pct: float, min_r_multiple: float
) -> str:
    if risk_pct > max_risk_pct * 1.5:
        return "too_risky"
    if risk_pct > max_risk_pct or r_multiple < min_r_multiple:
        return "needs_adjustment"
    if not has_reason:
        return "journal_incomplete"
    return "acceptable"
