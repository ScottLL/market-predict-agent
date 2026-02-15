You are building a beginner-friendly AI/ML demo app (educational, not financial advice).
Goal: a small running finance app that downloads daily stock data from Alpaca, computes simple technical-indicator features, trains a RandomForest model, evaluates MAE, and visualizes predictions. Also include a small CLI script that can be invoked by OpenClaw as a “skill command”.

Please create a complete Python project with these files:

1) app.py (Streamlit UI)
2) run_predict.py (CLI runner for OpenClaw / terminal use)
3) ml_core.py (shared feature + training code)
4) requirements.txt
5) .env.example
6) README.md

Constraints / style:

- Keep it simple for college students with zero AI background.
- Time-series safe split: do NOT shuffle. Use first 80% for train, last 20% for test.
- Add a visible banner: “Educational demo — not financial advice.”
- Handle missing API keys and insufficient data gracefully with clear messages.
- Prefer clarity over cleverness. Include comments.

Data source:

- Use Alpaca Market Data via alpaca-py.
- Read API keys from environment variables: ALPACA_API_KEY, ALPACA_API_SECRET.
- Use Alpaca’s data client (StockHistoricalDataClient) and request daily bars.
- Allow user to pick start date, end date, ticker.

Features (computed from daily bars):

- close_return: close.pct_change()
- vol_14: rolling std of close_return over 14 days
- sma_10: rolling mean of close over 10 days
- sma_30: rolling mean of close over 30 days
- rsi_14: 14-day RSI (implement manually; no TA-Lib required)
- volume_change: volume.pct_change()
- range_pct: (high - low) / close

Target:

- Predict next-day return: target = close_return.shift(-1)

Model:

- RandomForestRegressor with sensible defaults (e.g., n_estimators=300, random_state=42)
- Also compute a naive baseline: predict next-day return = 0 (or today’s return) and report its MAE for comparison.

Outputs in the Streamlit app:

- MAE on test set for model and baseline
- Predicted next-day return for the latest available day
- A line chart (matplotlib) showing actual vs predicted returns on the test set
- A “Feature snapshot” table for the latest row (RSI, SMA10/30, vol14, etc.)
- A short plain-English explanation of each feature and what MAE means (keep it short).

CLI script (run_predict.py):

- Usage: python run_predict.py --ticker NVDA --start 2022-01-01 --end 2026-02-15
- Prints JSON to stdout with keys:
  {
  "ticker": "...",
  "start": "...",
  "end": "...",
  "n_train": int,
  "n_test": int,
  "mae_model": float,
  "mae_baseline": float,
  "pred_next_return": float,
  "as_of_date": "YYYY-MM-DD"
  }
- Exit code nonzero on errors, with a clear error message.

Implementation details:

- Put feature engineering + dataset creation in ml_core.py so app.py and run_predict.py share it.
- Ensure there is no look-ahead leakage:
  - Features at day t must only use data up to day t.
  - Target is day t+1 return.
  - When predicting “next day”, use the latest day’s features only.
- Drop rows with NaNs created by rolling windows and shifts.

README.md must include:

- Setup steps (pip install, .env, Alpaca keys)
- How to run Streamlit
- How to run CLI
- Notes about limitations / not financial advice

After generating the files, briefly explain how to run the app locally.
