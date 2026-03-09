import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".matplotlib"))

import matplotlib.pyplot as plt
import pandas as pd


def plot_price_series(df: pd.DataFrame, stock_col: str, stock_label: str):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()

    price_data = df[["date", "coal_price", stock_col]].dropna(how="all", subset=["coal_price", stock_col])
    ax1.plot(price_data["date"], price_data[stock_col], color="tab:blue", linewidth=2, label=stock_label)
    ax2.plot(price_data["date"], price_data["coal_price"], color="tab:red", linewidth=2, label="Coal Price")

    ax1.set_title("Price Comparison")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Stock Price", color="tab:blue")
    ax2.set_ylabel("Coal Price", color="tab:red")
    ax1.tick_params(axis="y", labelcolor="tab:blue")
    ax2.tick_params(axis="y", labelcolor="tab:red")
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


def plot_rolling_correlation(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["rolling_correlation"], color="tab:green", linewidth=2)
    ax.axhline(0, color="black", linewidth=1, linestyle="--")
    ax.set_title("30-Day Rolling Correlation")
    ax.set_xlabel("Date")
    ax.set_ylabel("Correlation")
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


def plot_lag_correlation(df: pd.DataFrame):
    plot_data = df.copy()
    plot_data["correlation"] = pd.to_numeric(plot_data["correlation"], errors="coerce")
    plot_data = plot_data.dropna(subset=["correlation"])

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(plot_data["lag_days"].astype(str), plot_data["correlation"], color="tab:orange", width=0.6)
    ax.axhline(0, color="black", linewidth=1, linestyle="--")
    ax.set_title("Lag Sensitivity")
    ax.set_xlabel("Lag (Trading Days)")
    ax.set_ylabel("Correlation")
    fig.tight_layout()
    return fig
