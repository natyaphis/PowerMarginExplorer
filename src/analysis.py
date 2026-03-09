import pandas as pd


def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result = result.sort_values("date").reset_index(drop=True)

    price_columns = [
        column for column in result.columns if column == "coal_price" or column.startswith("stock_")
    ]
    for column in price_columns:
        valid_prices = result[column].dropna()
        result[f"{column}_return"] = valid_prices.pct_change().reindex(result.index)

    if "coal_price_return" not in result.columns:
        raise ValueError("Missing coal_price column for return calculation.")

    result["margin_proxy"] = -result["coal_price_return"]
    return result


def rolling_correlation(df: pd.DataFrame, stock_col: str) -> pd.DataFrame:
    stock_return_col = f"{stock_col}_return"
    required_columns = ["date", "coal_price_return", stock_return_col]
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    result = df[required_columns].copy().dropna().sort_values("date").reset_index(drop=True)
    result["rolling_correlation"] = (
        result["coal_price_return"].rolling(window=30, min_periods=30).corr(result[stock_return_col])
    )
    return result[["date", "rolling_correlation"]]


def lag_correlation(df: pd.DataFrame, stock_col: str) -> pd.DataFrame:
    stock_return_col = f"{stock_col}_return"
    required_columns = ["coal_price_return", stock_return_col]
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    clean = df[required_columns].copy()
    correlations = []

    for lag in [0, 5, 10]:
        shifted = clean[stock_return_col].shift(-lag)
        pair = pd.DataFrame(
            {
                "coal_price_return": clean["coal_price_return"],
                "stock_return": shifted,
            }
        ).dropna()

        correlation = pair["coal_price_return"].corr(pair["stock_return"]) if not pair.empty else pd.NA
        correlations.append({"lag_days": lag, "correlation": correlation})

    return pd.DataFrame(correlations)
