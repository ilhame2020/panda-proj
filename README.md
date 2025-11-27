
# 📦 Morocco E-Commerce Data Cleaning & Analysis  
### **Comprehensive Preprocessing Pipeline (Python · Pandas · VS Code · Jupyter Notebook)**  

This project provides a **fully modular, production-ready preprocessing pipeline** for cleaning, validating, profiling, transforming, and analyzing an e-commerce dataset from Morocco.  
The work follows a structured approach inspired by best practices in **Data Engineering**, **Data Quality**, and **Exploratory Data Analysis (EDA)**.

---

## 📁 Project Structure  

```
tppandas/
│
├── data/
│   ├── morocco_ecommerce.xlsx
│   └── (other raw files…)
│
├── notebooks/
│   └── pipeline_notebook.ipynb   # Main notebook with the full workflow
│
├── preprocessing/
│   ├── __init__.py
│   │
│   ├── s1_loading/
│   │   ├── __init__.py
│   │   └── loading.py            # Load data, inspect_data()
│   │
│   ├── s2_profiling/
│   │   ├── __init__.py
│   │   └── profiling.py          # Full profiling: types, dates, inconsistencies
│   │
│   ├── s3_cleaning/
│   │   ├── cleaning_missing_values.py
│   │   ├── cleaning_duplicates.py
│   │   ├── cleaning_type_fixing.py
│   │   ├── string_cleaning.py
│   │   ├── region_city_fixing.py
│   │   ├── amount_completion.py
│   │   └── date_fixing.py
│   │
│   ├── s4_features/
│   │   ├── feature_engineering.py  # date features, aggregates, new variables
│   │
│   ├── s5_analysis/
│   │   ├── descriptive_stats.py
│   │   ├── grouping_kpis.py
│   │   └── timeseries_analysis.py
│   │
│   └── pipeline/
│       ├── full_preprocessing.py   # Final orchestrated pipeline
│       └── __init__.py
│
└── results/
    ├── cleaned_dataset.csv
    ├── cleaned_dataset.xlsx
    └── (generated plots…)
```

---

# 🎯 Project Goals  

### ✔ Clean real-world messy dataset  
- Missing values  
- Duplicates  
- Incorrect types  
- Corrupted numeric fields (“free”, “twenty”, “NaN”, etc.)  
- Incorrect city/region combinations  
- Inconsistent dates  

### ✔ Generate a full profiling report  
- Type inference  
- Numeric anomalies  
- Inconsistent text  
- Date validity  
- Suspicious values  

### ✔ Build reusable cleaning modules  
Each cleaning function supports **test_mode=True** for debugging and transparency.

### ✔ Provide complete analysis  
- Statistical metrics  
- Regional KPIs  
- Product KPIs  
- Time-series revenue analysis  

### ✔ Export the final cleaned dataset  
The pipeline auto-detects the file format and exports with the same name plus `_cleaned`.

---

# 🧩 Pipeline Overview  

## **1️⃣ Loading & Inspection**  
- Load CSV, Excel, or JSON  
- Display shape, info(), head()  
- Column types overview  
- Basic validation rules  

## **2️⃣ Profiling**  
- Invalid dates  
- Numeric coercion test  
- Text inconsistencies  
- Value distribution and uniqueness  
- Outlier detection preview  
- Structural inspection (df.describe(include="all"))  

## **3️⃣ Cleaning**  
Includes modules for:  

✔ Missing values  
✔ Duplicate removal  
✔ Numeric type fixing  
✔ Number-words conversion  
✔ Free text → 0 replacement  
✔ City & region harmonization  
✔ Completing missing `quantity`, `unit_price`, `total_amount` using rules  
✔ Detect & mark outliers (IQR)  

Every function includes:  
```python
test_mode=True  # prints before/after preview
```

## **4️⃣ Feature Engineering**  
- Year, month, day  
- Weekday  
- Revenue aggregates  
- Order size metrics  

## **5️⃣ Analysis**  
- Descriptive statistics  
- KPI per region and per category  
- Top products  
- Time series (monthly revenue & AOV)  
- Trend visualization (Matplotlib)  

---

# 🚀 How to Run the Full Pipeline  

### **Option A — Use the Jupyter Notebook**  
Open:

```
notebooks/pipeline_notebook.ipynb
```

and run all cells.

### **Option B — Run the full pipeline script**

```python
from preprocessing.pipeline.full_preprocessing import full_preprocessing

cleaned_df = full_preprocessing("data/morocco_ecommerce.xlsx")
```

This automatically:

✔ Loads  
✔ Profiles  
✔ Cleans  
✔ Generates features  
✔ Performs analysis  
✔ Saves cleaned file in `/results/`

---

# 📤 Export of Cleaned Data  
At the end of the pipeline, the script auto-detects your file type:

| Input Format | Output Format |
|--------------|----------------|
| `.csv`       | `*_cleaned.csv` |
| `.xlsx`      | `*_cleaned.xlsx` |
| `.json`      | `*_cleaned.json` |

Example:

```
data/morocco_ecommerce.xlsx → results/morocco_ecommerce_cleaned.xlsx
```

---

# 🧪 Test Mode (Debugging)  

Nearly all functions include:

```python
test_mode=True
```

which prints:

- Before cleaning  
- After cleaning  
- Found invalid values  
- Replacements  
- Statistics & checks  

Example:

```python
df = clean_numeric_column(df, "unit_price", test_mode=True)
```

---

# 🖼 Visual Outputs  

Generated plots include:

- 📈 Monthly revenue trend  
- 🧮 KPI summary tables  
- 🗺 Revenue by region  
- 🛒 Top product revenue  

Saved automatically in:  
```
results/
```

---

# 📌 Requirements  

- Python 3.10+
- pandas
- numpy
- matplotlib
- openpyxl (for Excel export)
- Jupyter Notebook / VS Code

Install:

```bash
pip install pandas numpy matplotlib openpyxl
```

---

# 🏁 Conclusion  

This project gives you:

✨ A **complete, modular, reusable** data cleaning and analysis framework  
✨ Industrial-level structure with **separated concerns**  
✨ Debugging-friendly functions with `test_mode`  
✨ A final notebook for storytelling and exploration  
✨ A pipeline you can extend for larger datasets or ML tasks  
