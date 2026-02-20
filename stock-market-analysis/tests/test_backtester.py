"""Unit tests for the backtesting framework."""

import numpy as np
import pandas as pd
import pytest

from stockanalysis.backtester import Portfolio, Strategy, Signal, Backtester


@pytest.fixture
def simple_df():
    """A simple uptrending DataFrame for testing."""
    dates = pd.date_range("2024-01-01", periods=50, freq="B")
    prices = np.linspace(100, 150, 50)  # steadily rising
    return pd.DataFrame({
        "Open": prices - 0.5,
        "High": prices + 1,
        "Low": prices - 1,
        "Close": prices,
        "Volume": [500_000] * 50,
    }, index=dates)


class TestPortfolio:
    def test_initial_state(self):
        p = Portfolio(initial_cash=10_000)
        assert p.cash == 10_000
        assert len(p.positions) == 0
        assert len(p.trades) == 0

    def test_buy_and_sell(self):
        p = Portfolio(initial_cash=10_000)
        p.buy("2024-01-01", "AAPL", price=100, shares=10)
        assert p.cash == pytest.approx(9_000)
        assert p.positions["AAPL"] == 10

        p.sell("2024-01-02", "AAPL", price=110, shares=10)
        assert p.cash == pytest.approx(10_100)
        assert "AAPL" not in p.positions

    def test_buy_all_in(self):
        p = Portfolio(initial_cash=1_000)
        p.buy("2024-01-01", "AAPL", price=100)
        assert p.positions["AAPL"] == 10
        assert p.cash == pytest.approx(0)

    def test_insufficient_funds(self):
        p = Portfolio(initial_cash=50)
        p.buy("2024-01-01", "AAPL", price=100, shares=1)
        assert len(p.positions) == 0  # trade should not execute

    def test_sell_entire_position(self):
        p = Portfolio(initial_cash=10_000)
        p.buy("2024-01-01", "AAPL", price=100, shares=5)
        p.sell("2024-01-02", "AAPL", price=110)  # sell all
        assert "AAPL" not in p.positions

    def test_commission(self):
        p = Portfolio(initial_cash=10_000, commission=5.0)
        p.buy("2024-01-01", "AAPL", price=100, shares=10)
        assert p.cash == pytest.approx(10_000 - 1_000 - 5)

    def test_total_value(self):
        p = Portfolio(initial_cash=10_000)
        p.buy("2024-01-01", "AAPL", price=100, shares=10)
        val = p.total_value({"AAPL": 120})
        assert val == pytest.approx(9_000 + 10 * 120)


class AlwaysBuyOnce(Strategy):
    """Buy on bar 5, sell on bar 40."""
    name = "TestBuyOnce"

    def generate_signal(self, row, i, df):
        if i == 5:
            return Signal.BUY
        if i == 40:
            return Signal.SELL
        return Signal.HOLD


class TestBacktester:
    def test_basic_run(self, simple_df):
        strategy = AlwaysBuyOnce()
        bt = Backtester(strategy, simple_df, ticker="TEST", initial_cash=10_000)
        result = bt.run()
        assert result.final_value > 0
        assert result.total_trades >= 1
        assert len(result.equity_curve) == len(simple_df)

    def test_profitable_uptrend(self, simple_df):
        strategy = AlwaysBuyOnce()
        bt = Backtester(strategy, simple_df, ticker="TEST", initial_cash=10_000)
        result = bt.run()
        # Buying at bar 5 (~105) and selling at bar 40 (~146) should be profitable
        assert result.total_return_pct > 0

    def test_result_has_all_fields(self, simple_df):
        strategy = AlwaysBuyOnce()
        bt = Backtester(strategy, simple_df, ticker="TEST")
        result = bt.run()
        assert result.strategy_name == "TestBuyOnce"
        assert result.ticker == "TEST"
        assert result.sharpe_ratio is not None
        assert result.max_drawdown_pct >= 0
        assert result.summary()  # should produce a string
