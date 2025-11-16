import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from returns_calculator import calculate_aggregated_returns

def plot_cumulative_return(data: pd.DataFrame):
    """
    Plots the cumulative total return vs. price return.
    """
    data['Cumulative_Price_Return'] = (1 + data['Price_Return']).cumprod() - 1
    data['Cumulative_Total_Return'] = (1 + data['Total_Return']).cumprod() - 1

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index, y=data['Cumulative_Price_Return'] * 100,
        mode='lines', name='Price Return Only'
    ))
    fig.add_trace(go.Scatter(
        x=data.index, y=data['Cumulative_Total_Return'] * 100,
        mode='lines', name='Total Return (with Dividends)'
    ))
    fig.update_layout(
        title='Cumulative Return Comparison',
        xaxis_title='Date',
        yaxis_title='Cumulative Return (%)',
        legend_title='Return Type',
        template='plotly_white'
    )
    return fig

def plot_periodic_returns(daily_total_returns: pd.Series):
    """
    Plots bar charts for monthly, quarterly, and yearly returns.
    """
    monthly = calculate_aggregated_returns(daily_total_returns, 'ME') * 100
    quarterly = calculate_aggregated_returns(daily_total_returns, 'QE') * 100
    yearly = calculate_aggregated_returns(daily_total_returns, 'YE') * 100

    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Monthly Returns', 'Quarterly Returns', 'Yearly Returns'),
        vertical_spacing=0.1
    )

    fig.add_trace(go.Bar(
        x=monthly.index, y=monthly, name='Monthly',
        marker_color=['green' if v >= 0 else 'red' for v in monthly]
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=quarterly.index, y=quarterly, name='Quarterly',
        marker_color=['green' if v >= 0 else 'red' for v in quarterly]
    ), row=2, col=1)

    fig.add_trace(go.Bar(
        x=yearly.index, y=yearly, name='Yearly',
        marker_color=['green' if v >= 0 else 'red' for v in yearly]
    ), row=3, col=1)

    fig.update_layout(
        title_text='Periodic Returns',
        height=800,
        showlegend=False,
        template='plotly_white'
    )
    fig.update_yaxes(title_text="Return (%)")
    return fig

def plot_volume_analysis(data: pd.DataFrame):
    """
    Plots a dual-axis chart with price and volume.
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], name="Price"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Bar(x=data.index, y=data['Volume'], name="Volume"),
        secondary_y=True,
    )

    fig.update_layout(
        title_text='Price and Volume Analysis',
        template='plotly_white'
    )
    fig.update_yaxes(title_text="Price", secondary_y=False)
    fig.update_yaxes(title_text="Volume", secondary_y=True)
    return fig

def plot_daily_returns_boxplot(daily_total_returns: pd.Series, period: str):
    """
    Creates a box plot of daily return distribution by a specified time period.
    """
    if period == 'Monthly':
        grouper = daily_total_returns.index.to_period('M')
    elif period == 'Quarterly':
        grouper = daily_total_returns.index.to_period('Q')
    else: # Yearly
        grouper = daily_total_returns.index.to_period('Y')

    fig = go.Figure()
    
    # Group by the specified period and create a box for each group
    for name, group in daily_total_returns.groupby(grouper):
        fig.add_trace(go.Box(
            y=group * 100,
            name=str(name),
            boxpoints='outliers' # Show outliers
        ))

    fig.update_layout(
        title=f'Daily Total Return Distribution by {period}',
        xaxis_title='Period',
        yaxis_title='Daily Total Return (%)',
        template='plotly_white',
        showlegend=False
    )
    return fig

def plot_dividend_timeline(data: pd.DataFrame):
    """
    Plots a scatter/bar chart of dividend payments over time.
    """
    dividends = data[data['Dividends'] > 0]
    if dividends.empty:
        fig = go.Figure()
        fig.update_layout(title="No dividends were paid in this period.")
        return fig

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dividends.index,
        y=dividends['Dividends'],
        name='Dividend Amount'
    ))
    fig.update_layout(
        title='Dividend Payment Timeline',
        xaxis_title='Ex-Dividend Date',
        yaxis_title='Dividend per Share ($)',
        template='plotly_white'
    )
    return fig
