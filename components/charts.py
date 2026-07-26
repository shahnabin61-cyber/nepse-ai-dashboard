# components/charts.py
# Concept: Visualization Layer using Plotly
# Plotly makes INTERACTIVE charts — user can zoom, hover, click!

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_stock_prices(df):
    """Bar chart of stock prices"""
    # Color green if positive change, red if negative
    df['color'] = df['change'].apply(lambda x: 'green' if x >= 0 else 'red')

    fig = px.bar(
        df,
        x='symbol',
        y='ltp',
        color='color',
        color_discrete_map={'green': '#00C853', 'red': '#FF1744'},
        title='NEPSE Stock Prices Today',
        labels={'ltp': 'Last Traded Price (NPR)', 'symbol': 'Stock'}
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig

def plot_gainers_losers(df):
    """Show top gainers and losers"""
    df_sorted = df.sort_values('percentChange', ascending=True)

    fig = px.bar(
        df_sorted,
        x='percentChange',
        y='symbol',
        orientation='h',
        color='percentChange',
        color_continuous_scale=['#FF1744', '#ffffff', '#00C853'],
        title='Top Gainers & Losers (%)',
        labels={'percentChange': 'Change %', 'symbol': 'Stock'}
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig

def plot_volume(df):
    """Volume traded per stock"""
    fig = px.pie(
        df,
        values='volume',
        names='symbol',
        title='Trading Volume Distribution',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    return fig