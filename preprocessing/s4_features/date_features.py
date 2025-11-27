import pandas as pd

def add_date_features(df):
    """Create year, month, weekday from order_date."""
    if "order_date" in df.columns:
        df["year"] = df["order_date"].dt.year
        df["month"] = df["order_date"].dt.month
        df["weekday"] = df["order_date"].dt.day_name()
    return df

def add_date_variables(df, date_cols=["order_date", "ship_date"]):
    """
    Ajoute des variables de date pour chaque colonne dans date_cols :
    - <col>_year   (int)
    - <col>_month  (int)
    - <col>_day    (int)
    - <col>_weekday (string)
    """
    
    df = df.copy()
    
    for date_col in date_cols:
        # Convertir en datetime
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        
        # Suffixe basé sur le nom de la colonne
        suffix = date_col.replace("_date", "")
        
        # Extraction
        df[f"{suffix}_year"] = df[date_col].dt.year.astype("Int64")
        df[f"{suffix}_month"] = df[date_col].dt.month.astype("Int64")
        df[f"{suffix}_day"] = df[date_col].dt.day.astype("Int64")
        df[f"{suffix}_weekday"] = df[date_col].dt.day_name()

    return df

def convert_dates(df):
    """Convert order_date and ship_date to datetime."""
    date_cols = ["order_date", "ship_date"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df




def filter_after_date(df, date_str):
    """Return all orders after a given date."""
    if "order_date" in df.columns:
        return df[df["order_date"] > date_str]
    return df
