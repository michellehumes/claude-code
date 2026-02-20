"""Technical analysis indicators.

All functions accept a pandas DataFrame with at minimum a 'Close' column
and return a new DataFrame or Series with the indicator values.
The original DataFrame is never modified in-place.
"""

import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# Trend indicators
# ---------------------------------------------------------------------------

def sma(df: pd.DataFrame, period: int = 20, column: str = "Close") -> pd.Series:
    """Simple Moving Average."""
    return df[column].rolling(window=period).mean().rename(f"SMA_{period}")


def ema(df: pd.DataFrame, period: int = 20, column: str = "Close") -> pd.Series:
    """Exponential Moving Average."""
    return df[column].ewm(span=period, adjust=False).mean().rename(f"EMA_{period}")


def wma(df: pd.DataFrame, period: int = 20, column: str = "Close") -> pd.Series:
    """Weighted Moving Average."""
    weights = np.arange(1, period + 1)
    return (
        df[column]
        .rolling(window=period)
        .apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)
        .rename(f"WMA_{period}")
    )


def macd(
    df: pd.DataFrame,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
    column: str = "Close",
) -> pd.DataFrame:
    """Moving Average Convergence Divergence.

    Returns DataFrame with columns: MACD, Signal, Histogram.
    """
    ema_fast = df[column].ewm(span=fast, adjust=False).mean()
    ema_slow = df[column].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return pd.DataFrame({
        "MACD": macd_line,
        "Signal": signal_line,
        "Histogram": histogram,
    }, index=df.index)


# ---------------------------------------------------------------------------
# Momentum indicators
# ---------------------------------------------------------------------------

def rsi(df: pd.DataFrame, period: int = 14, column: str = "Close") -> pd.Series:
    """Relative Strength Index (Wilder's smoothing)."""
    delta = df[column].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    return (100 - 100 / (1 + rs)).rename(f"RSI_{period}")


def stochastic(
    df: pd.DataFrame,
    k_period: int = 14,
    d_period: int = 3,
) -> pd.DataFrame:
    """Stochastic Oscillator (%K and %D).

    Requires High, Low, Close columns.
    """
    low_min = df["Low"].rolling(window=k_period).min()
    high_max = df["High"].rolling(window=k_period).max()
    k = 100 * (df["Close"] - low_min) / (high_max - low_min)
    d = k.rolling(window=d_period).mean()
    return pd.DataFrame({f"Stoch_K_{k_period}": k, f"Stoch_D_{d_period}": d}, index=df.index)


def williams_r(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Williams %R."""
    high_max = df["High"].rolling(window=period).max()
    low_min = df["Low"].rolling(window=period).min()
    return (
        -100 * (high_max - df["Close"]) / (high_max - low_min)
    ).rename(f"Williams_R_{period}")


def roc(df: pd.DataFrame, period: int = 12, column: str = "Close") -> pd.Series:
    """Rate of Change (%)."""
    return (
        df[column].pct_change(periods=period) * 100
    ).rename(f"ROC_{period}")


# ---------------------------------------------------------------------------
# Volatility indicators
# ---------------------------------------------------------------------------

def bollinger_bands(
    df: pd.DataFrame,
    period: int = 20,
    std_dev: float = 2.0,
    column: str = "Close",
) -> pd.DataFrame:
    """Bollinger Bands (upper, middle, lower)."""
    middle = df[column].rolling(window=period).mean()
    std = df[column].rolling(window=period).std()
    return pd.DataFrame({
        "BB_Upper": middle + std_dev * std,
        "BB_Middle": middle,
        "BB_Lower": middle - std_dev * std,
    }, index=df.index)


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range. Requires High, Low, Close columns."""
    high_low = df["High"] - df["Low"]
    high_close = (df["High"] - df["Close"].shift()).abs()
    low_close = (df["Low"] - df["Close"].shift()).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return true_range.ewm(alpha=1 / period, min_periods=period, adjust=False).mean().rename(f"ATR_{period}")


def keltner_channels(
    df: pd.DataFrame,
    ema_period: int = 20,
    atr_period: int = 14,
    multiplier: float = 2.0,
) -> pd.DataFrame:
    """Keltner Channels (upper, middle, lower)."""
    middle = df["Close"].ewm(span=ema_period, adjust=False).mean()
    atr_val = atr(df, period=atr_period)
    return pd.DataFrame({
        "KC_Upper": middle + multiplier * atr_val,
        "KC_Middle": middle,
        "KC_Lower": middle - multiplier * atr_val,
    }, index=df.index)


# ---------------------------------------------------------------------------
# Volume indicators
# ---------------------------------------------------------------------------

def vwap(df: pd.DataFrame) -> pd.Series:
    """Volume-Weighted Average Price (cumulative intraday).

    Requires High, Low, Close, Volume columns.
    """
    typical_price = (df["High"] + df["Low"] + df["Close"]) / 3
    cumulative_tp_vol = (typical_price * df["Volume"]).cumsum()
    cumulative_vol = df["Volume"].cumsum()
    return (cumulative_tp_vol / cumulative_vol).rename("VWAP")


def obv(df: pd.DataFrame) -> pd.Series:
    """On-Balance Volume."""
    sign = np.sign(df["Close"].diff()).fillna(0)
    return (sign * df["Volume"]).cumsum().rename("OBV")


def mfi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Money Flow Index. Requires High, Low, Close, Volume."""
    typical_price = (df["High"] + df["Low"] + df["Close"]) / 3
    money_flow = typical_price * df["Volume"]
    delta = typical_price.diff()
    positive_flow = money_flow.where(delta > 0, 0).rolling(window=period).sum()
    negative_flow = money_flow.where(delta < 0, 0).rolling(window=period).sum()
    mfi_ratio = positive_flow / negative_flow
    return (100 - 100 / (1 + mfi_ratio)).rename(f"MFI_{period}")


# ---------------------------------------------------------------------------
# Convenience: add all indicators to a DataFrame
# ---------------------------------------------------------------------------

def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with common indicators added as columns."""
    out = df.copy()

    # Trend
    out["SMA_20"] = sma(df, 20)
    out["SMA_50"] = sma(df, 50)
    out["EMA_12"] = ema(df, 12)
    out["EMA_26"] = ema(df, 26)
    macd_df = macd(df)
    out["MACD"] = macd_df["MACD"]
    out["MACD_Signal"] = macd_df["Signal"]
    out["MACD_Histogram"] = macd_df["Histogram"]

    # Momentum
    out["RSI_14"] = rsi(df)
    stoch = stochastic(df)
    out["Stoch_K"] = stoch.iloc[:, 0]
    out["Stoch_D"] = stoch.iloc[:, 1]

    # Volatility
    bb = bollinger_bands(df)
    out["BB_Upper"] = bb["BB_Upper"]
    out["BB_Middle"] = bb["BB_Middle"]
    out["BB_Lower"] = bb["BB_Lower"]
    out["ATR_14"] = atr(df)

    # Volume
    out["VWAP"] = vwap(df)
    out["OBV"] = obv(df)

    return out
