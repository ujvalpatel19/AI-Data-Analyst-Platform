import pandas as pd
import numpy as np

def fill_missing_values(df, strategy="auto", custom_strategies=None):
    """
    Fills missing values in dataframe based on strategy.
    strategy: 'auto', 'mean_median', 'drop', 'zero'
    custom_strategies: dict mapping column_name -> strategy ('mean', 'median', 'mode', 'drop', 'zero', 'custom_val')
    """
    cleaned_df = df.copy()
    
    if custom_strategies:
        for col, strat in custom_strategies.items():
            if col not in cleaned_df.columns:
                continue
            if strat == 'mean' and pd.api.types.is_numeric_dtype(cleaned_df[col]):
                cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mean())
            elif strat == 'median' and pd.api.types.is_numeric_dtype(cleaned_df[col]):
                cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
            elif strat == 'mode':
                mode_val = cleaned_df[col].mode()
                if not mode_val.empty:
                    cleaned_df[col] = cleaned_df[col].fillna(mode_val[0])
            elif strat == 'zero':
                cleaned_df[col] = cleaned_df[col].fillna(0)
            elif strat == 'drop':
                cleaned_df = cleaned_df.dropna(subset=[col])
    else:
        for col in cleaned_df.columns:
            if cleaned_df[col].isnull().sum() > 0:
                if pd.api.types.is_numeric_dtype(cleaned_df[col]):
                    cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
                else:
                    mode_val = cleaned_df[col].mode()
                    if not mode_val.empty:
                        cleaned_df[col] = cleaned_df[col].fillna(mode_val[0])
                    else:
                        cleaned_df[col] = cleaned_df[col].fillna("Unknown")

    return cleaned_df

def remove_duplicates(df):
    """Removes duplicate rows from dataframe."""
    return df.drop_duplicates().reset_index(drop=True)

def drop_columns(df, columns_to_drop):
    """Drops specified columns."""
    return df.drop(columns=[col for col in columns_to_drop if col in df.columns])

def convert_column_types(df, conversions):
    """
    conversions: dict mapping col_name -> target_type ('numeric', 'datetime', 'string', 'categorical')
    """
    cleaned_df = df.copy()
    for col, target_type in conversions.items():
        if col not in cleaned_df.columns:
            continue
        try:
            if target_type == 'numeric':
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
            elif target_type == 'datetime':
                cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
            elif target_type == 'string':
                cleaned_df[col] = cleaned_df[col].astype(str)
            elif target_type == 'categorical':
                cleaned_df[col] = cleaned_df[col].astype('category')
        except Exception:
            pass
    return cleaned_df

def handle_outliers_iqr(df, col, factor=1.5):
    """Caps numerical outliers using the 1.5 * IQR rule."""
    cleaned_df = df.copy()
    if pd.api.types.is_numeric_dtype(cleaned_df[col]):
        Q1 = cleaned_df[col].quantile(0.25)
        Q3 = cleaned_df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR
        cleaned_df[col] = np.where(cleaned_df[col] < lower_bound, lower_bound, cleaned_df[col])
        cleaned_df[col] = np.where(cleaned_df[col] > upper_bound, upper_bound, cleaned_df[col])
    return cleaned_df

def get_cleaning_summary(original_df, cleaned_df):
    """Returns dictionary comparing original vs cleaned dataframe stats."""
    return {
        "original_rows": len(original_df),
        "cleaned_rows": len(cleaned_df),
        "rows_removed": len(original_df) - len(cleaned_df),
        "original_nulls": int(original_df.isnull().sum().sum()),
        "cleaned_nulls": int(cleaned_df.isnull().sum().sum()),
        "nulls_fixed": int(original_df.isnull().sum().sum()) - int(cleaned_df.isnull().sum().sum()),
        "original_duplicates": int(original_df.duplicated().sum()),
        "cleaned_duplicates": int(cleaned_df.duplicated().sum()),
    }
