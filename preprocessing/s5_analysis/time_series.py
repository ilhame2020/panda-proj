import pandas as pd
import matplotlib.pyplot as plt

def analyze_time_series(df, date_column="order_date", value_column="total_amount"):
    """
    Performs full time-series analysis:
    
    1. Sets datetime index
    2. Computes monthly total revenue
    3. Computes monthly average order value
    4. Computes same KPIs using Grouper (optional)
    5. Identifies best-performing month
    6. Generates monthly revenue trend plot
    
    Returns:
        dict with:
            - monthly_revenue
            - monthly_aov
            - best_month
            - best_month_revenue
            - monthly_revenue_alt (Grouper version)
    """

    df = df.copy()

    # 1️⃣ Set index to datetime column
    df.set_index(date_column, inplace=True)
    df.sort_index(inplace=True)

    # 2️⃣ Monthly total revenue
    monthly_revenue = df[value_column].resample("ME").sum()

    # 3️⃣ Monthly AOV
    monthly_aov = df[value_column].resample("ME").mean()

    # 4️⃣ Alternative method (Grouper)
    df_reset = df.reset_index()
    monthly_revenue_alt = df_reset.groupby(
        pd.Grouper(key=date_column, freq="ME")
    )[value_column].sum()

    # 5️⃣ Best performing month
    best_month = monthly_revenue.idxmax()
    best_month_revenue = monthly_revenue.max()

    # 6️⃣ Plot trend
    plt.figure(figsize=(12, 6))
    monthly_revenue.plot(kind='line', marker='o')
    plt.title("Monthly Total Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Revenue (MAD)")
    plt.grid(True)
    plt.savefig("monthly_revenue_trend.png")
    plt.close()

    return {
        "monthly_revenue": monthly_revenue,
        "monthly_aov": monthly_aov,
        "best_month": best_month,
        "best_month_revenue": best_month_revenue,
        "monthly_revenue_alt": monthly_revenue_alt
    }
