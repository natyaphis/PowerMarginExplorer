from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_csv(file_path: str | Path, value_name: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df.columns = [column.strip().lower() for column in df.columns]

    if "date" not in df.columns:
        raise ValueError(f"Missing 'date' column in {file_path}")

    price_column = "price"
    if "price" not in df.columns:
        candidates = [column for column in df.columns if column != "date"]
        if not candidates:
            raise ValueError(f"Missing price column in {file_path}")
        price_column = candidates[0]

    standardized = df[["date", price_column]].rename(columns={price_column: value_name})
    standardized["date"] = pd.to_datetime(standardized["date"])
    return standardized.sort_values("date").reset_index(drop=True)


def load_coal_price(file_path: str | Path | None = None) -> pd.DataFrame:
    file_path = file_path or DATA_DIR / "coal_price.csv"
    return load_csv(file_path, "coal_price")


def load_stock_price(stock_code: str, file_path: str | Path | None = None) -> pd.DataFrame:
    file_path = file_path or DATA_DIR / f"stock_{stock_code}.csv"
    return load_csv(file_path, f"stock_{stock_code}")


def load_merged_data(stock_codes: list[str] | None = None) -> pd.DataFrame:
    stock_codes = stock_codes or ["600011", "600027", "600795"]

    merged = load_coal_price()
    for stock_code in stock_codes:
        stock_df = load_stock_price(stock_code)
        merged = merged.merge(stock_df, on="date", how="outer")

    return merged.sort_values("date").reset_index(drop=True)
