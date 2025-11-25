# TPPandas -- E-commerce Data Preprocessing Pipeline

A complete, modular, and well-structured data preprocessing system built
in Python using Pandas. This project is designed to clean, explore, and
prepare an e-commerce dataset for further analysis, dashboards, or
machine learning.

## Project Goals

-   Provide a clean and organized preprocessing workflow
-   Modular functions grouped by logical tasks
-   A reusable full preprocessing pipeline
-   A notebook for interactive testing and exploration
-   Scripts for running the pipeline from the terminal
-   Results saved systematically

## Project Structure

    TPPANDAS/
    │
    ├── data/
    │   ├── morocco_ecommerce.csv
    │   ├── morocco_ecommerce.json
    │   └── morocco_ecommerce.xlsx
    │
    ├── notebooks/
    │   └── pipeline_notebook.ipynb
    │
    ├── preprocessing/
    │   ├── __init__.py
    │   ├── load_and_inspect.py
    │   ├── missing_values.py
    │   ├── duplicates.py
    │   ├── filtering.py
    │   ├── descriptive_stats.py
    │   ├── datetime_processing.py
    │   ├── string_cleaning.py
    │   ├── outliers.py
    │   └── pipeline/
    │       ├── __init__.py
    │       └── pipeline.py
    │
    ├── scripts/
    │   ├── __init__.py
    │   └── run_pipeline.py
    │
    ├── results/
    │   └── cleaned_dataset.csv
    │
    └── README.md

## Installation

1.  Create virtual environment:

```{=html}
<!-- -->
```
    python -m venv venv

2.  Activate it:

-   Windows: `venv\Scripts\activate`
-   macOS/Linux: `source venv/bin/activate`

3.  Install dependencies:

```{=html}
<!-- -->
```
    pip install pandas

## Running Full Preprocessing

### In Notebook

``` python
from preprocessing.pipeline import full_preprocessing
df = full_preprocessing("./data/morocco_ecommerce.csv")
```

### From Terminal

    python scripts/run_pipeline.py

## Results

Cleaned dataset saved in:

    results/cleaned_dataset.csv

## License

MIT License
