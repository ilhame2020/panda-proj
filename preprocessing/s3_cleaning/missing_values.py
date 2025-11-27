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

def complete_amounts(df, test_mode=False):
    """
    Complète les colonnes quantity, unit_price et total_amount lorsque possible.

    test_mode = True affiche :
      - valeurs manquantes au début
      - tailles des masques appliqués
      - exemples de lignes complétées
      - aperçu final
    """

    if test_mode:
        print("\n========== [TEST MODE] complete_amounts() ==========")
        print("\nMissing BEFORE:")
        print(df[["quantity", "unit_price", "total_amount"]].isna().sum())

    # Ensure numeric
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')

    # 1️⃣ Compute total_amount when quantity + price are available
    mask_total_missing = df['total_amount'].isna() & df['quantity'].notna() & df['unit_price'].notna()
    if test_mode:
        print(f"\nRows where total_amount can be computed: {mask_total_missing.sum()}")

    df.loc[mask_total_missing, 'total_amount'] = \
        df.loc[mask_total_missing, 'quantity'] * df.loc[mask_total_missing, 'unit_price']

    # 2️⃣ Compute unit_price when quantity + total_amount are available
    mask_unit_missing = df['unit_price'].isna() & df['quantity'].notna() & df['total_amount'].notna()
    if test_mode:
        print(f"Rows where unit_price can be computed: {mask_unit_missing.sum()}")

    df.loc[mask_unit_missing, 'unit_price'] = \
        df.loc[mask_unit_missing, 'total_amount'] / df.loc[mask_unit_missing, 'quantity']

    # 3️⃣ Compute quantity when unit_price > 0 + total_amount available
    mask_quantity_missing = (
        df['quantity'].isna() &
        df['unit_price'].notna() &
        (df['unit_price'] != 0) &
        df['total_amount'].notna()
    )
    if test_mode:
        print(f"Rows where quantity can be computed: {mask_quantity_missing.sum()}")

    df.loc[mask_quantity_missing, 'quantity'] = \
        df.loc[mask_quantity_missing, 'total_amount'] / df.loc[mask_quantity_missing, 'unit_price']

    # 4️⃣ Round and convert to integers
    df['quantity'] = df['quantity'].round()
    df['quantity'] = df['quantity'].astype('Int64')

    # 5️⃣ Fill remaining quantity NaN with mean
    moy_quantity = round(df['quantity'].mean(skipna=True))
    if test_mode:
        print(f"\nReplacing remaining quantity NaN with mean = {moy_quantity}")

    df['quantity'] = df['quantity'].fillna(moy_quantity)

    # 6️⃣ Fill remaining unit_price NaN with mean
    mean_unit_price = df['unit_price'].mean(skipna=True)
    if test_mode:
        print(f"Replacing remaining unit_price NaN with mean = {mean_unit_price:.2f}")

    df['unit_price'] = df['unit_price'].fillna(mean_unit_price)

    # 7️⃣ Recompute final total_amount
    df['total_amount'] = df['quantity'] * df['unit_price']

    if test_mode:
        print("\nAFTER fixing:")
        print(df[["quantity", "unit_price", "total_amount"]].head(10))
        print("\nMissing AFTER:")
        print(df[["quantity", "unit_price", "total_amount"]].isna().sum())
        print("=====================================================")

    return df

city_to_region = {
    "casablanca": "casablanca-settat",
    "mohammedia": "casablanca-settat",
    "settat": "casablanca-settat",

    "rabat": "rabat-salé-kénitra",
    "salé": "rabat-salé-kénitra",
    "kénitra": "rabat-salé-kénitra",

    "marrakech": "marrakech-safi",
    "safi": "marrakech-safi",
    "chichaoua": "marrakech-safi",

    "agadir": "souss-massa",
    "inezgane": "souss-massa",
    "tiznit": "souss-massa",

    "tanger": "tanger-tétouan-al hoceïma",
    "tétouan": "tanger-tétouan-al hoceïma",
    "al hoceïma": "tanger-tétouan-al hoceïma",

    "béni mellal": "béni mellal-khénifra",
    "khénifra": "béni mellal-khénifra",

    "oujda": "oriental",
    "nador": "oriental",
    "berkane": "oriental",

    "laâyoune": "laâyoune-sakia el hamra",
    "dakhla": "dakhla-oued ed-dahab",

    "errachidia": "drâa-tafilalet",
    "ouarzazate": "drâa-tafilalet",
    "guelmim": "guelmim-oued noun",
}

