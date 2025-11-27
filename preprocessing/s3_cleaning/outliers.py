#(Q26–Q28)
import numpy as np
from scipy.stats import zscore



def detect_outliers_iqr(df, column='total_amount'):

    # Calcul des quartiles
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    # Bornes
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Détection
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

    # Résultat rangé proprement
    return {
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'outliers': outliers
    }

def detect_outliers_zscore(df, column='total_amount', threshold=3):

    # Calcul du z-score
    df['zscore_' + column] = zscore(df[column])

    # Détection
    outliers = df[df['zscore_' + column].abs() > threshold]

    return outliers


def mark_outliers_iqr(df, column, test_mode=False):
    """
    Détecte les outliers via la méthode IQR, ajoute une colonne booléenne indiquant
    si une ligne est un outlier, et retourne les bornes.

    Parameters:
        df (DataFrame): le dataset
        column (str): colonne numérique à analyser
        test_mode (bool): si True, affiche les résultats détaillés

    Returns:
        df (DataFrame): avec une nouvelle colonne is_outlier_<column>_iqr
        result (dict): bornes IQR avec Q1, Q3, IQR, lower_bound, upper_bound
    """

    # 1️⃣ Détection IQR
    result = detect_outliers_iqr(df, column=column)
    lower = result["lower_bound"]
    upper = result["upper_bound"]

    # 2️⃣ Création du nom de colonne
    outlier_col = f"is_outlier_{column}_iqr"

    # 3️⃣ Marquage des outliers
    df[outlier_col] = df[column].apply(lambda x: x < lower or x > upper)

    # 4️⃣ Test Mode Output
    if test_mode:
        print("\n========== [TEST MODE] mark_outliers_iqr() ==========")
        print(f"Column analyzed : {column}")
        print(f"Lower bound     : {lower}")
        print(f"Upper bound     : {upper}")

        nb = df[outlier_col].sum()
        print(f"\nNumber of outliers detected : {nb}")

        if nb > 0:
            print("\nExample outliers (first 10):")
            print(df[df[outlier_col]].head(10))
        else:
            print("\nNo outliers detected.")

        print("\nPreview of column with flag :")
        print(df[[column, outlier_col]].head(10))
        print("======================================================")

    return df
