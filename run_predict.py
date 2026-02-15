#!/usr/bin/env python3
"""
CLI runner for the Market Predict Agent.
Can be invoked by OpenClaw as a "skill command".

Usage:
    python run_predict.py --ticker NVDA --start 2022-01-01 --end 2026-02-15
"""

import argparse
import json
import os
import sys

# Load .env from the directory containing this script (project root)
try:
    from pathlib import Path
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

from ml_core import (
    MIN_ROWS,
    build_dataset,
    fetch_alpaca_bars,
    get_latest_features_and_prediction,
    train_and_evaluate,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Predict next-day stock return using technical indicators and Random Forest."
    )
    parser.add_argument("--ticker", required=True, help="Stock ticker symbol (e.g., NVDA)")
    parser.add_argument("--start", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", required=True, help="End date (YYYY-MM-DD)")
    args = parser.parse_args()

    ticker = args.ticker.strip().upper()
    start = args.start.strip()
    end = args.end.strip()

    # Check API keys
    if not os.environ.get("ALPACA_API_KEY") or not os.environ.get("ALPACA_API_SECRET"):
        print("Error: Set ALPACA_API_KEY and ALPACA_API_SECRET in your environment.", file=sys.stderr)
        return 1

    # Fetch data
    try:
        df = fetch_alpaca_bars(ticker, start, end)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    if df is None or df.empty:
        print(
            "Error: Could not fetch data. Check dates, ticker, and API keys.",
            file=sys.stderr,
        )
        return 1

    try:
        X, y, dates = build_dataset(df)
    except Exception as e:
        print(f"Error building dataset: {e}", file=sys.stderr)
        return 1

    if len(X) < MIN_ROWS:
        print(
            f"Error: Need at least {MIN_ROWS} rows. Got {len(X)}. Try a longer date range.",
            file=sys.stderr,
        )
        return 1

    result = train_and_evaluate(X, y, dates)
    latest = get_latest_features_and_prediction(
        result["model"], result["X"], result["dates"]
    )

    output = {
        "ticker": ticker,
        "start": start,
        "end": end,
        "n_train": result["n_train"],
        "n_test": result["n_test"],
        "mae_model": result["mae_model"],
        "mae_baseline": result["mae_baseline"],
        "pred_next_return": latest["pred_next_return"],
        "as_of_date": latest["as_of_date"],
    }

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
