"""Combined Multi-Indicator Strategy.

Uses RSI + MACD + Bollinger Bands together for higher-confidence signals.
A signal only fires when at least 2 of the 3 indicators agree.
"""

import pandas as pd
from stockanalysis.backtester import Strategy, Signal
from stockanalysis.indicators import rsi, macd, bollinger_bands


class CombinedStrategy(Strategy):
    name = "Combined (RSI + MACD + BB)"

    def __init__(
        self,
        rsi_period: int = 14,
        rsi_oversold: float = 30.0,
        rsi_overbought: float = 70.0,
        bb_period: int = 20,
        bb_std: float = 2.0,
    ):
        self.rsi_period = rsi_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.bb_period = bb_period
        self.bb_std = bb_std

    def init(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["RSI"] = rsi(df, self.rsi_period)
        macd_df = macd(df)
        df["MACD_Hist"] = macd_df["Histogram"]
        bb = bollinger_bands(df, self.bb_period, self.bb_std)
        df["BB_Upper"] = bb["BB_Upper"]
        df["BB_Lower"] = bb["BB_Lower"]
        return df

    def generate_signal(self, row: pd.Series, i: int, df: pd.DataFrame) -> Signal:
        if i < 1:
            return Signal.HOLD

        rsi_val = row["RSI"]
        hist = row["MACD_Hist"]
        prev_hist = df.iloc[i - 1]["MACD_Hist"]
        close = row["Close"]
        bb_upper = row["BB_Upper"]
        bb_lower = row["BB_Lower"]

        if any(pd.isna(v) for v in [rsi_val, hist, prev_hist, bb_upper, bb_lower]):
            return Signal.HOLD

        buy_votes = 0
        sell_votes = 0

        # RSI vote
        if rsi_val < self.rsi_oversold:
            buy_votes += 1
        elif rsi_val > self.rsi_overbought:
            sell_votes += 1

        # MACD histogram vote
        if prev_hist <= 0 and hist > 0:
            buy_votes += 1
        elif prev_hist >= 0 and hist < 0:
            sell_votes += 1

        # Bollinger band vote
        if close <= bb_lower:
            buy_votes += 1
        elif close >= bb_upper:
            sell_votes += 1

        if buy_votes >= 2:
            return Signal.BUY
        if sell_votes >= 2:
            return Signal.SELL

        return Signal.HOLD
