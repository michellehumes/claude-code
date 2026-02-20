"""Data fetching module using yfinance."""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def fetch_stock_data(
    ticker: str,
    period: str = "1y",
    interval: str = "1d",
    start: str | None = None,
    end: str | None = None,
) -> pd.DataFrame:
    """Fetch historical stock data from Yahoo Finance.

    Args:
        ticker: Stock ticker symbol (e.g. 'AAPL', 'MSFT').
        period: Data period - 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max.
        interval: Data interval - 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo.
        start: Start date string (YYYY-MM-DD). Overrides period if provided.
        end: End date string (YYYY-MM-DD). Defaults to today.

    Returns:
        DataFrame with columns: Open, High, Low, Close, Volume, plus Adj Close if available.
    """
    stock = yf.Ticker(ticker)

    if start:
        df = stock.history(start=start, end=end or datetime.now().strftime("%Y-%m-%d"), interval=interval)
    else:
        df = stock.history(period=period, interval=interval)

    if df.empty:
        raise ValueError(f"No data returned for ticker '{ticker}'. Check the symbol and date range.")

    # Normalize column names
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    return df


def fetch_multiple(tickers: list[str], **kwargs) -> dict[str, pd.DataFrame]:
    """Fetch data for multiple tickers.

    Returns:
        Dict mapping ticker symbol to its DataFrame.
    """
    results = {}
    for t in tickers:
        try:
            results[t] = fetch_stock_data(t, **kwargs)
        except ValueError as e:
            print(f"Warning: {e}")
    return results


def get_stock_info(ticker: str) -> dict:
    """Return company info dict for a ticker."""
    return dict(yf.Ticker(ticker).info)
