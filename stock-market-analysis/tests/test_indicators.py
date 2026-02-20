"""Unit tests for technical indicators."""

import numpy as np
import pandas as pd
import pytest

from stockanalysis.indicators import (
    sma, ema, wma, macd, rsi, stochastic, williams_r, roc,
    bollinger_bands, atr, keltner_channels, vwap, obv, mfi,
    add_all_indicators,
)


@pytest.fixture
def sample_df():
    """Create a simple DataFrame with realistic-ish OHLCV data."""
    np.random.seed(42)
    n = 100
    close = 100 + np.cumsum(np.random.randn(n) * 0.5)
    high = close + np.abs(np.random.randn(n) * 0.3)
    low = close - np.abs(np.random.randn(n) * 0.3)
    open_ = close + np.random.randn(n) * 0.2
    volume = np.random.randint(100_000, 1_000_000, n).astype(float)
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    return pd.DataFrame({
        "Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume,
    }, index=dates)


class TestSMA:
    def test_length(self, sample_df):
        result = sma(sample_df, 20)
        assert len(result) == len(sample_df)

    def test_nan_for_early_rows(self, sample_df):
        result = sma(sample_df, 20)
        assert result.iloc[:19].isna().all()
        assert result.iloc[19:].notna().all()

    def test_known_value(self):
        df = pd.DataFrame({"Close": [1.0, 2.0, 3.0, 4.0, 5.0]})
        result = sma(df, 3)
        assert result.iloc[2] == pytest.approx(2.0)
        assert result.iloc[4] == pytest.approx(4.0)


class TestEMA:
    def test_length(self, sample_df):
        result = ema(sample_df, 12)
        assert len(result) == len(sample_df)

    def test_no_nan_after_start(self, sample_df):
        result = ema(sample_df, 12)
        assert result.iloc[-1] is not None and not np.isnan(result.iloc[-1])


class TestMACD:
    def test_columns(self, sample_df):
        result = macd(sample_df)
        assert list(result.columns) == ["MACD", "Signal", "Histogram"]
        assert len(result) == len(sample_df)


class TestRSI:
    def test_range(self, sample_df):
        result = rsi(sample_df, 14)
        valid = result.dropna()
        assert (valid >= 0).all() and (valid <= 100).all()


class TestStochastic:
    def test_columns(self, sample_df):
        result = stochastic(sample_df)
        assert len(result.columns) == 2
        assert len(result) == len(sample_df)


class TestBollingerBands:
    def test_bands_ordering(self, sample_df):
        result = bollinger_bands(sample_df)
        valid = result.dropna()
        assert (valid["BB_Upper"] >= valid["BB_Middle"]).all()
        assert (valid["BB_Middle"] >= valid["BB_Lower"]).all()


class TestATR:
    def test_positive(self, sample_df):
        result = atr(sample_df, 14)
        valid = result.dropna()
        assert (valid > 0).all()


class TestVWAP:
    def test_length(self, sample_df):
        result = vwap(sample_df)
        assert len(result) == len(sample_df)


class TestOBV:
    def test_length(self, sample_df):
        result = obv(sample_df)
        assert len(result) == len(sample_df)


class TestAddAllIndicators:
    def test_adds_columns(self, sample_df):
        result = add_all_indicators(sample_df)
        expected_cols = ["SMA_20", "SMA_50", "EMA_12", "EMA_26", "MACD", "RSI_14",
                         "BB_Upper", "BB_Middle", "BB_Lower", "ATR_14", "VWAP", "OBV"]
        for col in expected_cols:
            assert col in result.columns, f"Missing column: {col}"

    def test_original_not_modified(self, sample_df):
        original_cols = list(sample_df.columns)
        add_all_indicators(sample_df)
        assert list(sample_df.columns) == original_cols
