#(Q20–Q21)
import pandas as pd

def clean_city_format(df):
    """Trim spaces and convert city to Title Case."""
    if "city" in df.columns:
        df["city"] = df["city"].astype(str).str.strip().str.title()
    return df




def replace_casa_variants(df):
    """Replace any variation of 'Casa*' with 'Casablanca'."""
    if "city" in df.columns:
        df["city"] = df["city"].replace(
            to_replace=r"(?i)casa.*",
            value="Casablanca",
            regex=True
        )
    return df


def replace_nan_columns_by_words(data, columns, words):
    if len(columns) != len(words):
        raise ValueError("Les listes columns et words doivent avoir la même longueur.")
    
    for col, word in zip(columns, words):
        # Remplacer les chaînes "nan" par un vrai NaN
        data[col] = data[col].replace("nan", pd.NA)
        # Remplacer les NaN par le mot fourni
        data[col] = data[col].fillna(word)
    
    return data


def clean_city_column(data, column, test_mode=False):
    """
    Clean and standardize a city column:
    - lowercasing
    - trimming spaces
    - replacing known variants via mapping
    - converting "nan"/"none" to NaN

    test_mode=True provides:
      - BEFORE preview
      - values replaced
      - unknown city names
      - AFTER preview
    """

    if column not in data.columns:
        raise ValueError(f"La colonne '{column}' n'existe pas dans le DataFrame.")

    # -----------------------
    # TEST MODE: BEFORE
    # -----------------------
    if test_mode:
        print("\n========== [TEST MODE] clean_city_column() ==========")
        print(f"\nBEFORE cleaning ('{column}'):")
        print(data[column].head(10))

        print("\nRaw unique values (sample):")
        print(data[column].dropna().astype(str).unique()[:20])

    # -----------------------
    # Step 1 — Normalize text
    # -----------------------
    data[column] = data[column].astype(str).str.strip().str.lower()

    # map common invalid string placeholders to NaN
    data[column] = data[column].replace(
        ["nan", " nan ", "none", " none ", ""], 
        pd.NA
    )

    # -----------------------
    # Step 2 — City normalization dictionary
    # -----------------------
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

    # -----------------------
    # Step 3 — Apply mapping
    # -----------------------
    if test_mode:
        before_map = data[column].copy()

    data[column] = data[column].apply(lambda x: mapping.get(x, x))

    # -----------------------
    # TEST MODE: AFTER + ANALYSIS
    # -----------------------
    if test_mode:

        print("\nValues replaced by mapping:")
        replaced = before_map[before_map != data[column]]
        if len(replaced) > 0:
            print(replaced.head(10))
        else:
            print("No values were replaced.")

        print("\nUnknown city names (not in mapping):")
        unknown = sorted(
            {c for c in data[column].dropna().unique() if c not in mapping.values()}
        )
        print(unknown[:20] if unknown else "None")

        print("\nAFTER cleaning:")
        print(data[column].head(10))

        print("\n=====================================================")

    return data




def clean_region_column(data, column, test_mode=False):
    """
    Clean and standardize a region column:
    - lowercase, strip whitespace
    - normalize multiple spaces
    - normalize hyphens
    - convert fake 'nan' strings to real NaN
    - map dirty region names to clean ones

    test_mode=True prints:
        - BEFORE preview
        - sample of raw unique values
        - values replaced by the mapping
        - unknown regions not in mapping
        - AFTER preview
    """

    if column not in data.columns:
        raise ValueError(f"La colonne '{column}' n'existe pas dans le DataFrame.")

    # -----------------------
    # TEST MODE: BEFORE
    # -----------------------
    if test_mode:
        print("\n========== [TEST MODE] clean_region_column() ==========")
        print(f"\nBEFORE cleaning ('{column}'):")
        print(data[column].head(10))

        print("\nRaw unique region values (sample):")
        print(data[column].dropna().astype(str).unique()[:20])

    # -----------------------
    # Step 1 — Normalize casing & whitespace
    # -----------------------
    data[column] = data[column].astype(str).str.strip().str.lower()

    # convert common fake-NAN text to real NaN
    data[column] = data[column].replace(
        ["nan", " none ", "nan "],
        pd.NA
    )

    # normalize multiple spaces
    data[column] = data[column].str.replace(r"\s+", " ", regex=True)

    # normalize spaces around hyphens
    data[column] = data[column].str.replace(r"\s*-\s*", "-", regex=True)

    # -----------------------
    # Step 2 — Mapping dictionary
    # -----------------------
    mapping = {
        "casablanca-settat": "casablanca-settat",
        "casablanca settat": "casablanca-settat",

        "béni mellal-khénifra": "béni mellal-khénifra",
        "béni mellal khénifra": "béni mellal-khénifra",

        "oriental": "oriental",

        "marrakech-safi": "marrakech-safi",
        "marrakech safi": "marrakech-safi",

        "tanger-tétouan-al hoceïma": "tanger-tétouan-al hoceïma",
        "tanger tétouan al hoceïma": "tanger-tétouan-al hoceïma",

        "souss-massa": "souss-massa",
        "souss massa": "souss-massa",

        "dakhla-oued ed-dahab": "dakhla-oued ed-dahab",
        "dakhla oued ed dahab": "dakhla-oued ed-dahab",

        "drâa-tafilalet": "drâa-tafilalet",
        "drâa tafilalet": "drâa-tafilalet",

        "laâyoune-sakia el hamra": "laâyoune-sakia el hamra",
        "laâyoune sakia el hamra": "laâyoune-sakia el hamra",

        "guelmim-oued noun": "guelmim-oued noun",
        "guelmim oued noun": "guelmim-oued noun",

        "fès-meknès": "fès-meknès",
        "fès meknès": "fès-meknès",

        "rabat-salé-kénitra": "rabat-salé-kénitra",
        "rabat salé kénitra": "rabat-salé-kénitra",
    }

    # -----------------------
    # Step 3 — Apply mapping
    # -----------------------
    if test_mode:
        before_map = data[column].copy()

    data[column] = data[column].apply(lambda x: mapping.get(x, x) if pd.notna(x) else x)

    # -----------------------
    # TEST MODE: AFTER
    # -----------------------
    if test_mode:
        print("\nValues replaced by mapping:")
        replaced = before_map[before_map != data[column]]
        if len(replaced) > 0:
            print(replaced.head(10))
        else:
            print("No region names were replaced.")

        print("\nUnknown region names (not in mapping):")
        unknown = sorted({
            r for r in data[column].dropna().unique()
            if r not in mapping.values()
        })
        print(unknown[:20] if unknown else "None")

        print("\nAFTER cleaning:")
        print(data[column].head(10))
        print("\n=====================================================")

    return data



def strip_whitespace(df, column):
    """Remove leading/trailing whitespace from a string column."""
    if column in df.columns:
        df[column] = df[column].astype(str).str.strip()
    return df


def standardize_case(df, columns):
    """Standardize casing of text columns."""
    for col in columns:
      df[col] = df[col].astype(str).str.strip().str.title()
    
    return df


def clean_text_column(df, column):
    """Apply all cleaning steps to a text column."""
    df = strip_whitespace(df, column)
    df = standardize_case(df, column, mode="title")
    return df
