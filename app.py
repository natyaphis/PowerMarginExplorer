import os
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".matplotlib"))

from src.analysis import compute_returns, lag_correlation, rolling_correlation
from src.data_loader import load_merged_data
from src.visualization import (
    plot_lag_correlation,
    plot_price_series,
    plot_rolling_correlation,
)

COMPANIES = {
    "Huaneng (600011)": "stock_600011",
    "Huadian (600027)": "stock_600027",
    "GD Power (600795)": "stock_600795",
}

st.set_page_config(page_title="China Power Margin Explorer", layout="wide")


def build_insights(rolling_df: pd.DataFrame, lag_df: pd.DataFrame) -> list[str]:
    average_corr = rolling_df["rolling_correlation"].dropna().mean()
    valid_lags = lag_df.dropna(subset=["correlation"]).copy()
    strongest_row = valid_lags.loc[valid_lags["correlation"].abs().idxmax()] if not valid_lags.empty else None

    strongest_lag = "N/A"
    strongest_value = pd.NA
    if strongest_row is not None:
        strongest_lag = int(strongest_row["lag_days"])
        strongest_value = strongest_row["correlation"]

    if pd.isna(average_corr):
        direction = "insufficient data to determine the relationship direction."
    elif average_corr > 0:
        direction = "coal and the selected stock have generally moved in the same direction."
    elif average_corr < 0:
        direction = "coal and the selected stock have generally moved in opposite directions."
    else:
        direction = "coal and the selected stock have shown little directional relationship."

    average_text = "Average rolling correlation is unavailable."
    if not pd.isna(average_corr):
        average_text = f"Average 30-day rolling correlation is {average_corr:.2f}."

    strongest_text = "Strongest lag relationship is unavailable."
    if not pd.isna(strongest_value):
        strongest_text = f"Strongest lag is {strongest_lag} days with correlation {strongest_value:.2f}."

    return [
        average_text,
        strongest_text,
        f"Overall, {direction}",
    ]


def normalize_date_range(date_range, default_start, default_end):
    if isinstance(date_range, tuple) and len(date_range) == 2:
        return date_range
    if isinstance(date_range, list) and len(date_range) == 2:
        return date_range[0], date_range[1]
    return default_start, default_end


data = compute_returns(load_merged_data())

st.sidebar.header("Controls")
company_label = st.sidebar.selectbox("Company", list(COMPANIES.keys()))
stock_col = COMPANIES[company_label]

date_min = data["date"].min().date()
date_max = data["date"].max().date()
date_range = st.sidebar.date_input("Date Range", value=(date_min, date_max), min_value=date_min, max_value=date_max)
start_date, end_date = normalize_date_range(date_range, date_min, date_max)

filtered = data[(data["date"].dt.date >= start_date) & (data["date"].dt.date <= end_date)].copy()
rolling_df = rolling_correlation(filtered, stock_col)
lag_df = lag_correlation(filtered, stock_col)
insights = build_insights(rolling_df, lag_df)

st.title("China Power Margin Explorer")

st.subheader("Price Comparison")
st.pyplot(plot_price_series(filtered, stock_col, company_label), width="stretch")

st.subheader("Rolling Correlation")
if rolling_df["rolling_correlation"].dropna().empty:
    st.info("At least 30 trading-day return observations are needed to display the rolling correlation.")
else:
    st.pyplot(plot_rolling_correlation(rolling_df), width="stretch")

st.subheader("Lag Sensitivity")
if lag_df["correlation"].dropna().empty:
    st.info("Not enough overlapping return observations to calculate lag correlations.")
else:
    st.pyplot(plot_lag_correlation(lag_df), width="stretch")

st.subheader("Key Insights")
for insight in insights:
    st.markdown(f"- {insight}")
