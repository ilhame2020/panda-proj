import pandas as pd
from datetime import datetime


def normalize_date(data, column, test_mode=False):
    """
    Convertit une colonne date en datetime en gérant plusieurs formats.
    Les valeurs invalides deviennent NaT.

    test_mode=True :
        - affiche les valeurs avant/après
        - montre les dates non reconnues
        - affiche un résumé des comptes
    """

    if column not in data.columns:
        raise ValueError(f"La colonne '{column}' n'existe pas dans le DataFrame.")

    if test_mode:
        print("\n========== [TEST MODE] normalize_date() ==========")
        print(f"\nBefore normalization (raw values of '{column}'):")
        print(data[column].head(10))

        print("\nUnique sample values BEFORE:")
        print(data[column].dropna().astype(str).unique()[:15])

    # --- Internal parser ---
    def parse_date(val):
        if pd.isna(val):
            return pd.NaT

        val = str(val).strip()

        # Normalize separators
        val = val.replace('/', '-').replace('\\', '-')

        # Allowed formats
        formats = [
            "%Y-%m-%d", 
            "%d-%m-%Y", 
            "%d-%m-%Y %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(val, fmt)
            except:
                continue

        return pd.NaT  # nothing matched

    # --- Apply parsing ---
    parsed = data[column].apply(parse_date)

    # Test mode: show invalid dates
    if test_mode:
        invalid_mask = parsed.isna() & data[column].notna()
        num_invalid = invalid_mask.sum()

        print(f"\nInvalid date values detected: {num_invalid}")

        if num_invalid > 0:
            print("\nSample of invalid values:")
            print(data.loc[invalid_mask, column].head(10))

        print("\nAfter normalization (parsed values):")
        print(parsed.head(10))

        print("\n=====================================================")

    # Assign parsed values back to df
    data[column] = parsed

    return data