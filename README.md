# Equity Total Return Analysis

A comprehensive Python application for in-depth equity total return analysis, featuring an intuitive web interface built with Gradio. This tool allows users to fetch historical equity data, calculate a wide range of performance metrics including dividends, and visualize the results through interactive charts.

## Key Features
- **Historical Data Fetching**: Utilizes the `yfinance` library to retrieve daily prices, volume, dividends, and stock splits.
- **Comprehensive Calculations**: Computes daily total returns, aggregated periodic returns (monthly, quarterly, yearly), CAGR, annualized volatility, Sharpe ratio, and maximum drawdown.
- **Interactive Visualizations**: Generates a suite of `plotly` charts:
    - Cumulative Total Return vs. Price Return
    - Periodic Returns Bar Chart (Monthly, Quarterly, Yearly)
    - Price and Volume Analysis
    - Box Plot of Daily Return Distributions
    - Dividend Payment Timeline
- **Intuitive UI**: A clean, user-friendly interface powered by Gradio, with organized tabs for summary statistics, charts, and raw data.
- **Data Export**: Allows users to download the complete historical data and analysis results as a CSV file.

## Installation

### Prerequisites
- Python 3.8+
- A virtual environment (recommended)

### Setup
1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd equity-analyzer
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux/Windows
    uv init
    ```

3.  **Install the required dependencies:**
    ```bash
    uv add -r requirements.txt
    ```
## Usage Guide

1.  **Run the application:**
    ```bash
    uv run app.py
    ```
    This will start the Gradio web server. Open the URL displayed in your terminal (usually `http://127.0.0.1:7860`) in your web browser.

2.  **Input Parameters:**
    -   **Ticker Symbol**: Enter the stock ticker you want to analyze (e.g., `AAPL`, `MSFT`, `^GSPC` for the S&P 500).
    -   **Begin Date / End Date**: Select the start and end dates for the analysis period.
    -   **Box Plot Aggregation**: Choose the time period (Monthly, Quarterly, or Yearly) for grouping the daily return distribution box plot.

3.  **Analyze:**
    -   Click the **"Analyze"** button to fetch data and run the calculations.
    -   Loading indicators will show the progress.

4.  **View Results:**
    -   **Summary & Charts Tab**: View key performance metrics and all interactive visualizations.
    -   **Data Table Tab**: Inspect the raw daily data, including calculated returns. You can sort and filter this table.
    -   **Download Data**: Click the "Download Data as CSV" button to save the data locally.

## Features in Detail

### Return Calculations
-   **Daily Total Return**: Calculated as `(Price_t - Price_t-1 + Dividend_t) / Price_t-1`. This ensures dividends are accurately included on the ex-dividend date.
-   **Cumulative Return**: The compounded return over the entire period, shown separately for price-only and total return.
-   **CAGR (Compound Annual Growth Rate)**: The geometric mean annual return.
-   **Volatility**: The annualized standard deviation of daily total returns, a measure of risk.
-   **Sharpe Ratio**: Measures risk-adjusted return, calculated using an assumed risk-free rate of 0.
-   **Maximum Drawdown**: The largest peak-to-trough decline in the investment's value.

### Visualizations
-   **Cumulative Return Comparison**: A line chart that clearly illustrates the long-term impact of reinvesting dividends.
-   **Periodic Returns**: Bar charts that make it easy to spot performance trends across different months, quarters, or years.
-   **Daily Returns Distribution (Box Plot)**: A powerful visualization for understanding volatility and return patterns. Each box shows the median, interquartile range, and outliers of daily returns for a given period (e.g., each month). This helps answer questions like, "Which months were most volatile?"

## Technical Details
-   **Data Source**: All financial data is sourced from Yahoo Finance via the `yfinance` library. Data accuracy and availability are dependent on this source.
-   **Assumptions**:
    -   The Sharpe ratio calculation assumes a risk-free rate of 0.0%.
    -   Annualization calculations assume 252 trading days in a year.
    -   Dividends are assumed to be reinvested on the ex-dividend date.
