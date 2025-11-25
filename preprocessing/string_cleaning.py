#(Q20–Q21)
def clean_city_format(df):
    """Trim spaces and convert city to Title Case."""
    if "city" in df.columns:
        df["city"] = df["city"].astype(str).str.strip().str.title()
    return df


def replace_casa_variants(df):
    """Replace any variation of Casa with Casablanca."""
    if "city" in df.columns:
        df["city"] = df["city"].replace(
            to_replace=r"(?i)casa.*",
            value="Casablanca",
            regex=True
        )
    return df