def fix_region_with_city(data, test_mode=False):
    """
    Fix missing or incorrect region values using city information.
    """

    if test_mode:
        print("\n========== [TEST MODE] fix_region_with_city() ==========")
        print("Before fixing, rows where city == 'errachidia':")
        print(data.loc[data["city"].astype(str).str.lower() == "errachidia", ["city", "region"]].head(10))

    # --- Clean text ---
    data["city"] = data["city"].astype(str).str.lower().str.strip()
    data["region"] = data["region"].astype(str).str.lower().str.strip()

    # --- Convert fake NaN strings to real NA ---
    fake_nans = ["nan", "<na>", "none", "na", "n/a", ""]
    data["region"] = data["region"].apply(
        lambda x: pd.NA if x in fake_nans else x
    )

    # --- Fill missing/invalid region using city-to-region mapping ---
    data["region"] = data.apply(
        lambda row: city_to_region[row["city"]]
        if pd.isna(row["region"]) and row["city"] in city_to_region
        else row["region"],
        axis=1
    )

    if test_mode:
        print("\nAfter fixing, rows where city == 'errachidia':")
        print(data.loc[data["city"] == "errachidia", ["city", "region"]].head(10))
        print("========================================================\n")

    return data


# Pour les lignes où region est NaN et city est NaN (ou les deux sont NaN), on laisse les valeurs NaN


def clean_city_column(data, column):
    # convertir en str et nettoyer les espaces
    data[column] = data[column].astype(str).str.strip().str.lower()

    # remplacer les chaînes "nan" par NaN
    data[column] = data[column].replace(["nan", " nan ", " none "], pd.NA)

    # dictionnaire de normalisation
    mapping = {
        "casa": "casablanca",
        "casablanca": "casablanca",
        "khénifra": "khénifra",
        "béni mellal": "béni mellal",
        "guelmim": "guelmim",
        "laâyoune": "laâyoune",
        "tétouan": "tétouan",
        "tanger": "tanger",
        "marrakech": "marrakech",
        "chichaoua": "chichaoua",
        "ouarzazate": "ouarzazate",
        "nador": "nador",
        "berkane": "berkane",
        "agadir": "agadir",
        "fès": "fès",
        "salé": "salé",
        "errachidia": "errachidia",
        "settat": "settat",
        "mohammedia": "mohammedia",
        "tiznit": "tiznit",
        "el jadida": "el jadida",
        "inezgane": "inezgane",
        "oujda": "oujda",
        "meknès": "meknès",
        "safi": "safi"
    }

    # appliquer la normalisation si la valeur existe dans le mapping
    data[column] = data[column].apply(lambda x: mapping.get(x, x))

    return data

def replace_nan_columns_by_words(data, columns, words):
    if len(columns) != len(words):
        raise ValueError("Les listes columns et words doivent avoir la même longueur.")
    
    for col, word in zip(columns, words):
        # Remplacer les chaînes "nan" par un vrai NaN
        data[col] = data[col].replace("nan", pd.NA)
        # Remplacer les NaN par le mot fourni
        data[col] = data[col].fillna(word)
    
    return data


def fill_missing_dates(df, date_columns):
    
    # S'assurer que les colonnes sont en datetime
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Remplir les valeurs manquantes par la mode
    for col in date_columns:
        if df[col].notna().sum() == 0:
            # Si la colonne est entièrement vide, bon courage...
            # On met une date par défaut
            df[col] = df[col].fillna(pd.Timestamp("2000-01-01"))
        else:
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
    
    return df