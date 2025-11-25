import pandas as pd
#(Q1–Q4)


def load_data(file_path):
    if file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        return pd.read_json(file_path)
    elif file_path.endswith('.csv'):
        return pd.read_csv(file_path, sep="|")
    else:
        raise ValueError("Unsupported file format")
    
def inspect_data(df):
    """Display basic information about the DataFrame."""
    print("\nDataFrame Shape:", df.shape)
    print("\nDataFrame Columns:", df.columns.tolist())
    print("\nData Types:\n", df.dtypes)


