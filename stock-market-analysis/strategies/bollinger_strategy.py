"""Bollinger Band Strategy.

Buy when price touches or drops below the lower band (oversold bounce).
Sell when price touches or rises above the upper band (overbought reversal).
"""

import pandas as pd
from stockanalysis.backtester import Strategy, Signal
from stockanalysis.indicators import bollinger_bands


class BollingerBandStrategy(Strategy):
    name = "Bollinger Band Bounce"

    def __init__(self, period: int = 20, std_dev: float = 2.0):
        self.period = period
        self.std_dev = std_dev

    def init(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        bb = bollinger_bands(df, self.period, self.std_dev)
        df["BB_Upper"] = bb["BB_Upper"]
        df["BB_Lower"] = bb["BB_Lower"]
        df["BB_Middle"] = bb["BB_Middle"]
        return df

    def generate_signal(self, row: pd.Series, i: int, df: pd.DataFrame) -> Signal:
        close = row["Close"]
        upper = row["BB_Upper"]
        lower = row["BB_Lower"]

        if pd.isna(upper) or pd.isna(lower):
            return Signal.HOLD

        if close <= lower:
            return Signal.BUY
        if close >= upper:
            return Signal.SELL

        return Signal.HOLD
