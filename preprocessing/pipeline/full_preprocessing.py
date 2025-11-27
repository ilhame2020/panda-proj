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
    Full preprocessing pipeline supporting:
    - Q1–Q28 steps
    - PDF project sections 1–11
    """

    # ----------------------------
    # 1. LOAD DATA
    # ----------------------------
    df = load_data(path)

    # ----------------------------
    # 2. PROFILING (PDF: Section 2–5)
    # ----------------------------
   # generate_profiling_report(df)


    # ----------------------------
    # 3. TYPE FIXING (PDF 11–15)
    # ----------------------------
    df = clean_numeric_column(df, "quantity",True)
    df.loc[df["order_id"]=="ORD000309"]
    df = clean_numeric_column(df, "unit_price",True)
    df=convert_to_type(df,["order_id","customer_id","product_category","product_id","discount_code","order_status","payment_method","total_amount"]
                     , ["string","string","string","string","string","string","string","numerique"])

    # generate_profiling_report(df)

    # ----------------------------
    # 4. TEXT CLEANING (PDF 16–20 + Q20–Q21)
    # ----------------------------

    df= clean_city_column(df, "city", test_mode=True)
    df= clean_region_column(df, "region", test_mode=True)
    df= standardize_case(df,["product_category","payment_method","city","region"])

    # ----------------------------
    # 5. MISSING VALUES (Q5–Q9 + PDF recommendations)
    # ----------------------------
    df=complete_amounts(df, test_mode=True)
    df=clean_region_column(df, "region", test_mode=True)
    df=clean_city_column(df, "city", test_mode=True)
    df=fix_region_with_city(df)
    df = fill_missing_dates(df, ["order_date","ship_date"])
    df=replace_nan_columns_by_words(df,["discount_code","region","city"],["No code","Unknown","Unknown"])


    # df = fill_city_unknown(df)
    # df = fill_unit_price_mean(df)
    # df = drop_missing_rows(df)

    # ----------------------------
    # 6. DATE CLEANING (PDF 21–25 + Q22–Q25)
    # ----------------------------

    df.loc[df["order_id"]=="ORD004306"]
    df=normalize_date(df, "order_date", test_mode=True)
    df=normalize_date(df, "ship_date", test_mode=True)
    df.loc[df["order_id"]=="ORD004306"]

    # ----------------------------
    # FEATURE ENGINEERING 
    # ----------------------------
    df=add_date_variables(df)
    discount_mapping = {
    "SALE20": 0.2,       # 20% de remise
    "FREESHIP": 0.0,     # gratuité livraison → pas de remise sur le prix
    "WELCOME": 0.1,      # 10% de remise
    "No code": 0.0,      # pas de remise
    "AYD10": 0.1,        # 10% de remise
    "RAMADAN10": 0.1     # 10% de remise
    }
    df = apply_discount(df, discount_mapping)


    # ----------------------------
    # 7. DUPLICATES (Q10–Q12 + PDF 26–30)
    # ----------------------------
    df = drop_duplicates_all(df)
    df = drop_duplicates_order_id(df)

    # ----------------------------
    # 8. OUTLIERS (PDF 31–35 + Q26–Q28)
    # ----------------------------
    detect_outliers_iqr(df,'total_amount')
    detect_outliers_zscore(df,'total_amount',3)
    df=mark_outliers_iqr(df,'total_amount', test_mode=True)
    # ----------------------------
    # STATISTICAL ANALYSIS 
    # ----------------------------
    stats = summarize_total_amount(df)

    print("\n📊 Total Amount Statistics:")
    print(f"- Mean   : {stats['mean']:.2f}")
    print(f"- Median : {stats['median']:.2f}")
    print(f"- Min    : {stats['min']:.2f}")
    print(f"- Max    : {stats['max']:.2f}")


    # ----------------------------
    # 10. GROUPED KPIs (PDF 41–45)
    # ----------------------------
    results = compute_grouped_kpis(df)

    print("Total Amount Statistics:\n", results["total_amount_stats"])
    print("\nRegional Analysis:\n", results["region_analysis"])
    print("\nCategory Analysis:\n", results["category_analysis"])
    print("\nTop 5 Products:\n", results["top_5_products"])


    # ----------------------------
    # 11. TIME SERIES (PDF 46–50)
    # ----------------------------
    results = analyze_time_series(df)

    print(results["monthly_revenue"].head())
    print(results["monthly_aov"].head())
    print("Best month:", results["best_month"])
    print("Revenue:", results["best_month_revenue"])


    return df
