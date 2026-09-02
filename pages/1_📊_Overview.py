import streamlit as st
import pandas as pd
from utils.data_summary import get_dataset_info, get_column_types, get_missing_summary
from utils.health_score import calculate_health_score
from utils.components.sidebar import render_sidebar
from utils.components.header import render_header

st.set_page_config(page_title="Overview - AI Data Analyst", page_icon="📊", layout="wide")

render_sidebar()
render_header(title="Dataset Overview", subtitle="Exploration, Structure & Data Health Audit")

df = st.session_state.get('cleaned_df')

if df is None or df.empty:
    st.warning("⚠️ No dataset loaded. Please upload a CSV/Excel file from the sidebar.")
    st.stop()

# 1. Top Level Dimension Cards
info = get_dataset_info(df)
health = calculate_health_score(df)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Rows", f"{info.get('rows', 0):,}")
col2.metric("Columns", info.get('cols', 0))
col3.metric("Numeric Cols", info.get('numeric_cols', 0))
col4.metric("Categorical Cols", info.get('categorical_cols', 0))
col5.metric("Health Score", f"{health.get('score', 0)}%", delta=health.get('grade', 'N/A'))

st.markdown("---")

# 2. Interactive Data Viewer & Head/Tail
tab1, tab2, tab3, tab4 = st.tabs(["📋 Raw Dataset Explorer", "🔍 Column Taxonomy", "❓ Missing Values Matrix", "🩺 Data Quality Audit"])

with tab1:
    st.subheader("Interactive Dataset Viewer")
    row_count = st.slider("Rows to preview", min_value=5, max_value=min(500, len(df)), value=20)
    st.dataframe(df.head(row_count), use_container_width=True)

with tab2:
    st.subheader("Column Data Types & Non-Null Counts")
    types_dict = get_column_types(df)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("#### Data Types Summary")
        type_counts = pd.DataFrame([
            {"Type": "Numeric", "Count": len(types_dict['numeric'])},
            {"Type": "Categorical / Text", "Count": len(types_dict['categorical'])},
            {"Type": "Datetime", "Count": len(types_dict['datetime'])},
        ])
        st.dataframe(type_counts, use_container_width=True)

    with col_b:
        st.write("#### Detailed Column Schema")
        schema_df = pd.DataFrame({
            "Column": df.columns,
            "Type": df.dtypes.astype(str),
            "Non-Null Count": df.notnull().sum().values,
            "Null Count": df.isnull().sum().values,
            "Unique Values": [df[c].nunique() for c in df.columns]
        })
        st.dataframe(schema_df, use_container_width=True)

with tab3:
    st.subheader("Missing Values Breakdown")
    missing_df = get_missing_summary(df)
    if missing_df.empty:
        st.success("🎉 No missing values detected in any column!")
    else:
        st.dataframe(missing_df, use_container_width=True)

with tab4:
    st.subheader("Data Health Score Audit")
    st.markdown(f"### Overall Health Grade: **{health['grade']}**")

    c1, c2, c3, c4 = st.columns(4)
    c1.progress(health['completeness'] / 100, text=f"Completeness: {health['completeness']}%")
    c2.progress(health['uniqueness'] / 100, text=f"Uniqueness: {health['uniqueness']}%")
    c3.progress(health['consistency'] / 100, text=f"Consistency: {health['consistency']}%")
    c4.progress(health['outliers_score'] / 100, text=f"Outlier Rating: {health['outliers_score']}%")

    st.markdown("#### Detected Data Quality Issues:")
    for issue in health['issues']:
        st.info(f"• {issue}")
