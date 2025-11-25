import pandas as pd
import argparse
import numpy as np
import os
# -------------------------------------------------
# Purpose of this file:
# -------------------------------------------------
# export_eda_summary.py is designed to produce a lightweight, quick text summary, 
# not to run the entire preprocessing suite.
# -------------------------------------------------

def mad_outlier_count(df):
    """
    Detect outliers using the MAD (Median Absolute Deviation) method.
    Returns the count of outliers in total_amount.
    """
    col = df["total_amount"]

    median = col.median()
    mad = np.median(np.abs(col - median))

    # Avoid division by zero
    if mad == 0:
        return 0

    modified_z_scores = 0.6745 * (col - median) / mad

    outliers = np.abs(modified_z_scores) > 3.5
    return outliers.sum()


def generate_eda_report(df, output_path):
    lines = []

    lines.append("📊 EDA SUMMARY\n")
    lines.append("=====================================\n\n")

    # Shape
    lines.append(f"Shape: {df.shape}\n\n")

    # Missing values
    lines.append("🔸 Missing Values:\n")
    lines.append(df.isna().sum().to_string())
    lines.append("\n\n")

    # Duplicates
    lines.append(f"🔸 Duplicate Rows: {df.duplicated().sum()}\n\n")

    # Stats
    lines.append("🔸 Numeric Summary:\n")
    lines.append(df.describe().to_string())
    lines.append("\n\n")

    # Outliers — MAD method (NEW LOGIC)
    outlier_count = mad_outlier_count(df)
    lines.append(f"🔸 Outliers (MAD method): {outlier_count}\n\n")

    # Save
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export EDA summary to text file.")

    parser.add_argument("--input", type=str, required=True,
                        help="Path to the cleaned CSV file")

    parser.add_argument("--output", type=str, required=True,
                        help="Where to save the report")

    args = parser.parse_args()

    df = pd.read_csv(args.input)
    path = generate_eda_report(df, args.output)

    print(f"EDA summary saved to {path}")