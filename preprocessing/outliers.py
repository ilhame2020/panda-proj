#(Q26–Q28)
import numpy as np

def detect_outliers_iqr(df):
    """Detect outliers using IQR method."""
    col = df["total_amount"]
    Q1 = col.quantile(0.25)
    Q3 = col.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(col < lower) | (col > upper)]


def detect_outliers_zscore(df):
    """Detect outliers using Z-score."""
    col = df["total_amount"]
    z = (col - col.mean()) / col.std()
    return df[np.abs(z) > 3]


def top_5_largest_orders(df):
    """Return top 5 orders by total_amount."""
    return df.nlargest(5, "total_amount")[["order_id", "total_amount"]]
