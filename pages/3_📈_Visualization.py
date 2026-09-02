import streamlit as st
import pandas as pd
from utils.chart_generator import (
    create_line_chart, create_bar_chart, create_scatter_chart, 
    create_box_plot, create_histogram, create_pie_chart, create_correlation_heatmap
)
from utils.statistics import get_correlation_matrix
from utils.components.sidebar import render_sidebar
from utils.components.header import render_header

st.set_page_config(page_title="Visualizations - AI Data Analyst", page_icon="📈", layout="wide")

render_sidebar()
render_header(title="Advanced Visualization Studio", subtitle="Dynamic Plotly Interactive Charts & Relationship Exploration")

df = st.session_state.get('cleaned_df')

if df is None or df.empty:
    st.warning("⚠️ No dataset loaded. Please upload a dataset from the sidebar first.")
    st.stop()

# Controls Panel
st.subheader("🎨 Custom Chart Builder")

col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns(4)

numeric_cols = list(df.select_dtypes(include=['float64', 'int64']).columns)
all_cols = list(df.columns)
cat_cols = list(df.select_dtypes(include=['object', 'category']).columns)

with col_ctrl1:
    chart_type = st.selectbox(
        "Chart Type",
        ["Line Chart", "Bar Chart", "Scatter Plot", "Box Plot", "Histogram", "Pie / Donut Chart", "Correlation Heatmap"]
    )

with col_ctrl2:
    if chart_type in ["Line Chart", "Bar Chart", "Scatter Plot"]:
        x_axis = st.selectbox("X-Axis", all_cols, index=0)
    elif chart_type in ["Box Plot", "Histogram"]:
        x_axis = st.selectbox("Group By (Optional)", [None] + cat_cols)
    else:
        x_axis = None

with col_ctrl3:
    if chart_type in ["Line Chart", "Bar Chart", "Scatter Plot", "Box Plot"]:
        y_axis = st.selectbox("Y-Axis", numeric_cols, index=0 if numeric_cols else None)
    elif chart_type == "Histogram":
        y_axis = st.selectbox("Target Column", numeric_cols, index=0 if numeric_cols else None)
    elif chart_type == "Pie / Donut Chart":
        y_axis = st.selectbox("Values Column", numeric_cols, index=0 if numeric_cols else None)
    else:
        y_axis = None

with col_ctrl4:
    if chart_type in ["Line Chart", "Bar Chart", "Scatter Plot"]:
        color_group = st.selectbox("Color / Legend Group", [None] + cat_cols)
    elif chart_type == "Pie / Donut Chart":
        color_group = st.selectbox("Category Names Column", cat_cols, index=0 if cat_cols else None)
    else:
        color_group = None

st.markdown("---")

# Render Chart
fig = None

if chart_type == "Line Chart" and x_axis and y_axis:
    fig = create_line_chart(df, x_col=x_axis, y_col=y_axis, color_col=color_group)
elif chart_type == "Bar Chart" and x_axis and y_axis:
    fig = create_bar_chart(df, x_col=x_axis, y_col=y_axis, color_col=color_group)
elif chart_type == "Scatter Plot" and x_axis and y_axis:
    fig = create_scatter_chart(df, x_col=x_axis, y_col=y_axis, color_col=color_group)
elif chart_type == "Box Plot" and y_axis:
    fig = create_box_plot(df, y_col=y_axis, x_col=x_axis)
elif chart_type == "Histogram" and y_axis:
    fig = create_histogram(df, col=y_axis)
elif chart_type == "Pie / Donut Chart" and color_group and y_axis:
    grouped = df.groupby(color_group)[y_axis].sum().reset_index()
    fig = create_pie_chart(grouped, names_col=color_group, values_col=y_axis)
elif chart_type == "Correlation Heatmap":
    corr_df = get_correlation_matrix(df)
    if corr_df is not None:
        fig = create_correlation_heatmap(corr_df)
    else:
        st.warning("Need at least 2 numeric columns for correlation heatmap.")

if fig is not None:
    st.plotly_chart(fig, use_container_width=True)
