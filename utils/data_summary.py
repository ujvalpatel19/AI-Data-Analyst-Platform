import pandas as pd
import numpy as np

def get_dataset_info(df):
    """Returns basic dataset dimensions and memory usage."""
    if df is None or df.empty:
        return {}
    
    memory_usage = df.memory_usage(deep=True).sum() / (1024 * 1024)  # MB
    num_rows, num_cols = df.shape
    num_numeric = len(df.select_dtypes(include=[np.number]).columns)
    num_categorical = len(df.select_dtypes(include=['object', 'category']).columns)
    num_datetime = len(df.select_dtypes(include=['datetime64', 'datetime']).columns)
    total_cells = num_rows * num_cols
    total_nulls = df.isnull().sum().sum()
    null_percentage = (total_nulls / total_cells * 100) if total_cells > 0 else 0
    duplicate_rows = df.duplicated().sum()

    return {
        "rows": num_rows,
        "cols": num_cols,
        "memory_mb": round(memory_usage, 2),
        "numeric_cols": num_numeric,
        "categorical_cols": num_categorical,
        "datetime_cols": num_datetime,
        "total_nulls": int(total_nulls),
        "null_percentage": round(null_percentage, 2),
        "duplicate_rows": int(duplicate_rows),
    }

def get_column_types(df):
    """Categorizes dataframe columns into numerical, categorical, and datetime."""
    numeric_cols = list(df.select_dtypes(include=[np.number]).columns)
    categorical_cols = list(df.select_dtypes(include=['object', 'category', 'bool']).columns)
    datetime_cols = list(df.select_dtypes(include=['datetime64', 'datetime']).columns)
    
    return {
        "numeric": numeric_cols,
        "categorical": categorical_cols,
        "datetime": datetime_cols
    }

def get_missing_summary(df):
    """Returns missing values breakdown per column."""
    missing_data = []
    total_rows = len(df)
    
    for col in df.columns:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            missing_data.append({
                "Column": col,
                "Missing Values": int(null_count),
                "Missing Percentage": round((null_count / total_rows) * 100, 2),
                "Data Type": str(df[col].dtype)
            })
            
    summary_df = pd.DataFrame(missing_data)
    if not summary_df.empty:
        summary_df = summary_df.sort_values(by="Missing Values", ascending=False)
    return summary_df
