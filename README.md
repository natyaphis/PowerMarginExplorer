# China Power Margin Explorer

Minimal Python MVP to explore the relationship between coal prices and Chinese power-sector equities.

## Project Structure

```text
china-power-margin-explorer/
├── data/
│   ├── coal_price.csv
│   ├── stock_600011.csv
│   ├── stock_600027.csv
│   └── stock_600795.csv
├── src/
│   ├── analysis.py
│   ├── data_loader.py
│   └── visualization.py
├── app.py
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## What This MVP Includes

- CSV-based data loading with simple column standardization
- Date alignment across coal and stock price series
- Placeholder analysis functions for returns and correlations
- Minimal Streamlit UI to inspect merged data

## Example CSV Schema

All CSV files can use this simple schema:

```csv
date,price
2024-01-02,850.0
2024-01-03,848.5
2024-01-04,852.0
```

Notes:

- `date`: trading date or observation date
- `price`: coal price or stock closing price

If a CSV uses a different second-column name, `data_loader.py` will still treat the first non-`date` column as the price series and rename it during loading.

## License

All Rights Reserved. See [LICENSE](LICENSE).
