"""Backtesting framework engine.

Core abstractions:
    - Signal: enum for BUY / SELL / HOLD
    - Strategy: base class users subclass to implement trading logic
    - Portfolio: tracks cash, positions, and trade history
    - Backtester: runs a Strategy against historical data and produces results
    - BacktestResult: holds performance metrics and trade log
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

class Signal(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


# ---------------------------------------------------------------------------
# Trade record
# ---------------------------------------------------------------------------

@dataclass
class Trade:
    date: Any
    ticker: str
    action: str          # "BUY" or "SELL"
    shares: float
    price: float
    value: float         # shares * price
    commission: float = 0.0


# ---------------------------------------------------------------------------
# Portfolio
# ---------------------------------------------------------------------------

class Portfolio:
    """Tracks cash, open positions, and completed trades."""

    def __init__(self, initial_cash: float = 10_000.0, commission: float = 0.0):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.commission = commission          # flat $ per trade
        self.positions: dict[str, float] = {}  # ticker -> shares held
        self.trades: list[Trade] = []
        self._equity_curve: list[float] = []

    # -- actions -----------------------------------------------------------

    def buy(self, date, ticker: str, price: float, shares: float | None = None):
        """Buy shares. If *shares* is None, go all-in with available cash."""
        if shares is None:
            affordable = math.floor((self.cash - self.commission) / price)
            shares = max(affordable, 0)
        cost = shares * price + self.commission
        if cost > self.cash or shares <= 0:
            return
        self.cash -= cost
        self.positions[ticker] = self.positions.get(ticker, 0) + shares
        self.trades.append(Trade(date, ticker, "BUY", shares, price, shares * price, self.commission))

    def sell(self, date, ticker: str, price: float, shares: float | None = None):
        """Sell shares. If *shares* is None, sell entire position."""
        held = self.positions.get(ticker, 0)
        if held <= 0:
            return
        if shares is None:
            shares = held
        shares = min(shares, held)
        revenue = shares * price - self.commission
        self.cash += revenue
        self.positions[ticker] = held - shares
        if self.positions[ticker] == 0:
            del self.positions[ticker]
        self.trades.append(Trade(date, ticker, "SELL", shares, price, shares * price, self.commission))

    # -- valuation ---------------------------------------------------------

    def total_value(self, prices: dict[str, float]) -> float:
        """Total portfolio value = cash + market value of all positions."""
        position_value = sum(self.positions.get(t, 0) * prices.get(t, 0) for t in self.positions)
        return self.cash + position_value

    def record_equity(self, value: float):
        self._equity_curve.append(value)

    @property
    def equity_curve(self) -> list[float]:
        return self._equity_curve


# ---------------------------------------------------------------------------
# Strategy (base class)
# ---------------------------------------------------------------------------

class Strategy:
    """Subclass this and implement `init` and `generate_signal`."""

    name: str = "BaseStrategy"

    def init(self, df: pd.DataFrame) -> pd.DataFrame:
        """Called once before the backtest loop.

        Use this to pre-compute indicators and attach them to *df*.
        Must return the (possibly modified) DataFrame.
        """
        return df

    def generate_signal(self, row: pd.Series, i: int, df: pd.DataFrame) -> Signal:
        """Called on each bar. Return a Signal."""
        return Signal.HOLD


# ---------------------------------------------------------------------------
# Backtest result
# ---------------------------------------------------------------------------

@dataclass
class BacktestResult:
    strategy_name: str
    ticker: str
    start_date: str
    end_date: str
    initial_cash: float
    final_value: float
    total_return_pct: float
    buy_and_hold_return_pct: float
    annualized_return_pct: float
    max_drawdown_pct: float
    sharpe_ratio: float
    sortino_ratio: float
    win_rate_pct: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win_pct: float
    avg_loss_pct: float
    profit_factor: float
    equity_curve: list[float]
    trades: list[Trade]
    dates: list

    def summary(self) -> str:
        lines = [
            f"{'='*60}",
            f"  Backtest Results: {self.strategy_name}",
            f"  Ticker: {self.ticker}  |  {self.start_date} -> {self.end_date}",
            f"{'='*60}",
            f"  Initial Capital:      ${self.initial_cash:>12,.2f}",
            f"  Final Value:          ${self.final_value:>12,.2f}",
            f"  Total Return:          {self.total_return_pct:>11.2f}%",
            f"  Buy & Hold Return:     {self.buy_and_hold_return_pct:>11.2f}%",
            f"  Annualized Return:     {self.annualized_return_pct:>11.2f}%",
            f"  Max Drawdown:          {self.max_drawdown_pct:>11.2f}%",
            f"  Sharpe Ratio:          {self.sharpe_ratio:>11.2f}",
            f"  Sortino Ratio:         {self.sortino_ratio:>11.2f}",
            f"{'─'*60}",
            f"  Total Trades:          {self.total_trades:>8}",
            f"  Winning Trades:        {self.winning_trades:>8}",
            f"  Losing Trades:         {self.losing_trades:>8}",
            f"  Win Rate:              {self.win_rate_pct:>11.2f}%",
            f"  Avg Win:               {self.avg_win_pct:>11.2f}%",
            f"  Avg Loss:              {self.avg_loss_pct:>11.2f}%",
            f"  Profit Factor:         {self.profit_factor:>11.2f}",
            f"{'='*60}",
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Backtester
# ---------------------------------------------------------------------------

class Backtester:
    """Run a Strategy over historical data and collect results."""

    def __init__(
        self,
        strategy: Strategy,
        df: pd.DataFrame,
        ticker: str = "UNKNOWN",
        initial_cash: float = 10_000.0,
        commission: float = 0.0,
    ):
        self.strategy = strategy
        self.df = df.copy()
        self.ticker = ticker
        self.initial_cash = initial_cash
        self.commission = commission

    def run(self) -> BacktestResult:
        # Let strategy pre-compute indicators
        df = self.strategy.init(self.df)
        portfolio = Portfolio(initial_cash=self.initial_cash, commission=self.commission)

        for i in range(len(df)):
            row = df.iloc[i]
            price = row["Close"]
            signal = self.strategy.generate_signal(row, i, df)

            if signal == Signal.BUY:
                portfolio.buy(df.index[i], self.ticker, price)
            elif signal == Signal.SELL:
                portfolio.sell(df.index[i], self.ticker, price)

            equity = portfolio.total_value({self.ticker: price})
            portfolio.record_equity(equity)

        # Force close any open position at last price
        last_price = df.iloc[-1]["Close"]
        if self.ticker in portfolio.positions:
            portfolio.sell(df.index[-1], self.ticker, last_price)

        return self._compute_results(df, portfolio)

    # -- metrics -----------------------------------------------------------

    def _compute_results(self, df: pd.DataFrame, portfolio: Portfolio) -> BacktestResult:
        equity = np.array(portfolio.equity_curve)
        returns = np.diff(equity) / equity[:-1] if len(equity) > 1 else np.array([0.0])

        # Total return
        final_value = equity[-1] if len(equity) else self.initial_cash
        total_return = (final_value - self.initial_cash) / self.initial_cash * 100

        # Buy & hold
        bh_return = (df.iloc[-1]["Close"] - df.iloc[0]["Close"]) / df.iloc[0]["Close"] * 100

        # Annualized return
        n_days = (df.index[-1] - df.index[0]).days if hasattr(df.index[-1], "days") or True else 1
        try:
            n_days = (df.index[-1] - df.index[0]).days
        except Exception:
            n_days = len(df)
        n_days = max(n_days, 1)
        ann_return = ((final_value / self.initial_cash) ** (365.0 / n_days) - 1) * 100

        # Max drawdown
        peak = np.maximum.accumulate(equity)
        drawdown = (peak - equity) / peak * 100
        max_dd = float(drawdown.max()) if len(drawdown) else 0.0

        # Sharpe ratio (annualized, risk-free = 0)
        sharpe = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0.0

        # Sortino ratio
        downside = returns[returns < 0]
        sortino = (returns.mean() / downside.std() * np.sqrt(252)) if len(downside) > 0 and downside.std() > 0 else 0.0

        # Trade analysis
        buy_prices: dict[str, list[float]] = {}
        wins, losses = [], []
        for t in portfolio.trades:
            if t.action == "BUY":
                buy_prices.setdefault(t.ticker, []).append(t.price)
            elif t.action == "SELL" and t.ticker in buy_prices and buy_prices[t.ticker]:
                buy_p = buy_prices[t.ticker].pop(0)
                pct = (t.price - buy_p) / buy_p * 100
                if pct >= 0:
                    wins.append(pct)
                else:
                    losses.append(pct)

        total_trades = len(wins) + len(losses)
        win_rate = (len(wins) / total_trades * 100) if total_trades > 0 else 0.0
        avg_win = float(np.mean(wins)) if wins else 0.0
        avg_loss = float(np.mean(losses)) if losses else 0.0
        gross_profit = sum(wins) if wins else 0.0
        gross_loss = abs(sum(losses)) if losses else 0.0
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float("inf") if gross_profit > 0 else 0.0

        return BacktestResult(
            strategy_name=self.strategy.name,
            ticker=self.ticker,
            start_date=str(df.index[0].date()) if hasattr(df.index[0], "date") else str(df.index[0]),
            end_date=str(df.index[-1].date()) if hasattr(df.index[-1], "date") else str(df.index[-1]),
            initial_cash=self.initial_cash,
            final_value=final_value,
            total_return_pct=total_return,
            buy_and_hold_return_pct=bh_return,
            annualized_return_pct=ann_return,
            max_drawdown_pct=max_dd,
            sharpe_ratio=float(sharpe),
            sortino_ratio=float(sortino),
            win_rate_pct=win_rate,
            total_trades=total_trades,
            winning_trades=len(wins),
            losing_trades=len(losses),
            avg_win_pct=avg_win,
            avg_loss_pct=avg_loss,
            profit_factor=profit_factor,
            equity_curve=portfolio.equity_curve,
            trades=portfolio.trades,
            dates=list(df.index),
        )
