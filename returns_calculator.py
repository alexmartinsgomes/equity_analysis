import pandas as pd
import numpy as np

def calculate_daily_total_return(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates daily total returns, including price appreciation and dividends.

    Args:
        data (pd.DataFrame): DataFrame with 'Close', 'Dividends' columns.

    Returns:
        pd.DataFrame: Original DataFrame with 'Price_Return' and 'Total_Return' columns.
    """
    data['Price_Return'] = data['Close'].pct_change()
    data['Dividend_Yield'] = data['Dividends'] / data['Close'].shift(1)
    data['Total_Return'] = data['Price_Return'] + data['Dividend_Yield'].fillna(0)
    return data

def calculate_aggregated_returns(daily_returns: pd.Series, period: str) -> pd.Series:
    """
    Calculates aggregated (compounded) returns for a given period.

    Args:
        daily_returns (pd.Series): A Series of daily total returns.
        period (str): 'ME' for monthly, 'QE' for quarterly, 'YE' for yearly.

    Returns:
        pd.Series: A Series of aggregated returns for the specified period.
    """
    return daily_returns.resample(period).apply(lambda x: (1 + x).prod() - 1)

def calculate_performance_metrics(daily_returns: pd.Series, risk_free_rate: float = 0.0) -> dict:
    """
    Calculates key performance metrics from daily total returns.

    Args:
        daily_returns (pd.Series): A Series of daily total returns.
        risk_free_rate (float): The annual risk-free rate for Sharpe ratio calculation.

    Returns:
        dict: A dictionary containing performance metrics.
    """
    if daily_returns.empty or len(daily_returns) < 2:
        return {
            'total_return': 0,
            'cagr': 0,
            'annualized_volatility': 0,
            'sharpe_ratio': 0,
            'max_drawdown': 0,
            'arithmetic_mean_return': 0,
            'geometric_mean_return': 0,
        }

    # Total Return
    total_return = (1 + daily_returns).prod() - 1

    # Compound Annual Growth Rate (CAGR)
    num_days = len(daily_returns)
    num_years = num_days / 252  # Assuming 252 trading days in a year
    cagr = ((1 + total_return)**(1 / num_years) - 1) if num_years > 0 else 0

    # Annualized Volatility
    annualized_volatility = daily_returns.std() * np.sqrt(252)

    # Sharpe Ratio
    excess_returns = daily_returns - (risk_free_rate / 252)
    sharpe_ratio = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252) if excess_returns.std() != 0 else 0

    # Maximum Drawdown
    cumulative_returns = (1 + daily_returns).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()

    # Mean Returns
    arithmetic_mean_return = daily_returns.mean()
    geometric_mean_return = (1 + daily_returns).prod()**(1/len(daily_returns)) - 1 if len(daily_returns) > 0 else 0


    return {
        'total_return': total_return,
        'cagr': cagr,
        'annualized_volatility': annualized_volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'arithmetic_mean_return': arithmetic_mean_return,
        'geometric_mean_return': geometric_mean_return,
    }

def get_summary_statistics(data_with_returns: pd.DataFrame, risk_free_rate: float = 0.0) -> dict:
    """
    Generates a summary statistics table.

    Args:
        data_with_returns (pd.DataFrame): DataFrame with 'Total_Return' and 'Dividends' columns.
        risk_free_rate (float): The annual risk-free rate.

    Returns:
        dict: A dictionary of summary statistics.
    """
    daily_returns = data_with_returns['Total_Return'].dropna()
    metrics = calculate_performance_metrics(daily_returns, risk_free_rate)

    summary = {
        "Total Return (%)": f"{metrics['total_return'] * 100:.2f}",
        "Annualized Return (CAGR) (%)": f"{metrics['cagr'] * 100:.2f}",
        "Annualized Volatility (%)": f"{metrics['annualized_volatility'] * 100:.2f}",
        "Sharpe Ratio": f"{metrics['sharpe_ratio']:.2f}",
        "Maximum Drawdown (%)": f"{metrics['max_drawdown'] * 100:.2f}",
        "Number of Dividend Payments": data_with_returns[data_with_returns['Dividends'] > 0].shape[0],
        "Total Dividends per Share": f"{data_with_returns['Dividends'].sum():.2f}",
    }
    return summary
