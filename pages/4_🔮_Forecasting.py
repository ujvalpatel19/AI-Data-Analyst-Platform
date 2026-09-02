import streamlit as st
import pandas as pd
import numpy as np
from utils.chart_generator import create_forecast_chart, create_line_chart
from utils.components.sidebar import render_sidebar
from utils.components.header import render_header

st.set_page_config(page_title="Sales Forecasting - AI Data Analyst", page_icon="🔮", layout="wide")

render_sidebar()
render_header(title="Sales Trend Analysis & Forecasting", subtitle="Time-Series Trend Extraction & Predictive Sales Projections")

df = st.session_state.get('cleaned_df')

if df is None or df.empty:
    st.warning("⚠️ No dataset loaded. Please upload a dataset from the sidebar first.")
    st.stop()

date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c]) or 'date' in c.lower() or 'time' in c.lower()]
numeric_cols = list(df.select_dtypes(include=['float64', 'int64']).columns)

if not date_cols or not numeric_cols:
    st.error("Sales forecasting requires at least one Date column and one Numeric target column (e.g. Sales, Revenue).")
    st.stop()

c1, c2, c3 = st.columns(3)
with c1:
    selected_date_col = st.selectbox("Select Date Column", date_cols)
with c2:
    selected_val_col = st.selectbox("Select Target Metric to Forecast", numeric_cols, index=0)
with c3:
    forecast_periods = st.slider("Forecast Days Ahead", min_value=7, max_value=90, value=30)

# Convert date column to datetime if needed
try:
    df_ts = df.copy()
    df_ts[selected_date_col] = pd.to_datetime(df_ts[selected_date_col])
    df_daily = df_ts.groupby(df_ts[selected_date_col].dt.date)[selected_val_col].sum().reset_index()
    df_daily.columns = ['Date', 'Value']
    df_daily['Date'] = pd.to_datetime(df_daily['Date'])
    df_daily = df_daily.sort_values('Date').reset_index(drop=True)
except Exception as e:
    st.error(f"Error processing time-series data: {e}")
    st.stop()

st.markdown("---")
st.subheader("📈 Historical Trend Line")
fig_hist = create_line_chart(df_daily, x_col='Date', y_col='Value', title=f"Historical Daily {selected_val_col}")
st.plotly_chart(fig_hist, use_container_width=True)

# Exponential Smoothing Forecast Logic
st.subheader("🔮 Predictive Sales Forecast")

try:
    from statsmodels.tsa.holtwinters import SimpleExpSmoothing, ExponentialSmoothing
    
    values = df_daily['Value'].values
    if len(values) >= 4:
        # Fit Holt's Linear Trend Model
        model = ExponentialSmoothing(values, trend='add', seasonal=None).fit()
        forecast_vals = model.forecast(forecast_periods)
        
        last_date = df_daily['Date'].max()
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_periods)
        
        # Calculate Confidence Bands (95%)
        std_err = np.std(values[-7:]) if len(values) >= 7 else np.std(values)
        upper_ci = forecast_vals + (1.96 * std_err)
        lower_ci = np.maximum(0, forecast_vals - (1.96 * std_err))

        forecast_df = pd.DataFrame({
            'Date': future_dates,
            'Forecast': forecast_vals,
            'Upper_CI': upper_ci,
            'Lower_CI': lower_ci
        })

        fig_fc = create_forecast_chart(
            df_daily.rename(columns={'Value': selected_val_col}),
            forecast_df,
            date_col='Date',
            value_col=selected_val_col
        )
        st.plotly_chart(fig_fc, use_container_width=True)

        st.markdown("#### Forecast Metrics & Summary")
        col_m1, col_m2, col_m3 = st.columns(3)
        total_projected = forecast_vals.sum()
        avg_daily_projected = forecast_vals.mean()
        last_hist = values[-1]
        pct_diff = ((avg_daily_projected - last_hist) / last_hist * 100) if last_hist != 0 else 0

        col_m1.metric(f"Total Projected {selected_val_col}", f"₹{total_projected:,.2f}")
        col_m2.metric(f"Avg Daily Forecast", f"₹{avg_daily_projected:,.2f}")
        col_m3.metric("Projected Trend vs Recent", f"{pct_diff:+.1f}%")

    else:
        st.warning("Insufficient date records (need at least 4 daily data points) to compute time-series forecast.")

except Exception as e:
    st.error(f"Error computing forecast: {e}")
