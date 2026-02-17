# Market Predict Agent

A beginner-friendly AI/ML demo app that downloads daily stock data from Alpaca, computes technical indicators, trains a Random Forest model, and visualizes predictions. **Educational purposes only — not financial advice.**

<img width="787" height="836" alt="Screenshot 2026-02-15 at 5 50 10 PM" src="https://github.com/user-attachments/assets/785d93ea-9ae3-414a-85ce-4150d535beba" />


## Setup

1. **Create a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Alpaca API keys**:

   - Copy `.env.example` to `.env`
   - Add your Alpaca API key and secret (get them at [alpaca.markets](https://alpaca.markets))

   ```bash
   cp .env.example .env
   # Edit .env and set ALPACA_API_KEY and ALPACA_API_SECRET
   ```

   Or export them in your shell:

   ```bash
   export ALPACA_API_KEY=your_key
   export ALPACA_API_SECRET=your_secret
   ```

## Run the Streamlit App

```bash
streamlit run app.py
```

Open the URL shown in the terminal (typically http://localhost:8501). Use the sidebar to pick a ticker and date range, then click **Run**.

## Run the CLI

```bash
python run_predict.py --ticker NVDA --start 2022-01-01 --end 2026-02-15
```

Output is JSON printed to stdout, suitable for use by OpenClaw or other tools:

```json
{
  "ticker": "NVDA",
  "start": "2022-01-01",
  "end": "2026-02-15",
  "n_train": 400,
  "n_test": 100,
  "mae_model": 0.012,
  "mae_baseline": 0.015,
  "pred_next_return": 0.008,
  "as_of_date": "2026-02-14"
}
```

## Limitations / Disclaimer

- **Educational demo only.** This app is for learning about ML and technical indicators. Do not use it to make investment decisions.
- Past performance does not guarantee future results.
- The model uses simple features and a basic Random Forest; it is not suitable for real trading.
- Alpaca free-tier data may have limitations; check [Alpaca's data docs](https://docs.alpaca.markets/docs/market-data) for details.
