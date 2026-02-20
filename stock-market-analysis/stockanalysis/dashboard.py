"""Visualization dashboard using matplotlib.

Generates multi-panel charts showing price, indicators, and backtest results.
"""

import matplotlib
matplotlib.use("Agg")  # non-interactive backend for file output

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

from stockanalysis.indicators import add_all_indicators
from stockanalysis.backtester import BacktestResult


def plot_technical_analysis(df: pd.DataFrame, ticker: str, save_path: str = "technical_analysis.png"):
    """Plot a full technical analysis chart with 4 panels.

    Panels:
        1. Price + SMA + Bollinger Bands
        2. Volume + OBV
        3. RSI
        4. MACD
    """
    data = add_all_indicators(df)

    fig, axes = plt.subplots(4, 1, figsize=(16, 20), sharex=True,
                              gridspec_kw={"height_ratios": [3, 1, 1, 1]})
    fig.suptitle(f"{ticker} — Technical Analysis", fontsize=16, fontweight="bold")

    # -- Panel 1: Price + overlays ----------------------------------------
    ax = axes[0]
    ax.plot(data.index, data["Close"], label="Close", color="#1f77b4", linewidth=1.2)
    ax.plot(data.index, data["SMA_20"], label="SMA 20", color="#ff7f0e", linewidth=0.9, alpha=0.8)
    ax.plot(data.index, data["SMA_50"], label="SMA 50", color="#2ca02c", linewidth=0.9, alpha=0.8)
    ax.fill_between(data.index, data["BB_Upper"], data["BB_Lower"],
                     alpha=0.12, color="#9467bd", label="Bollinger Bands")
    ax.plot(data.index, data["BB_Upper"], color="#9467bd", linewidth=0.5, alpha=0.5)
    ax.plot(data.index, data["BB_Lower"], color="#9467bd", linewidth=0.5, alpha=0.5)
    ax.set_ylabel("Price ($)")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)

    # -- Panel 2: Volume ---------------------------------------------------
    ax = axes[1]
    colors = ["#2ca02c" if data["Close"].iloc[i] >= data["Close"].iloc[max(i-1, 0)]
              else "#d62728" for i in range(len(data))]
    ax.bar(data.index, data["Volume"], color=colors, alpha=0.6, width=0.8)
    ax.set_ylabel("Volume")
    ax.grid(True, alpha=0.3)

    # -- Panel 3: RSI ------------------------------------------------------
    ax = axes[2]
    ax.plot(data.index, data["RSI_14"], color="#e377c2", linewidth=1.0)
    ax.axhline(70, color="#d62728", linestyle="--", linewidth=0.7, alpha=0.7)
    ax.axhline(30, color="#2ca02c", linestyle="--", linewidth=0.7, alpha=0.7)
    ax.fill_between(data.index, 70, 100, alpha=0.08, color="#d62728")
    ax.fill_between(data.index, 0, 30, alpha=0.08, color="#2ca02c")
    ax.set_ylabel("RSI")
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)

    # -- Panel 4: MACD -----------------------------------------------------
    ax = axes[3]
    ax.plot(data.index, data["MACD"], label="MACD", color="#1f77b4", linewidth=1.0)
    ax.plot(data.index, data["MACD_Signal"], label="Signal", color="#ff7f0e", linewidth=0.9)
    hist = data["MACD_Histogram"]
    ax.bar(data.index, hist,
           color=["#2ca02c" if v >= 0 else "#d62728" for v in hist],
           alpha=0.4, width=0.8)
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.set_ylabel("MACD")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)

    # Format x-axis
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    fig.autofmt_xdate()
    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Technical analysis chart saved to {save_path}")


def plot_backtest_results(result: BacktestResult, save_path: str = "backtest_results.png"):
    """Plot backtest equity curve, drawdown, and trade markers."""
    equity = np.array(result.equity_curve)
    dates = result.dates[:len(equity)]

    fig, axes = plt.subplots(3, 1, figsize=(16, 14), sharex=True,
                              gridspec_kw={"height_ratios": [3, 1, 1]})
    fig.suptitle(f"Backtest: {result.strategy_name} on {result.ticker}", fontsize=16, fontweight="bold")

    # -- Panel 1: Equity curve + trades ------------------------------------
    ax = axes[0]
    ax.plot(dates, equity, label="Portfolio Value", color="#1f77b4", linewidth=1.2)
    ax.axhline(result.initial_cash, color="gray", linestyle="--", linewidth=0.7, alpha=0.7, label="Initial Capital")

    # Mark buy / sell trades
    for trade in result.trades:
        if trade.date in dates:
            idx = dates.index(trade.date)
            if trade.action == "BUY":
                ax.annotate("B", (trade.date, equity[idx]),
                           fontsize=7, color="#2ca02c", fontweight="bold",
                           ha="center", va="bottom")
            else:
                ax.annotate("S", (trade.date, equity[idx]),
                           fontsize=7, color="#d62728", fontweight="bold",
                           ha="center", va="top")

    ax.set_ylabel("Portfolio Value ($)")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)

    # -- Panel 2: Drawdown -------------------------------------------------
    ax = axes[1]
    peak = np.maximum.accumulate(equity)
    drawdown = (peak - equity) / peak * 100
    ax.fill_between(dates, drawdown, 0, color="#d62728", alpha=0.3)
    ax.plot(dates, drawdown, color="#d62728", linewidth=0.8)
    ax.set_ylabel("Drawdown (%)")
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3)

    # -- Panel 3: Daily returns --------------------------------------------
    ax = axes[2]
    returns = np.diff(equity) / equity[:-1] * 100
    colors = ["#2ca02c" if r >= 0 else "#d62728" for r in returns]
    ax.bar(dates[1:], returns, color=colors, alpha=0.5, width=0.8)
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.set_ylabel("Daily Return (%)")
    ax.grid(True, alpha=0.3)

    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    fig.autofmt_xdate()
    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Backtest results chart saved to {save_path}")


def plot_strategy_comparison(results: list[BacktestResult], save_path: str = "strategy_comparison.png"):
    """Compare equity curves of multiple strategies side by side."""
    fig, axes = plt.subplots(2, 1, figsize=(16, 12), gridspec_kw={"height_ratios": [2, 1]})
    fig.suptitle("Strategy Comparison", fontsize=16, fontweight="bold")

    colors = plt.cm.tab10.colors

    # -- Panel 1: Equity curves overlaid -----------------------------------
    ax = axes[0]
    for i, result in enumerate(results):
        equity = result.equity_curve
        dates = result.dates[:len(equity)]
        ax.plot(dates, equity, label=result.strategy_name, color=colors[i % len(colors)], linewidth=1.2)

    ax.axhline(results[0].initial_cash, color="gray", linestyle="--", linewidth=0.7, alpha=0.7)
    ax.set_ylabel("Portfolio Value ($)")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3)

    # -- Panel 2: Bar chart of key metrics ---------------------------------
    ax = axes[1]
    names = [r.strategy_name for r in results]
    x = np.arange(len(names))
    width = 0.2
    ax.bar(x - width, [r.total_return_pct for r in results], width, label="Total Return %", color=colors[0])
    ax.bar(x, [-r.max_drawdown_pct for r in results], width, label="Max Drawdown % (neg)", color=colors[1])
    ax.bar(x + width, [r.sharpe_ratio * 10 for r in results], width, label="Sharpe x10", color=colors[2])
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=9)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Strategy comparison chart saved to {save_path}")
