"""SMA Crossover Strategy.

Buy when a fast SMA crosses above a slow SMA (golden cross).
Sell when the fast SMA crosses below the slow SMA (death cross).
"""

import pandas as pd
from stockanalysis.backtester import Strategy, Signal
from stockanalysis.indicators import sma


class SMACrossoverStrategy(Strategy):
    name = "SMA Crossover"

    def __init__(self, fast_period: int = 20, slow_period: int = 50):
        self.fast_period = fast_period
        self.slow_period = slow_period

    def init(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["SMA_Fast"] = sma(df, self.fast_period)
        df["SMA_Slow"] = sma(df, self.slow_period)
        return df

    def generate_signal(self, row: pd.Series, i: int, df: pd.DataFrame) -> Signal:
        if i < 1:
            return Signal.HOLD

        curr_fast, curr_slow = row["SMA_Fast"], row["SMA_Slow"]
        prev_fast = df.iloc[i - 1]["SMA_Fast"]
        prev_slow = df.iloc[i - 1]["SMA_Slow"]

        if pd.isna(curr_fast) or pd.isna(curr_slow) or pd.isna(prev_fast) or pd.isna(prev_slow):
            return Signal.HOLD

        # Golden cross
        if prev_fast <= prev_slow and curr_fast > curr_slow:
            return Signal.BUY
        # Death cross
        if prev_fast >= prev_slow and curr_fast < curr_slow:
            return Signal.SELL

        return Signal.HOLD
