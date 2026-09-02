import numpy as np
import pandas as pd

def calculate_health_score(df):
    """
    Computes a Data Quality Health Score (0-100%) based on completeness, 
    uniqueness, type consistency, and outlier presence.
    """
    if df is None or df.empty:
        return {
            "score": 0,
            "grade": "N/A",
            "completeness": 0,
            "uniqueness": 0,
            "consistency": 0,
            "outliers_score": 0,
            "issues": ["No dataset loaded."]
        }

    total_cells = df.shape[0] * df.shape[1]
    total_nulls = df.isnull().sum().sum()
    
    # 1. Completeness Score (35%)
    completeness = max(0, (1 - (total_nulls / total_cells if total_cells > 0 else 0)) * 100)
    
    # 2. Uniqueness Score (25%)
    dup_rows = df.duplicated().sum()
    uniqueness = max(0, (1 - (dup_rows / len(df) if len(df) > 0 else 0)) * 100)
    
    # 3. Consistency Score (20%)
    # Check if string columns contain mixed numeric/string types
    consistency_penalties = 0
    for col in df.select_dtypes(include=['object']).columns:
        # Check ratio of numeric-like strings
        numeric_convertible = pd.to_numeric(df[col], errors='coerce').notnull().sum()
        if 0 < numeric_convertible < len(df) * 0.8:
            consistency_penalties += 10
            
    consistency = max(0, 100 - consistency_penalties)
    
    # 4. Outliers Score (20%)
    outlier_count = 0
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        if IQR > 0:
            outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
            outlier_count += outliers

    total_numeric_cells = len(df) * max(1, len(numeric_cols))
    outlier_ratio = outlier_count / total_numeric_cells if total_numeric_cells > 0 else 0
    outliers_score = max(0, (1 - outlier_ratio) * 100)
    
    # Weighted Final Score
    final_score = int(round(
        (completeness * 0.35) + 
        (uniqueness * 0.25) + 
        (consistency * 0.20) + 
        (outliers_score * 0.20)
    ))
    
    # Assign Grade
    if final_score >= 90:
        grade = "A (Excellent)"
    elif final_score >= 75:
        grade = "B (Good)"
    elif final_score >= 60:
        grade = "C (Fair)"
    elif final_score >= 45:
        grade = "D (Poor)"
    else:
        grade = "F (Critical)"

    # Identify Key Issues
    issues = []
    if total_nulls > 0:
        issues.append(f"Found {total_nulls} missing values across columns.")
    if dup_rows > 0:
        issues.append(f"Found {dup_rows} duplicate rows in the dataset.")
    if outlier_count > 0:
        issues.append(f"Detected {outlier_count} statistical outlier values in numeric fields.")
    if consistency_penalties > 0:
        issues.append("Detected potential mixed data types in categorical text columns.")
    if not issues:
        issues.append("No critical data quality issues detected. Dataset is clean!")

    return {
        "score": final_score,
        "grade": grade,
        "completeness": round(completeness, 1),
        "uniqueness": round(uniqueness, 1),
        "consistency": round(consistency, 1),
        "outliers_score": round(outliers_score, 1),
        "issues": issues
    }
