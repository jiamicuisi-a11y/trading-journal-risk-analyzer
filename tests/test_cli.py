from trading_journal_risk.cli import main


def test_cli_analyze_outputs_verdict(capsys):
    code = main([
        "analyze",
        "--symbol",
        "BTC",
        "--side",
        "long",
        "--entry",
        "100",
        "--stop",
        "90",
        "--target",
        "130",
        "--size",
        "2",
        "--equity",
        "10000",
        "--reason",
        "range breakout",
    ])

    out = capsys.readouterr().out
    assert code == 0
    assert "BTC long review" in out
    assert "Verdict: acceptable" in out


def test_cli_template(capsys):
    code = main(["template", "--symbol", "ETH-USDT"])

    out = capsys.readouterr().out
    assert code == 0
    assert "Trade Review — ETH-USDT" in out
