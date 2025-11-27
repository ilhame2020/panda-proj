#(Q17–Q19)
def summarize_total_amount(df):
    """Return mean, median, min, max of total_amount."""
    col = df["total_amount"]
    return {
        "mean": col.mean(),
        "median": col.median(),
        "min": col.min(),
        "max": col.max()
    }


def region_highest_average_total(df):
    """Return region with highest average total_amount."""
    return df.groupby("region")["total_amount"].mean().idxmax()#["total_amount"].mean()  → résultat : une Series 
                                                               # où l’index = les régions les valeurs = la moyenne du total_amount


def product_highest_revenue(df):
    """Return product_id with highest total revenue."""
    revenue = df.groupby("product_id")["total_amount"].sum()
    return revenue.idxmax(), revenue.max()
