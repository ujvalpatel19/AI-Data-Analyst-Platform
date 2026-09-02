import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Modern sleek color palettes
DARK_TEMPLATE = "plotly_dark"
THEME_COLORS = ["#6366F1", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#3B82F6", "#14B8A6"]

def create_line_chart(df, x_col, y_col, color_col=None, title=None):
    """Generates a modern Plotly line chart."""
    fig = px.line(
        df, x=x_col, y=y_col, color=color_col,
        title=title or f"{y_col} over {x_col}",
        color_discrete_sequence=THEME_COLORS,
        template=DARK_TEMPLATE
    )
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20), hovermode="x unified")
    return fig

def create_bar_chart(df, x_col, y_col, color_col=None, barmode="group", title=None):
    """Generates a modern Plotly bar chart."""
    fig = px.bar(
        df, x=x_col, y=y_col, color=color_col, barmode=barmode,
        title=title or f"{y_col} by {x_col}",
        color_discrete_sequence=THEME_COLORS,
        template=DARK_TEMPLATE
    )
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_scatter_chart(df, x_col, y_col, color_col=None, size_col=None, title=None):
    """Generates an interactive scatter plot with optional trendlines."""
    fig = px.scatter(
        df, x=x_col, y=y_col, color=color_col, size=size_col,
        title=title or f"Relationship between {x_col} and {y_col}",
        color_discrete_sequence=THEME_COLORS,
        template=DARK_TEMPLATE,
        trendline="ols" if pd.api.types.is_numeric_dtype(df[x_col]) and pd.api.types.is_numeric_dtype(df[y_col]) else None
    )
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_box_plot(df, y_col, x_col=None, title=None):
    """Generates a box plot for outlier detection and distribution comparison."""
    fig = px.box(
        df, x=x_col, y=y_col,
        title=title or f"Distribution of {y_col}" + (f" by {x_col}" if x_col else ""),
        color_discrete_sequence=THEME_COLORS,
        template=DARK_TEMPLATE
    )
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_histogram(df, col, nbins=30, title=None):
    """Generates a histogram with frequency distribution."""
    fig = px.histogram(
        df, x=col, nbins=nbins,
        title=title or f"Frequency Distribution of {col}",
        color_discrete_sequence=THEME_COLORS,
        template=DARK_TEMPLATE
    )
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_pie_chart(df, names_col, values_col, hole=0.4, title=None):
    """Generates a donut / pie chart."""
    fig = px.pie(
        df, names=names_col, values=values_col, hole=hole,
        title=title or f"Share of {values_col} by {names_col}",
        color_discrete_sequence=THEME_COLORS,
        template=DARK_TEMPLATE
    )
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_correlation_heatmap(corr_df):
    """Generates an interactive correlation matrix heatmap."""
    if corr_df is None or corr_df.empty:
        return None
        
    fig = px.imshow(
        corr_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        title="Correlation Heatmap",
        template=DARK_TEMPLATE
    )
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_forecast_chart(historical_df, forecast_df, date_col, value_col):
    """
    Plots historical vs forecasted data with confidence boundaries.
    """
    fig = go.Figure()

    # Historical Line
    fig.add_trace(go.Scatter(
        x=historical_df[date_col],
        y=historical_df[value_col],
        mode='lines+markers',
        name='Historical Sales',
        line=dict(color='#3B82F6', width=3)
    ))

    # Forecast Line
    fig.add_trace(go.Scatter(
        x=forecast_df[date_col],
        y=forecast_df['Forecast'],
        mode='lines+markers',
        name='Forecasted Sales',
        line=dict(color='#10B981', width=3, dash='dash')
    ))

    # Upper and Lower Confidence Bounds
    if 'Upper_CI' in forecast_df.columns and 'Lower_CI' in forecast_df.columns:
        fig.add_trace(go.Scatter(
            x=list(forecast_df[date_col]) + list(forecast_df[date_col])[::-1],
            y=list(forecast_df['Upper_CI']) + list(forecast_df['Lower_CI'])[::-1],
            fill='toself',
            fillcolor='rgba(16, 185, 129, 0.15)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=True,
            name='Confidence Band (95%)'
        ))

    fig.update_layout(
        title=f"Sales Forecast - {value_col} Projections",
        xaxis_title="Date",
        yaxis_title=value_col,
        template=DARK_TEMPLATE,
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def create_powerbi_donut_chart(df, names_col, values_col, title=""):
    """PowerBI style dark donut chart with gold/cyan/blue rings matching reference image."""
    colors = ['#F59E0B', '#3B82F6', '#10B981', '#EC4899', '#8B5CF6']
    fig = px.pie(
        df, names=names_col, values=values_col, hole=0.6,
        title=title, color_discrete_sequence=colors
    )
    fig.update_layout(
        paper_bgcolor='#0D0F12',
        plot_bgcolor='#0D0F12',
        font=dict(color='#F59E0B', family="sans-serif"),
        title=dict(font=dict(size=14, color='#F59E0B')),
        margin=dict(l=10, r=10, t=35, b=10),
        legend=dict(orientation="v", font=dict(color='#94A3B8', size=10)),
        showlegend=True
    )
    fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#0D0F12', width=2)))
    return fig

def create_powerbi_timeline_chart(df, date_col, value_col, title=""):
    """PowerBI style spiky timeline line chart matching reference image."""
    fig = px.line(df, x=date_col, y=value_col, title=title)
    fig.update_traces(line=dict(color='#38BDF8', width=2))
    fig.update_layout(
        paper_bgcolor='#0D0F12',
        plot_bgcolor='#0D0F12',
        font=dict(color='#F59E0B'),
        title=dict(font=dict(size=14, color='#FFFFFF')),
        margin=dict(l=20, r=20, t=35, b=20),
        xaxis=dict(showgrid=True, gridcolor='#1E293B', color='#94A3B8'),
        yaxis=dict(showgrid=True, gridcolor='#1E293B', color='#94A3B8'),
        hovermode="x unified"
    )
    return fig

def create_powerbi_dual_bar_chart(df, cat_col, val1_col, val2_col, title=""):
    """PowerBI style dual quarterly bar chart (Sum of Profit & Sum of Sales)."""
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df[cat_col], y=df[val1_col], name=f"Sum of {val1_col}", marker_color='#3B82F6'))
    fig.add_trace(go.Bar(x=df[cat_col], y=df[val2_col], name=f"Sum of {val2_col}", marker_color='#F59E0B'))
    fig.update_layout(
        barmode='group',
        paper_bgcolor='#0D0F12',
        plot_bgcolor='#0D0F12',
        font=dict(color='#FFFFFF'),
        title=dict(font=dict(size=14, color='#FFFFFF')),
        margin=dict(l=20, r=20, t=35, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#94A3B8')),
        xaxis=dict(showgrid=False, color='#94A3B8'),
        yaxis=dict(showgrid=True, gridcolor='#1E293B', color='#94A3B8')
    )
    return fig


# Cache invalidate trigger
