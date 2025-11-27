import pandas as pd
import numpy as np
import warnings
from datetime import datetime


# -----------------------------------------------------------
# Helper: Detect if a column resembles dates
# -----------------------------------------------------------
def looks_like_date_series(series):
    sample = series.dropna().astype(str).head(20)
    if sample.empty:
        return False

    pattern_match = sample.str.contains(
        r"\d{4}[-/]\d{2}[-/]\d{2}",
        regex=True,
        na=False,
    ).mean()

    return pattern_match > 0.4


# -----------------------------------------------------------
# 1. Basic structure
# -----------------------------------------------------------
def profile_basic_structure(df, n=15):
    print("\n================= 1. INITIAL INSPECTION =================")

    print(f"\n🔎 First {n} rows:")
    print(df.head(n))

    print("\n📏 Shape:")
    print(f"- Rows: {df.shape[0]}")
    print(f"- Columns: {df.shape[1]}")

    print("\n📚 Columns & Data Types:")
    print(df.dtypes)

    print("\n📂 Structural Info:")
    df.info()

    print("\n📊 df.describe(include='all'):")
    df.describe(include="all")


# -----------------------------------------------------------
# 2. Type issues
# -----------------------------------------------------------
def find_invalid_values(data, column, dtype="datetime", test_mode=False):
    """
    Détecte les valeurs invalides dans une colonne selon le type attendu.
    
    Parameters:
    - data: pandas DataFrame
    - column: nom de la colonne à vérifier
    - dtype: type attendu ("datetime", "numeric", "string")
    - test_mode (bool): si True, affiche un aperçu détaillé
    
    Returns:
    - array des valeurs invalides (uniques)
    """

    if column not in data.columns:
        raise ValueError(f"Column '{column}' does not exist in dataframe")

    col = data[column]

    if dtype == "datetime":
        converted = pd.to_datetime(col, errors="coerce")
        problems = col[converted.isna()].unique()

    elif dtype == "numeric":
        converted = pd.to_numeric(col, errors="coerce")
        problems = col[converted.isna()].unique()

    elif dtype == "string":
        problems = col[col.isna()].unique()

    else:
        raise ValueError("dtype doit être 'datetime', 'numeric' ou 'string'")

    # --------------------------
    # TEST MODE
    # --------------------------
    if test_mode:
        print(f"\n===== TEST MODE: Invalid values in '{column}' (expected {dtype}) =====")

        print(f"Number of invalid values: {len(problems)}")

        if len(problems) > 0:
            print("\nSample of invalid values:")
            print(problems[:20])  # show first 20

        print("==================================================================")

    return problems



# -----------------------------------------------------------
# 3. Numeric anomalies
# -----------------------------------------------------------
def profile_unusual_numeric_stats(df):
    print("\n================= 3. NUMERIC ANOMALY CHECK =================")

    num_cols = df.select_dtypes(include=[np.number]).columns

    for col in num_cols:
        s = df[col]

        if s.min() < 0:
            print(f"- ⚠ Negative values in '{col}'")

        if s.max() > s.mean() + 4 * s.std():
            print(f"- ⚠ Extreme values in '{col}'")

        if s.std() == 0:
            print(f"- ⚠ Constant column '{col}' (no variation)")


# -----------------------------------------------------------
# 4. Text inconsistencies
# -----------------------------------------------------------
def profile_text_inconsistencies(df):
    print("\n================= 4. TEXT CONSISTENCY CHECK =================")

    text_cols = df.select_dtypes(include=["object"]).columns

    for col in text_cols:
        sample = df[col].dropna().astype(str).unique()[:10]
        print(f"\n🔤 Column '{col}' — sample values:")
        print(sample)


# -----------------------------------------------------------
# 5. Date issues (NO WARNINGS)
# -----------------------------------------------------------
def profile_date_issues(df):
    print("\n================= 5. DATE QUALITY CHECK =================")

    for col in df.columns:
        series = df[col]

        if not looks_like_date_series(series):
            continue

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=Warning)
            date_col = pd.to_datetime(series, errors="coerce")

        print(f"\n🗓 Column '{col}' contains dates")

        invalid = date_col.isna() & series.notna()
        if invalid.sum() > 0:
            print(f"  > Invalid dates: {invalid.sum()}")

        if date_col.notna().any():
            min_d, max_d = date_col.min(), date_col.max()

            if min_d < datetime(1900, 1, 1):
                print(f"  > Suspicious early date: {min_d}")

            if max_d > datetime.now():
                print(f"  > Suspicious future date: {max_d}")

# -----------------------------------------------------------
# duplicate rows analysis
# -----------------------------------------------------------
def number_duplicated_rows(data, test_mode=False):
    """
    Retourne le nombre de lignes dupliquées dans le DataFrame.
    
    Parameters:
        data (pd.DataFrame)
        test_mode (bool): si True, affiche un aperçu détaillé.
    
    Returns:
        int : nombre de lignes dupliquées
    """

    duplicated_mask = data.duplicated()
    count = duplicated_mask.sum()

    # --------------------------
    # TEST MODE OUTPUT
    # --------------------------
    if test_mode:
        print("\n===== TEST MODE: Duplicate Row Analysis =====")
        print(f"Total duplicated rows: {count}")

        if count > 0:
            print("\nIndices of duplicated rows:")
            print(data.index[duplicated_mask].tolist()[:20])  # first 20 indices

            print("\nPreview of duplicated rows:")
            print(data[duplicated_mask].head(10))
        else:
            print("No duplicated rows found.")

        print("=================================================")

    return count

# -----------------------------------------------------------
# MASTER FUNCTION
# -----------------------------------------------------------
def generate_profiling_report(df, n=15):
    print("\n================= FULL DATA PROFILING REPORT =================")

    profile_basic_structure(df, n)
    find_invalid_values(df, "order_date", dtype="datetime", test_mode=True)
    find_invalid_values(df, "unit_price", dtype="numeric", test_mode=True)
    find_invalid_values(df, "order_id", dtype="string", test_mode=True)
    find_invalid_values(df, "quantity", dtype="numeric",test_mode=True)
    number_duplicated_rows(df, test_mode=True)
    profile_unusual_numeric_stats(df)
    profile_text_inconsistencies(df)
    profile_date_issues(df)

    print("\n================= END OF PROFILING REPORT =================")
