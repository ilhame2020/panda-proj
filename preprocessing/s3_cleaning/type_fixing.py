import pandas as pd
import numpy as np
import re

def convert_to_float(df, column):
    """Convert a column to float, coercing invalid values to NaN."""
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df

def convert_to_type(data, columns, types):
    """
    Convertit plusieurs colonnes selon leur type :
    - 'numerique'  -> numeric (float ou int)
    - 'string'     -> string propre
    - 'date'       -> datetime (NaT si invalide)
    """

    for col, t in zip(columns, types):

        if t == "numerique":
            data[col] = pd.to_numeric(data[col], errors="coerce")

        elif t == "string":
            data[col] = data[col].astype(str).str.strip()

        elif t == "date":
            data[col] = pd.to_datetime(data[col], errors="coerce")

        else:
            print(f"Type inconnu : {t} pour la colonne {col}")

    return data
# -----------------------------
# Convert number words → numeric
# -----------------------------
NUM_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
    "hundred": 100
}

def convert_number_words_to_numeric(value):
    """Converts number words into numeric values."""
    if not isinstance(value, str):
        return value

    value = value.lower().strip()

    # Try direct float conversion
    try:
        return float(value)
    except:
        pass

    # Handle hyphen: "twenty-one"
    if "-" in value:
        parts = value.split("-")
        if len(parts) == 2 and parts[0] in NUM_WORDS and parts[1] in NUM_WORDS:
            return NUM_WORDS[parts[0]] + NUM_WORDS[parts[1]]

    # Handle phrases: "one hundred twenty"
    tokens = value.split()
    total = 0
    current = 0

    for word in tokens:
        if word in NUM_WORDS:
            number = NUM_WORDS[word]
            if number == 100:
                current *= 100
            else:
                current += number
        else:
            return value  # Unknown word → return original

    total += current
    return float(total)


# -----------------------------
# Detect invalid / unusual values
# -----------------------------
def detect_unusual_values(df, column, expected_type="float"):
    col = df[column].astype(str).str.lower()

    invalid_tokens = {"free", "none", "unknown", "n/a", "null", ""}

    mask_invalid_text = col.isin(invalid_tokens)

    # Values that cannot be converted to numeric
    mask_non_numeric = pd.to_numeric(df[column], errors="coerce").isna()

    unusual_mask = (mask_invalid_text | mask_non_numeric) & df[column].notna()

    return df[unusual_mask]


# -----------------------------
# Main cleaning function
# -----------------------------
def clean_numeric_column(df, column, test_mode=False):
    """
    Steps:
    1. Convert number words (e.g., "twenty" → 20)
    2. Detect unusual or invalid values (free, unknown, non-numeric)
    3. Replace invalid values with 0
    4. Convert column to float
    """
    if column not in df.columns:
        print(f"[WARNING] Column '{column}' does not exist.")
        return df

    # PREVIEW BEFORE CLEANING
    if test_mode:
        print(f"\n[TEST MODE] Cleaning '{column}' → BEFORE:")
        print(df[column].head(10))

    # Step 1 — Convert number words
    df[column] = df[column].apply(convert_number_words_to_numeric)

    # Step 2 — Detect invalid values
    unusual = detect_unusual_values(df, column)

    if len(unusual) > 0:
        print(f"\nInvalid values detected in '{column}':")
        print(unusual)

        # Step 3 — Replace all invalid/unusual values with 0
        df.loc[unusual.index, column] = 0

    # Step 4 — Convert everything to float
    df = convert_to_float(df, column)

    # PREVIEW AFTER CLEANING
    if test_mode:
        print(f"\n[TEST MODE] Cleaning '{column}' → AFTER:")
        print(df[column].head(10))

    return df
