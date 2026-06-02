import pytest

from trading_journal_risk.core import TradePlan, analyze_trade


def test_long_trade_risk_and_r_multiple():
    review = analyze_trade(
        TradePlan(
            symbol="BTC-USDT",
            side="long",
            entry=68000,
            stop=66400,
            target=72000,
            size=0.2,
            equity=50000,
            reason="breakout retest",
        )
    )

    assert review.risk_usd == 320
    assert review.reward_usd == 800
    assert review.r_multiple == 2.5
    assert review.verdict == "acceptable"


def test_short_trade_risk():
    review = analyze_trade(
        TradePlan(symbol="ETH", side="short", entry=3500, stop=3600, target=3200, size=1, equity=20000)
    )

    assert review.risk_usd == 100
    assert review.reward_usd == 300
    assert review.verdict == "journal_incomplete"


def test_invalid_stop_raises():
    with pytest.raises(ValueError):
        analyze_trade(TradePlan(symbol="BTC", side="long", entry=100, stop=110, target=120, size=1, equity=10000))
