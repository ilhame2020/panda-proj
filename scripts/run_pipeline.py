import argparse
import logging
import os
from tqdm import tqdm
import pandas as pd
from preprocessing.pipeline import full_preprocessing

# -------------------------------------------------
#  Purpose of this file:
# -------------------------------------------------
#📌 Automating the cleaning process without opening Jupyter Notebook
#📌 Make sure the Command is like this :
#   python scripts/run_pipeline.py --input data/morocco_ecommerce.csv --output results/clean.csv




# -------------------------------------------------
# Setup logging
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    datefmt="%H:%M:%S",
)


# -------------------------------------------------
# Helper validation functions
# -------------------------------------------------
def validate_input_file(path):
    if not os.path.exists(path):
        logging.error(f"Input file does NOT exist: {path}")
        raise FileNotFoundError(f"File not found: {path}")
    logging.info(f"Input file found: {path}")


def validate_output_folder(path):
    folder = os.path.dirname(path)
    if folder != "" and not os.path.exists(folder):
        logging.info(f"Creating output folder: {folder}")
        os.makedirs(folder)


# -------------------------------------------------
# Main run function
# -------------------------------------------------
def run_pipeline(input_path, output_path):

    try:
        logging.info("🔍 Starting pipeline...")

        # Validate inputs
        validate_input_file(input_path)
        validate_output_folder(output_path)

        # Progress bar
        steps = [
            "Loading + Inspecting",
            "Missing Values",
            "Duplicates",
            "String Cleaning",
            "Datetime",
            "Outliers",
            "Exporting"
        ]

        for _ in tqdm(range(len(steps)), desc="Processing", ncols=80):
            pass

        # Run full pipeline
        cleaned_df = full_preprocessing(input_path)

        # Save cleaned data
        cleaned_df.to_csv(output_path, index=False)
        logging.info(f"✨ Cleaned dataset saved to: {output_path}")

        logging.info("🎉 Pipeline completed successfully.")

    except Exception as e:
        logging.error(f"❌ Pipeline failed: {str(e)}")


# -------------------------------------------------
# Argument parser
#
# -------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run full data preprocessing pipeline.")

    parser.add_argument("--input", type=str, required=True,
                        help="Path to input CSV file")

    parser.add_argument("--output", type=str, required=True,
                        help="Path to save cleaned CSV file")

    args = parser.parse_args()

    run_pipeline(args.input, args.output)
