import pandas as pd

# --- Import your preprocessing modules ---

# 1) Loading
from ..s1_loading.loading import (
    load_data,
)

# 2) Profiling (if needed before cleaning)
from ..s2_profiling.profiling import (
    generate_profiling_report,
)

# 3) Cleaning
from ..s3_cleaning.missing_values import (
    count_missing,
    column_with_most_missing,
    count_city_unknown,
    drop_missing_rows,
    fill_missing_dates,
    fill_city_unknown,
    count_unit_price_missing,
    fill_unit_price_mean,
    complete_amounts,
    fix_region_with_city,
)

from ..s3_cleaning.type_fixing import (
    convert_to_float,
    convert_to_type,
    convert_number_words_to_numeric,
    detect_unusual_values,
    clean_numeric_column,
)

from ..s3_cleaning.duplicates import (
    count_duplicates,
    drop_duplicates_all,
    drop_duplicates_order_id,
)

from ..s3_cleaning.string_cleaning import (
    clean_city_format,
    replace_casa_variants,
    replace_nan_columns_by_words,
    standardize_case,
    clean_city_column,
    clean_region_column
)
from ..s3_cleaning.date_cleaning import (
    normalize_date,
)
from ..s3_cleaning.outliers import (
    detect_outliers_iqr, 
    detect_outliers_zscore,
    mark_outliers_iqr,
)

# 4) Features
from ..s4_features.date_features import (
    add_date_variables,
    add_date_features,
    convert_dates,
    filter_after_date,
)
from ..s4_features.feature_engineering import (
    apply_discount,
)
# 5) Analysis
from ..s5_analysis.filtering import (
    filter_quantity_gt_3,
    filter_total_amount_gt_1000,
    filter_region_casa_settat,
    filter_not_cash,
)

from ..s5_analysis.descriptive_stats import (
    summarize_total_amount,
    region_highest_average_total,
    product_highest_revenue,
)
from ..s5_analysis.grouped_kpis import (
    average_monthly_revenue,
    top_n_largest_orders,
    compute_grouped_kpis,
)
from ..s5_analysis.time_series import (
    analyze_time_series,
)

# ---------------------------------------------------------------------
# 🔥 MASTER PIPELINE FUNCTION — runs all Q1–Q28 steps
# ---------------------------------------------------------------------
def full_preprocessing(path):

    """
    Runs the entire preprocessing workflow:
    - Q1–Q4: load data + basic inspection
    - Q5–Q9: missing values
    - Q10–Q12: duplicates
    - Q13–Q16: filtering examples
    - Q17–Q19: descriptive statistics
    - Q20–Q21: string cleaning
    - Q22–Q25: datetime processing
    - Q26–Q28: outlier detection

    Returns:
        cleaned DataFrame
    """
  

    print("\n--- Loading Data (Q1–Q4) ---")
    df = load_data(path)
  
    # --------------------------
    # Missing Values (Q5–Q9)
    # --------------------------
    print("\n--- Handling Missing Values (Q5–Q9) ---")
    print(count_missing(df))
    print("Column with most missing:", column_with_most_missing(df))

    if count_city_unknown(df) > 0:
        print("Filling missing city values with 'Unknown'")
    else:
        print("No missing city values to fill")
    df = fill_city_unknown(df)
    if count_unit_price_missing(df) > 0:
        print("Filling missing unit_price values with mean")
    else:
        print("No missing unit_price values to fill")
    df = fill_unit_price_mean(df)

    # do NOT drop rows in pipeline unless required
    print("Dropping rows with ANY missing values")
    df = drop_missing_rows(df)
    print("Missing values after cleaning:\n", count_missing(df),df.shape)
    # --------------------------
    # Duplicates (Q10–Q12)
    # --------------------------
    print("\n--- Handling Duplicates (Q10–Q12) ---")
    print("Duplicate count:", count_duplicates(df))
    if count_duplicates(df) > 0:
        df = drop_duplicates_all(df)
        df = drop_duplicates_order_id(df)
        print("Dropping all duplicate rows")
    
    #- -------------------------
    # Filtering (Q13–Q16)
    # --------------------------
    print("\n--- Filtering Examples (Q13–Q16) ---")
    print("Filtering quantity > 3",filter_quantity_gt_3(df))
    print("Filtering total_amount > 1000",filter_total_amount_gt_1000(df))      
    print("Filtering region Casablanca-Settat",filter_region_casa_settat(df))
    print("Filtering payment_method not Cash",filter_not_cash(df))

    # --------------------------
    # Descriptive Statistics (Q17–Q19)
    # --------------------------
    print("\n--- Descriptive Statistics (Q17–Q19) ---")
    print("Total amount summary:", summarize_total_amount(df))
    print("Region with highest average total_amount:", region_highest_average_total(df))
    print("Product with highest revenue:", product_highest_revenue(df))


    # --------------------------
    # String Cleaning (Q20–Q21)
    # --------------------------
    print("\n--- Cleaning String Columns (Q20–Q21) ---")
    print("Cleaning city format and replacing Casa variants") 
    print("checking city before cleaning:", df["city"].unique())
    df = clean_city_format(df)
    df = replace_casa_variants(df)
    print("checking city after cleaning:", df["city"].unique())

    # --------------------------
    # Datetime (Q22–Q25)
    # --------------------------
    print("\n--- Handling Dates (Q22–Q25) ---")
    print("checking order_date dtype before conversion:", df["order_date"].dtype)
    df = convert_dates(df)
    print("checking order_date dtype after conversion:", df["order_date"].dtype)
    print("Adding date features: year, month, weekday")
    df = add_date_features(df)
    print("displaying first 5 rows with new date features:")
    print(df[["order_date", "year", "month", "weekday"]].head())
    print("filtering orders after 2022-01-01")
    df = filter_after_date(df, "2022-01-01")
    print("Average monthly revenue:")
    print(average_monthly_revenue(df))

    # --------------------------
    # Outliers (Q26–Q28)
    # --------------------------
    print("\n--- Detecting Outliers (Q26–Q28) ---")
    print("Outliers detected by IQR method:")
    detect_outliers_iqr(df)
    print("Outliers detected by Z-score method:")
    detect_outliers_zscore(df)
    print("Top 5 largest orders by total_amount:")
    print(top_n_largest_orders(df,"order_id","total_amount",5))

    # print("\n--- PIPELINE COMPLETE ---\n")

    return df
