"""
Streamlit UI for the Market Predict Agent.
Educational demo — not financial advice.
"""

import os

# Load .env from the directory containing this script (project root)
try:
    from pathlib import Path
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass
from datetime import date, timedelta

import matplotlib.pyplot as plt
import streamlit as st

from ml_core import (
    FEATURE_COLUMNS,
    MIN_ROWS,
    build_dataset,
    fetch_alpaca_bars,
    get_latest_features_and_prediction,
    train_and_evaluate,
)

st.set_page_config(page_title="Market Predict Agent", page_icon="📈")

# Educational banner
st.warning(
    "**Educational demo — not financial advice.** This app is for learning "
    "purposes only. Do not use it to make investment decisions."
)

st.title("Market Predict Agent")
st.caption("Predict next-day stock returns using technical indicators and a Random Forest model.")

# Sidebar inputs
with st.sidebar:
    st.header("Parameters")
    ticker = st.text_input("Ticker symbol", value="NVDA", max_chars=10).strip().upper()
    end_default = date.today()
    start_default = end_default - timedelta(days=365 * 4)  # ~4 years
    start_date = st.date_input("Start date", value=start_default)
    end_date = st.date_input("End date", value=end_default)
    run_btn = st.button("Run")

if run_btn:
    # Check API keys
    if not os.environ.get("ALPACA_API_KEY") or not os.environ.get("ALPACA_API_SECRET"):
        st.error(
            "Missing API keys. Set ALPACA_API_KEY and ALPACA_API_SECRET in your environment "
            "(e.g., in a .env file). See .env.example for the format."
        )
        st.stop()

    if not ticker:
        st.error("Please enter a ticker symbol.")
        st.stop()

    if start_date >= end_date:
        st.error("Start date must be before end date.")
        st.stop()

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    with st.spinner("Fetching data from Alpaca..."):
        try:
            df = fetch_alpaca_bars(ticker, start_str, end_str)
        except RuntimeError as e:
            st.error(f"Could not fetch data: {e}")
            st.stop()
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            st.stop()

    if df is None or df.empty:
        st.error(
            "Could not fetch data. Check your API keys, dates, and ticker symbol. "
            "Ensure the ticker is valid and the date range contains trading days."
        )
        st.stop()

    try:
        X, y, dates = build_dataset(df)
    except Exception as e:
        st.error(f"Error building dataset: {e}")
        st.stop()

    if len(X) < MIN_ROWS:
        st.error(
            f"Need at least {MIN_ROWS} rows after computing features. "
            f"Got {len(X)}. Try a longer date range."
        )
        st.stop()

    with st.spinner("Training model..."):
        result = train_and_evaluate(X, y, dates)

    latest = get_latest_features_and_prediction(
        result["model"], result["X"], result["dates"]
    )

    # Display results
    st.subheader("Results")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("MAE (Model)", f"{result['mae_model']:.6f}")
    with col2:
        st.metric("MAE (Baseline)", f"{result['mae_baseline']:.6f}")
    with col3:
        st.metric("Predicted next-day return", f"{latest['pred_next_return']:.6f}")

    st.caption(f"As of date: {latest['as_of_date']} | Train: {result['n_train']} | Test: {result['n_test']}")

    # Line chart: actual vs predicted returns on test set
    st.subheader("Actual vs Predicted Returns (Test Set)")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(
        result["dates_test"],
        result["y_test"].values,
        label="Actual",
        color="blue",
        alpha=0.8,
    )
    ax.plot(
        result["dates_test"],
        result["y_pred"],
        label="Predicted",
        color="orange",
        alpha=0.8,
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Return")
    ax.set_title(f"{ticker} — Test Set")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Feature snapshot table
    st.subheader("Feature Snapshot (Latest Day)")
    feat_df = latest["features"].to_frame(name="Value")
    feat_df.index.name = "Feature"
    st.dataframe(feat_df, use_container_width=True)

    # Plain-English explanations
    with st.expander("What do these features and metrics mean?"):
        st.markdown("""
        **Features:**
        - **close_return**: Today's percentage change in closing price vs yesterday.
        - **vol_14**: 14-day rolling standard deviation of daily returns (volatility).
        - **sma_10 / sma_30**: 10-day and 30-day simple moving averages of the closing price.
        - **rsi_14**: Relative Strength Index (0–100). Values >70 suggest overbought; <30 oversold.
        - **volume_change**: Today's volume change vs yesterday (as a percentage).
        - **range_pct**: (High - Low) / Close — how wide the day's price range was.

        **MAE (Mean Absolute Error):** The average absolute difference between predicted and actual returns.
        Lower is better. The baseline predicts "no change" (0) for every day; if the model's MAE is
        lower than the baseline's, it may be capturing some signal (though past performance does not
        guarantee future results).
        """)

else:
    st.info("Use the sidebar to pick a ticker and date range, then click **Run**.")
