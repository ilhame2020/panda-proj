
def average_monthly_revenue(df):
    """Return mean total_amount per month."""
    if "order_date" in df.columns:
        df = df.set_index("order_date")#The index becomes the dates instead of row numbers.
        return df["total_amount"].resample("ME").mean()
    return None

def top_n_largest_orders(df,column,columnby,num=5):
    """Return top 5 orders by total_amount."""
    return df.nlargest(num, columnby)[[column, columnby]]

def compute_grouped_kpis(df):
    """
    Computes key performance indicators (KPIs) for the dataset:
    
    1. Global statistics on total_amount (mean, median, min, max)
    2. Regional analysis (Sum, Mean, Count)
    3. Product category analysis (Sum, Mean, Count)
    4. Top 5 products by total revenue

    Returns:
        dict: containing all result DataFrames and Series.
    """

    # 1️⃣ Global statistics
    total_amount_stats = df['total_amount'].agg(['mean', 'median', 'min', 'max'])

    # 2️⃣ Regional KPIs — Named Aggregation (clean output)
    region_analysis = df.groupby('region').agg(
        Total_Revenue=('total_amount', 'sum'),
        Avg_Order_Value=('total_amount', 'mean'),
        Order_Count=('order_id', 'count')
    ).sort_values(by='Total_Revenue', ascending=False)

    # 3️⃣ Product Category KPIs
    category_analysis = df.groupby('product_category').agg(
        Total_Revenue=('total_amount', 'sum'),
        Avg_Order_Value=('total_amount', 'mean'),
        Order_Count=('order_id', 'count')
    ).sort_values(by='Total_Revenue', ascending=False)

    # 4️⃣ Top 5 Products by revenue
    top_5_products = (
        df.groupby('product_id')['total_amount']
        .sum()
        .nlargest(5)
    )

    return {
        "total_amount_stats": total_amount_stats,
        "region_analysis": region_analysis,
        "category_analysis": category_analysis,
        "top_5_products": top_5_products
    }
