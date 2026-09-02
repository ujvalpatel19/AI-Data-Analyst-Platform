import pandas as pd
import numpy as np

def get_numeric_stats(df):
    """Generates detailed summary statistics for numeric columns."""
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return pd.DataFrame()

    stats = numeric_df.describe().T
    stats['skewness'] = numeric_df.skew()
    stats['kurtosis'] = numeric_df.kurtosis()
    stats['median'] = numeric_df.median()
    stats = stats.round(2)
    return stats

def get_categorical_stats(df, max_categories=10):
    """Generates summary statistics for categorical columns."""
    cat_df = df.select_dtypes(include=['object', 'category', 'bool'])
    if cat_df.empty:
        return {}

    summary = {}
    for col in cat_df.columns:
        counts = cat_df[col].value_counts().head(max_categories)
        percentages = (cat_df[col].value_counts(normalize=True).head(max_categories) * 100).round(2)
        top_df = pd.DataFrame({'Count': counts, 'Percentage (%)': percentages})
        summary[col] = {
            "unique_count": cat_df[col].nunique(),
            "top_value": cat_df[col].mode()[0] if not cat_df[col].mode().empty else "N/A",
            "distribution": top_df
        }
    return summary

def get_correlation_matrix(df):
    """Calculates Pearson correlation matrix for numeric columns."""
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] < 2:
        return None
    return numeric_df.corr().round(3)
