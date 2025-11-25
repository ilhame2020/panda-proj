import pandas as pd

#(Q22–Q25)
def convert_dates(df):
    """Convert order_date and ship_date to datetime."""
    date_cols = ["order_date", "ship_date"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def add_date_features(df):
    """Create year, month, weekday from order_date."""
    if "order_date" in df.columns:
        df["year"] = df["order_date"].dt.year
        df["month"] = df["order_date"].dt.month
        df["weekday"] = df["order_date"].dt.day_name()
    return df


def filter_after_date(df, date_str):
    """Return all orders after a given date."""
    if "order_date" in df.columns:
        return df[df["order_date"] > date_str]
    return df


def average_monthly_revenue(df):
    """Return mean total_amount per month."""
    if "order_date" in df.columns:
        df = df.set_index("order_date")#The index becomes the dates instead of row numbers.
        return df["total_amount"].resample("ME").mean()
    return None
