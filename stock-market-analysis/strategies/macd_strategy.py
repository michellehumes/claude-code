"""MACD Strategy.

Buy when MACD line crosses above the signal line.
Sell when MACD line crosses below the signal line.
"""

import pandas as pd
from stockanalysis.backtester import Strategy, Signal
from stockanalysis.indicators import macd


class MACDStrategy(Strategy):
    name = "MACD Crossover"

    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9):
        self.fast = fast
        self.slow = slow
        self.signal = signal

    def init(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        macd_df = macd(df, self.fast, self.slow, self.signal)
        df["MACD_Line"] = macd_df["MACD"]
        df["MACD_Signal"] = macd_df["Signal"]
        df["MACD_Hist"] = macd_df["Histogram"]
        return df

    def generate_signal(self, row: pd.Series, i: int, df: pd.DataFrame) -> Signal:
        if i < 1:
            return Signal.HOLD

        curr_hist = row["MACD_Hist"]
        prev_hist = df.iloc[i - 1]["MACD_Hist"]

        if pd.isna(curr_hist) or pd.isna(prev_hist):
            return Signal.HOLD

        # Histogram crosses zero upward -> buy
        if prev_hist <= 0 and curr_hist > 0:
            return Signal.BUY
        # Histogram crosses zero downward -> sell
        if prev_hist >= 0 and curr_hist < 0:
            return Signal.SELL

        return Signal.HOLD
