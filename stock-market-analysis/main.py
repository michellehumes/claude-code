#!/usr/bin/env python3
"""Stock Market Analysis & Backtesting CLI.

Usage examples:
    # Analyze a single stock with technical indicators and charts
    python main.py analyze AAPL

    # Backtest a specific strategy
    python main.py backtest AAPL --strategy sma --cash 10000

    # Compare all built-in strategies on a ticker
    python main.py compare AAPL MSFT GOOGL --cash 10000

    # Quick summary of current indicator readings
    python main.py scan AAPL MSFT TSLA NVDA AMZN
"""

import argparse
import sys
import os

# Allow running from the project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stockanalysis.data import fetch_stock_data, fetch_multiple, get_stock_info
from stockanalysis.indicators import add_all_indicators, rsi, macd, bollinger_bands, sma, atr
from stockanalysis.backtester import Backtester, BacktestResult
from stockanalysis.dashboard import plot_technical_analysis, plot_backtest_results, plot_strategy_comparison
from strategies import (
    SMACrossoverStrategy,
    RSIMeanReversionStrategy,
    MACDStrategy,
    BollingerBandStrategy,
    CombinedStrategy,
)

STRATEGY_MAP = {
    "sma": SMACrossoverStrategy,
    "rsi": RSIMeanReversionStrategy,
    "macd": MACDStrategy,
    "bollinger": BollingerBandStrategy,
    "combined": CombinedStrategy,
}


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_analyze(args):
    """Fetch data, compute indicators, print summary, and generate charts."""
    print(f"\nFetching data for {args.ticker} (period={args.period})...")
    df = fetch_stock_data(args.ticker, period=args.period)

    data = add_all_indicators(df)
    latest = data.iloc[-1]

    print(f"\n{'='*60}")
    print(f"  {args.ticker} — Technical Analysis Summary")
    print(f"  Date: {data.index[-1].strftime('%Y-%m-%d') if hasattr(data.index[-1], 'strftime') else data.index[-1]}")
    print(f"{'='*60}")
    print(f"  Close:           ${latest['Close']:>10.2f}")
    print(f"  SMA 20:          ${latest['SMA_20']:>10.2f}")
    print(f"  SMA 50:          ${latest['SMA_50']:>10.2f}")
    print(f"  EMA 12:          ${latest['EMA_12']:>10.2f}")
    print(f"  EMA 26:          ${latest['EMA_26']:>10.2f}")
    print(f"{'─'*60}")
    print(f"  RSI (14):         {latest['RSI_14']:>10.2f}  {'(Overbought)' if latest['RSI_14'] > 70 else '(Oversold)' if latest['RSI_14'] < 30 else ''}")
    print(f"  MACD:             {latest['MACD']:>10.4f}")
    print(f"  MACD Signal:      {latest['MACD_Signal']:>10.4f}")
    print(f"  MACD Histogram:   {latest['MACD_Histogram']:>10.4f}  {'(Bullish)' if latest['MACD_Histogram'] > 0 else '(Bearish)'}")
    print(f"{'─'*60}")
    print(f"  Bollinger Upper:  ${latest['BB_Upper']:>10.2f}")
    print(f"  Bollinger Mid:    ${latest['BB_Middle']:>10.2f}")
    print(f"  Bollinger Lower:  ${latest['BB_Lower']:>10.2f}")
    print(f"  ATR (14):         ${latest['ATR_14']:>10.2f}")
    print(f"{'─'*60}")
    print(f"  VWAP:             ${latest['VWAP']:>10.2f}")
    print(f"  OBV:         {latest['OBV']:>14,.0f}")
    print(f"  Volume:      {latest['Volume']:>14,.0f}")
    print(f"{'='*60}")

    # Signal interpretation
    signals = []
    if latest["Close"] > latest["SMA_50"]:
        signals.append("Price ABOVE SMA 50 (bullish trend)")
    else:
        signals.append("Price BELOW SMA 50 (bearish trend)")

    if latest["RSI_14"] < 30:
        signals.append("RSI oversold — potential bounce")
    elif latest["RSI_14"] > 70:
        signals.append("RSI overbought — potential pullback")

    if latest["MACD_Histogram"] > 0:
        signals.append("MACD histogram positive (bullish momentum)")
    else:
        signals.append("MACD histogram negative (bearish momentum)")

    if latest["Close"] <= latest["BB_Lower"]:
        signals.append("Price at lower Bollinger Band (oversold)")
    elif latest["Close"] >= latest["BB_Upper"]:
        signals.append("Price at upper Bollinger Band (overbought)")

    print("\n  Signal Summary:")
    for s in signals:
        print(f"    - {s}")
    print()

    if not args.no_chart:
        chart_path = f"{args.ticker}_technical_analysis.png"
        plot_technical_analysis(df, args.ticker, save_path=chart_path)


def cmd_backtest(args):
    """Run a single strategy backtest."""
    strategy_cls = STRATEGY_MAP.get(args.strategy)
    if not strategy_cls:
        print(f"Unknown strategy: {args.strategy}. Choose from: {', '.join(STRATEGY_MAP)}")
        sys.exit(1)

    print(f"\nFetching data for {args.ticker} (period={args.period})...")
    df = fetch_stock_data(args.ticker, period=args.period)

    strategy = strategy_cls()
    bt = Backtester(strategy, df, ticker=args.ticker, initial_cash=args.cash, commission=args.commission)

    print(f"Running backtest: {strategy.name}...")
    result = bt.run()
    print(result.summary())

    if not args.no_chart:
        chart_path = f"{args.ticker}_{args.strategy}_backtest.png"
        plot_backtest_results(result, save_path=chart_path)


