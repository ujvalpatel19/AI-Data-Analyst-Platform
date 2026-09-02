import streamlit as st
import pandas as pd
from utils.data_cleaner import fill_missing_values, remove_duplicates, drop_columns, handle_outliers_iqr, get_cleaning_summary
from utils.components.sidebar import render_sidebar
from utils.components.header import render_header

st.set_page_config(page_title="Data Cleaning - AI Data Analyst", page_icon="🧹", layout="wide")

render_sidebar()
render_header(title="Data Cleaning Studio", subtitle="Detect, Fix & Sanitize Missing Data, Duplicates & Outliers")

df = st.session_state.get('cleaned_df')
orig_df = st.session_state.get('df')

if df is None or df.empty:
    st.warning("⚠️ No dataset loaded. Please upload a dataset from the sidebar first.")
    st.stop()

st.subheader("🛠️ Interactive Data Cleaning Toolbar")

col_left, col_right = st.columns([2, 1])

with col_left:
    with st.expander("1. Handle Missing Values", expanded=True):
        missing_cols = [c for c in df.columns if df[c].isnull().sum() > 0]
        if not missing_cols:
            st.success("No missing values found in dataset!")
        else:
            st.write(f"Missing values found in columns: `{', '.join(missing_cols)}`")
            strategy = st.selectbox("Imputation Strategy", ["Auto (Numeric: Median, Text: Mode)", "Fill with Zeros / Unknown", "Drop rows with missing values"])
            if st.button("Apply Missing Value Fix"):
                if strategy.startswith("Auto"):
                    df = fill_missing_values(df, strategy="auto")
                elif strategy.startswith("Fill"):
                    df = fill_missing_values(df, strategy="zero")
                else:
                    df = df.dropna().reset_index(drop=True)
                st.session_state['cleaned_df'] = df
                st.success("Missing values fixed!")
                st.rerun()

    with st.expander("2. Remove Duplicate Rows", expanded=False):
        dups = df.duplicated().sum()
        st.write(f"Current duplicate row count: **{dups}**")
        if dups > 0:
            if st.button("Remove All Duplicates"):
                df = remove_duplicates(df)
                st.session_state['cleaned_df'] = df
                st.success(f"Removed {dups} duplicate rows!")
                st.rerun()

    with st.expander("3. Outlier Handling (IQR Capping)", expanded=False):
        num_cols = list(df.select_dtypes(include=['float64', 'int64']).columns)
        if num_cols:
            selected_num_col = st.selectbox("Select numeric column to cap outliers", num_cols)
            if st.button("Cap Outliers via 1.5x IQR"):
                df = handle_outliers_iqr(df, selected_num_col)
                st.session_state['cleaned_df'] = df
                st.success(f"Outliers capped for '{selected_num_col}'!")
                st.rerun()

    with st.expander("4. Drop Unnecessary Columns", expanded=False):
        cols_to_drop = st.multiselect("Select columns to remove", df.columns)
        if cols_to_drop and st.button("Drop Selected Columns"):
            df = drop_columns(df, cols_to_drop)
            st.session_state['cleaned_df'] = df
            st.success(f"Dropped columns: {cols_to_drop}")
            st.rerun()

with col_right:
    st.subheader("📊 Cleaning Summary")
    summary = get_cleaning_summary(orig_df, df)
    st.json(summary)

    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Cleaned CSV",
        data=csv_data,
        file_name="cleaned_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

st.markdown("---")
st.subheader("Preview Cleaned Dataset")
st.dataframe(df.head(20), use_container_width=True)
