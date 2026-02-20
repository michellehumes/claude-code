"""RSI Mean-Reversion Strategy.

Buy when RSI drops below an oversold threshold.
Sell when RSI rises above an overbought threshold.
"""

import pandas as pd
from stockanalysis.backtester import Strategy, Signal
from stockanalysis.indicators import rsi


class RSIMeanReversionStrategy(Strategy):
    name = "RSI Mean Reversion"

    def __init__(self, period: int = 14, oversold: float = 30.0, overbought: float = 70.0):
        self.period = period
        self.oversold = oversold
        self.overbought = overbought

    def init(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["RSI"] = rsi(df, self.period)
        return df

    def generate_signal(self, row: pd.Series, i: int, df: pd.DataFrame) -> Signal:
        rsi_val = row["RSI"]
        if pd.isna(rsi_val):
            return Signal.HOLD

        if rsi_val < self.oversold:
            return Signal.BUY
        if rsi_val > self.overbought:
            return Signal.SELL

        return Signal.HOLD
