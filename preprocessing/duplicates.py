#(Q10–Q12)
def count_duplicates(df):
    """Count fully duplicated rows."""
    return df.duplicated().sum()


def drop_duplicates_all(df):
    """Drop all fully duplicated rows."""
    return df.drop_duplicates()



def drop_duplicates_order_id(df):
    # Look at the order_id column only
    # If two or more rows have the same order_id → treat them as duplicates
    # Keep only the first occurrence
    # Remove all others
    """Drop duplicated order_id rows, keep first."""
    if "order_id" in df.columns:
        return df.drop_duplicates(subset="order_id", keep="first")
    return df