def cmd_compare(args):
    """Run all strategies on one or more tickers and compare."""
    all_results: list[BacktestResult] = []

    for ticker in args.tickers:
        print(f"\nFetching data for {ticker} (period={args.period})...")
        df = fetch_stock_data(ticker, period=args.period)

        for name, strategy_cls in STRATEGY_MAP.items():
            strategy = strategy_cls()
            bt = Backtester(strategy, df, ticker=ticker, initial_cash=args.cash, commission=args.commission)
            result = bt.run()
            all_results.append(result)

    # Print comparison table
    print(f"\n{'='*90}")
    print(f"  Strategy Comparison")
    print(f"{'='*90}")
    print(f"  {'Strategy':<30} {'Ticker':<8} {'Return':>10} {'MaxDD':>10} {'Sharpe':>8} {'WinRate':>8} {'Trades':>7}")
    print(f"  {'-'*30} {'-'*8} {'-'*10} {'-'*10} {'-'*8} {'-'*8} {'-'*7}")
    for r in all_results:
        print(f"  {r.strategy_name:<30} {r.ticker:<8} {r.total_return_pct:>9.2f}% {r.max_drawdown_pct:>9.2f}% {r.sharpe_ratio:>8.2f} {r.win_rate_pct:>7.1f}% {r.total_trades:>7}")
    print(f"{'='*90}\n")

    if not args.no_chart and len(args.tickers) == 1:
        plot_strategy_comparison(all_results, save_path=f"{args.tickers[0]}_comparison.png")


def cmd_scan(args):
    """Quick multi-stock indicator scan."""
    data = fetch_multiple(args.tickers, period=args.period)

    print(f"\n{'='*100}")
    print(f"  Market Scanner — Quick Indicator Readings")
    print(f"{'='*100}")
    print(f"  {'Ticker':<8} {'Close':>10} {'SMA20':>10} {'SMA50':>10} {'RSI':>8} {'MACD Hist':>12} {'BB %':>8} {'ATR':>8} {'Signal'}")
    print(f"  {'-'*8} {'-'*10} {'-'*10} {'-'*10} {'-'*8} {'-'*12} {'-'*8} {'-'*8} {'-'*10}")

    for ticker, df in data.items():
        enriched = add_all_indicators(df)
        r = enriched.iloc[-1]

        # Bollinger Band position as percentage (0=lower, 100=upper)
        bb_pct = (r["Close"] - r["BB_Lower"]) / (r["BB_Upper"] - r["BB_Lower"]) * 100 if (r["BB_Upper"] - r["BB_Lower"]) != 0 else 50

        # Simple composite signal
        score = 0
        if r["Close"] > r["SMA_50"]:
            score += 1
        if r["RSI_14"] < 30:
            score += 1
        elif r["RSI_14"] > 70:
            score -= 1
        if r["MACD_Histogram"] > 0:
            score += 1
        else:
            score -= 1

        signal = "BULLISH" if score >= 2 else "BEARISH" if score <= -1 else "NEUTRAL"

        print(f"  {ticker:<8} ${r['Close']:>9.2f} ${r['SMA_20']:>9.2f} ${r['SMA_50']:>9.2f} {r['RSI_14']:>7.1f} {r['MACD_Histogram']:>11.4f} {bb_pct:>7.1f}% ${r['ATR_14']:>7.2f} {signal}")

    print(f"{'='*100}\n")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Stock Market Analysis & Backtesting Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # -- analyze -----------------------------------------------------------
    p = subparsers.add_parser("analyze", help="Technical analysis for a single stock")
    p.add_argument("ticker", help="Stock ticker symbol (e.g. AAPL)")
    p.add_argument("--period", default="1y", help="Data period (default: 1y)")
    p.add_argument("--no-chart", action="store_true", help="Skip chart generation")

    # -- backtest ----------------------------------------------------------
    p = subparsers.add_parser("backtest", help="Backtest a strategy on a stock")
    p.add_argument("ticker", help="Stock ticker symbol")
    p.add_argument("--strategy", "-s", default="sma", choices=STRATEGY_MAP.keys(),
                   help="Strategy to test (default: sma)")
    p.add_argument("--period", default="2y", help="Data period (default: 2y)")
    p.add_argument("--cash", type=float, default=10_000, help="Starting capital (default: 10000)")
    p.add_argument("--commission", type=float, default=0, help="Commission per trade in $ (default: 0)")
    p.add_argument("--no-chart", action="store_true", help="Skip chart generation")

    # -- compare -----------------------------------------------------------
    p = subparsers.add_parser("compare", help="Compare all strategies on one or more tickers")
    p.add_argument("tickers", nargs="+", help="One or more ticker symbols")
    p.add_argument("--period", default="2y", help="Data period (default: 2y)")
    p.add_argument("--cash", type=float, default=10_000, help="Starting capital (default: 10000)")
    p.add_argument("--commission", type=float, default=0, help="Commission per trade in $ (default: 0)")
    p.add_argument("--no-chart", action="store_true", help="Skip chart generation")

    # -- scan --------------------------------------------------------------
    p = subparsers.add_parser("scan", help="Quick indicator scan across multiple tickers")
    p.add_argument("tickers", nargs="+", help="Ticker symbols to scan")
    p.add_argument("--period", default="1y", help="Data period (default: 1y)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    commands = {
        "analyze": cmd_analyze,
        "backtest": cmd_backtest,
        "compare": cmd_compare,
        "scan": cmd_scan,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
