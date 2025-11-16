import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_equity_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches historical equity data from Yahoo Finance.

    Args:
        ticker (str): The stock ticker symbol.
        start_date (str): The start date for the data (YYYY-MM-DD).
        end_date (str): The end date for the data (YYYY-MM-DD).

    Returns:
        pd.DataFrame: A DataFrame containing the historical data, or an empty
                      DataFrame if an error occurs.
    """
    try:
        stock = yf.Ticker(ticker)
        # Add 1 day to end_date to make it inclusive in yfinance
        end_date_inclusive = (pd.to_datetime(end_date) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        data = stock.history(start=start_date, end=end_date_inclusive, auto_adjust=False)

        if data.empty:
            raise ValueError(f"No data found for ticker '{ticker}' in the given date range.")

        # Ensure required columns are present
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
        for col in required_cols:
            if col not in data.columns:
                data[col] = 0

        # Forward fill dividends and stock splits to align with price data on ex-dividend dates
        data[['Dividends', 'Stock Splits']] = data[['Dividends', 'Stock Splits']].fillna(0)

        return data

    except Exception as e:
        print(f"An error occurred while fetching data for {ticker}: {e}")
        return pd.DataFrame()

def validate_dates(start_date_str: str, end_date_str: str) -> tuple[bool, str]:
    """
    Validates the provided start and end dates.

    Args:
        start_date_str (str): The start date string (YYYY-MM-DD).
        end_date_str (str): The end date string (YYYY-MM-DD).

    Returns:
        tuple[bool, str]: A tuple containing a boolean indicating if the dates are valid,
                          and a string message.
    """
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()

        if start_date > end_date:
            return False, "Error: Begin date cannot be after end date."
        if start_date > today or end_date > today:
            return False, "Error: Dates cannot be in the future."

        return True, "Dates are valid."

    except ValueError:
        return False, "Error: Invalid date format. Please use YYYY-MM-DD."
