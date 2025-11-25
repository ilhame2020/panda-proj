import pandas as pd
import numpy as np
#(Q5–Q9)

def count_missing(df):
    """Count missing values per column."""
    return df.isna().sum()


def column_with_most_missing(df):
    """Return the column with the highest missing count."""
    missing = df.isna().sum()
    return missing.idxmax(), missing.max()


def drop_missing_rows(df):
    """Remove rows containing ANY missing values."""
    return df.dropna()

def count_city_unknown(df):
    """Count missing values in the city column."""
    return (df["city"] == "Unknown").sum()

def fill_city_unknown(df):
    """Fill missing city values with 'Unknown'."""
    df["city"] = df["city"].fillna("Unknown")
    return df
def count_unit_price_missing(df):
    """Count missing values in the unit_price column."""
    return df["unit_price"].isna().sum()

def detect_unusual_values(df, column, expected_type="float"):
    """
    Detect unusual or invalid values in a column.
    
    Parameters:
        df: DataFrame
        column: column name to inspect
        expected_type: "float", "int", "str", or "date"
    
    Returns:
        DataFrame containing rows with unusual values.
    """

    col = df[column]

    # Define invalid tokens seen in messy datasets
    invalid_tokens = {"free", "none", "unknown", "n/a", "null", ""}

    # 1. Identify invalid tokens (case-insensitive)
    mask_invalid_string = col.astype(str).str.lower().isin(invalid_tokens)

    # 2. Identify non-numeric where numeric is expected
    if expected_type in ["float", "int"]:
        # True for values that CANNOT be converted to numbers
        mask_non_numeric = pd.to_numeric(col, errors="coerce").isna()
    else:
        mask_non_numeric = pd.Series([False] * len(col))

    # 3. Identify non-date values where date is expected
    if expected_type == "date":
        mask_non_date = pd.to_datetime(col, errors="coerce").isna()
    else:
        mask_non_date = pd.Series([False] * len(col))

    # Combine all unusual conditions
    unusual_mask = mask_invalid_string | mask_non_numeric | mask_non_date

    # Exclude actual proper NaN (we only care about invalid text, etc.)
    unusual_mask &= col.notna()

    return df[unusual_mask]

def fill_unit_price_mean(df):
    """Fill missing unit_price with column mean."""
    if "unit_price" in df.columns:
        df["unit_price"] = df["unit_price"].fillna(df["unit_price"].mean())
    return df