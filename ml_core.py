"""
Shared ML logic for the Market Predict Agent.
Handles Alpaca data fetching, feature engineering, and model training.
"""

import os
from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Feature columns used for training (excludes target)
FEATURE_COLUMNS = [
    "close_return",
    "vol_14",
    "sma_10",
    "sma_30",
    "rsi_14",
    "volume_change",
    "range_pct",
]

MIN_ROWS = 50  # Minimum rows after dropna for training


def fetch_alpaca_bars(
    ticker: str,
    start: str,
    end: str,
) -> Optional[pd.DataFrame]:
    """
    Fetch daily OHLCV bars from Alpaca Market Data API.

    Args:
        ticker: Stock symbol (e.g., "NVDA")
        start: Start date as "YYYY-MM-DD"
        end: End date as "YYYY-MM-DD"

    Returns:
        DataFrame with columns: open, high, low, close, volume, timestamp (as date index).
        Returns None if API keys are missing or fetch fails.
    """
    api_key = os.environ.get("ALPACA_API_KEY")
    api_secret = os.environ.get("ALPACA_API_SECRET")

    if not api_key or not api_secret:
        return None

    try:
        from alpaca.data.historical import StockHistoricalDataClient
        from alpaca.data.requests import StockBarsRequest
        from alpaca.data.timeframe import TimeFrame

        client = StockHistoricalDataClient(api_key=api_key, secret_key=api_secret)

        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")

        request = StockBarsRequest(
            symbol_or_symbols=ticker,
            start=start_dt,
            end=end_dt,
            timeframe=TimeFrame.Day,
        )

        bars = client.get_stock_bars(request_params=request)

        if not bars or not bars.data:
            raise ValueError("Alpaca returned no bar data.")

        # Use BarSet.df for robust DataFrame conversion (handles multi-index)
        df = bars.df
        if df.empty:
            raise ValueError(f"Alpaca returned no data for ticker {ticker}.")

        # Flatten multi-index: symbol, timestamp -> columns
        df = df.reset_index()
        if "symbol" in df.columns:
            df = df[df["symbol"] == ticker]
        df["date"] = pd.to_datetime(df["timestamp"]).dt.tz_localize(None).dt.date
        df = df.set_index("date")[["open", "high", "low", "close", "volume"]].sort_index()

        return df

    except Exception as e:
        raise RuntimeError(f"Alpaca API error: {e}") from e


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute technical indicator features from OHLCV data.
    All features at day t use only data up to day t (no look-ahead).
    """
    out = df.copy()

    # Daily return (close-to-close)
    out["close_return"] = out["close"].pct_change()

    # 14-day rolling volatility of returns
    out["vol_14"] = out["close_return"].rolling(14).std()

    # Simple moving averages
    out["sma_10"] = out["close"].rolling(10).mean()
    out["sma_30"] = out["close"].rolling(30).mean()

    # RSI (14-day, manual implementation)
    delta = out["close"].diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    out["rsi_14"] = 100 - (100 / (1 + rs))
    # When avg_loss is 0, rs is inf -> RSI = 100
    out["rsi_14"] = out["rsi_14"].fillna(100)

    # Volume change
    out["volume_change"] = out["volume"].pct_change()

    # Daily range as % of close
    out["range_pct"] = (out["high"] - out["low"]) / out["close"]

    # Target: next-day return (what we want to predict)
    out["target"] = out["close_return"].shift(-1)

    return out


def build_dataset(df: pd.DataFrame):
    """
    Build feature matrix X, target vector y, and date index.
    Drops rows with NaN from rolling windows and shifts.
    """
    df_feat = compute_features(df)
    df_clean = df_feat.dropna()

    X = df_clean[FEATURE_COLUMNS]
    y = df_clean["target"]
    dates = df_clean.index

    return X, y, dates


def train_and_evaluate(X: pd.DataFrame, y: pd.Series, dates: pd.Index) -> dict:
    """
    Time-series split: first 80% train, last 20% test (no shuffle).
    Trains RandomForest and computes MAE for model and baseline.
    """
    n = len(X)
    split_idx = int(n * 0.8)

    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    dates_test = dates[split_idx:]

    model = RandomForestRegressor(n_estimators=300, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae_model = mean_absolute_error(y_test, y_pred)

    # Baseline: predict 0 for all (naive "no change" forecast)
    y_baseline = np.zeros_like(y_test)
    mae_baseline = mean_absolute_error(y_test, y_baseline)

    return {
        "mae_model": float(mae_model),
        "mae_baseline": float(mae_baseline),
        "model": model,
        "X_test": X_test,
        "y_test": y_test,
        "y_pred": y_pred,
        "dates_test": dates_test,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "X": X,
        "y": y,
        "dates": dates,
    }


def get_latest_features_and_prediction(model, X: pd.DataFrame, dates: pd.Index) -> dict:
    """
    Get the latest row's feature snapshot and predicted next-day return.
    """
    latest_idx = -1
    latest_features = X.iloc[latest_idx]
    pred_next_return = float(model.predict(X.iloc[[latest_idx]])[0])
    as_of_date = str(dates[latest_idx])

    return {
        "features": latest_features,
        "pred_next_return": pred_next_return,
        "as_of_date": as_of_date,
    }
