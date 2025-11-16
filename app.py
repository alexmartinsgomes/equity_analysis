import gradio as gr
import pandas as pd
from datetime import date, timedelta

# Project modules
from data_fetcher import fetch_equity_data, validate_dates
from returns_calculator import calculate_daily_total_return, get_summary_statistics
from visualizations import (
    plot_cumulative_return,
    plot_periodic_returns,
    plot_volume_analysis,
    plot_daily_returns_boxplot,
    plot_dividend_timeline
)
from utils import format_summary_for_display, save_df_to_temp_csv

# --- Analysis Function ---
def analyze_equity(ticker, start_date, end_date, boxplot_period, progress=gr.Progress()):
    """
    Main function to run the analysis and generate outputs for the Gradio interface.
    """
    # 1. Validate Inputs
    progress(0, desc="Validating inputs...")
    if not all([ticker, start_date, end_date]):
        return [gr.Markdown("Error: Ticker, Begin Date, and End Date are required.")] + [gr.update(visible=False)] * 8

    valid, msg = validate_dates(start_date, end_date)
    if not valid:
        return [gr.Markdown(f"Error: {msg}")] + [gr.update(visible=False)] * 8

    # 2. Fetch Data
    progress(0.2, desc=f"Fetching data for {ticker}...")
    try:
        data = fetch_equity_data(ticker, start_date, end_date)
        if data.empty:
            return [gr.Markdown(f"Error: Could not fetch data for '{ticker}'. Check the symbol or date range.")] + [gr.update(visible=False)] * 8
    except Exception as e:
        return [gr.Markdown(f"An unexpected error occurred: {e}")] + [gr.update(visible=False)] * 8

    # 3. Calculate Returns
    progress(0.4, desc="Calculating returns...")
    data_with_returns = calculate_daily_total_return(data)
    daily_total_returns = data_with_returns['Total_Return'].dropna()

    # 4. Generate Summary Statistics
    progress(0.5, desc="Generating summary...")
    summary_stats = get_summary_statistics(data_with_returns)
    summary_df = format_summary_for_display(summary_stats)

    # 5. Generate Visualizations
    progress(0.6, desc="Creating charts...")
    fig_cumulative = plot_cumulative_return(data_with_returns.copy())
    fig_periodic = plot_periodic_returns(daily_total_returns.copy())
    fig_volume = plot_volume_analysis(data.copy())
    fig_boxplot = plot_daily_returns_boxplot(daily_total_returns.copy(), boxplot_period)
    fig_dividends = plot_dividend_timeline(data.copy())
    
    # 6. Prepare Data Table for Download
    progress(0.9, desc="Finalizing...")
    download_filename = f"{ticker}_analysis_{start_date}_to_{end_date}.csv"
    csv_path = save_df_to_temp_csv(data_with_returns, download_filename)

    return [
        gr.update(visible=False), # Hide error message
        gr.update(visible=True, value=summary_df),
        gr.update(visible=True, value=fig_cumulative),
        gr.update(visible=True, value=fig_periodic),
        gr.update(visible=True, value=fig_volume),
        gr.update(visible=True, value=fig_boxplot),
        gr.update(visible=True, value=fig_dividends),
        gr.update(visible=True, value=data_with_returns.reset_index()),
        gr.update(visible=True, value=csv_path)
    ]

# --- Gradio Interface ---
def build_ui():
    """
    Builds the Gradio application interface.
    """
    with gr.Blocks(theme=gr.themes.Soft(), title="Equity Total Return Analysis") as app:
        gr.Markdown("# Equity Total Return Analysis")
        gr.Markdown("Analyze the performance of an equity, including total returns with dividends and interactive visualizations.")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Inputs")
                ticker_input = gr.Textbox(label="Ticker Symbol", placeholder="e.g., AAPL, ^GSPC")
                
                # Default dates: last 1 year
                end_date_input = gr.Textbox(label="End Date", value=date.today().strftime("%Y-%m-%d"))
                start_date_input = gr.Textbox(label="Begin Date", value=(date.today() - timedelta(days=365)).strftime("%Y-%m-%d"))

                boxplot_period_input = gr.Dropdown(
                    label="Box Plot Aggregation",
                    choices=["Monthly", "Quarterly", "Yearly"],
                    value="Monthly"
                )
                
                with gr.Row():
                    reset_btn = gr.Button("Reset")
                    submit_btn = gr.Button("Analyze", variant="primary")

            with gr.Column(scale=3):
                error_output = gr.Markdown(visible=False)
                
                with gr.Tabs(visible=False) as output_tabs:
                    with gr.TabItem("Summary & Charts"):
                        with gr.Row():
                            summary_output = gr.DataFrame(
                                label="Key Performance Metrics", 
                                headers=["Metric", "Value"],
                                interactive=False,
                                visible=False
                            )
                        with gr.Row():
                            cumulative_plot = gr.Plot(label="Cumulative Return", visible=False)
                        with gr.Row():
                            periodic_plot = gr.Plot(label="Periodic Returns", visible=False)
                        with gr.Row():
                            volume_plot = gr.Plot(label="Volume Analysis", visible=False)
                        with gr.Row():
                            boxplot_plot = gr.Plot(label="Daily Returns Distribution", visible=False)
                        with gr.Row():
                            dividend_plot = gr.Plot(label="Dividend Timeline", visible=False)

                    with gr.TabItem("Data Table"):
                        data_table_output = gr.DataFrame(label="Historical Data", visible=False, interactive=True)
                        download_button = gr.DownloadButton(label="Download Data as CSV", visible=False, elem_id="download_csv")

        # --- Event Handlers ---
        all_inputs = [ticker_input, start_date_input, end_date_input, boxplot_period_input]
        all_outputs = [
            error_output, summary_output, cumulative_plot, periodic_plot, 
            volume_plot, boxplot_plot, dividend_plot, data_table_output, download_button
        ]

        submit_btn.click(
            fn=lambda *args: [gr.update(visible=True)] + [gr.update(visible=False)] * 9, # Show tabs, hide outputs
            outputs=[output_tabs] + all_outputs
        ).then(
            fn=analyze_equity,
            inputs=all_inputs,
            outputs=all_outputs
        )

        def reset_ui():
            # Reset inputs to default and hide all output components
            default_end = date.today().strftime("%Y-%m-%d")
            default_start = (date.today() - timedelta(days=365)).strftime("%Y-%m-%d")
            return [
                "", default_start, default_end, "Monthly", # Reset inputs
                gr.update(visible=False), # Hide error
                gr.update(visible=False), # Hide tabs
            ] + [gr.update(visible=False)] * 8 # Hide all other outputs

        reset_btn.click(
            fn=reset_ui,
            outputs=[ticker_input, start_date_input, end_date_input, boxplot_period_input, error_output, output_tabs] + all_outputs[1:]
        )

    return app

if __name__ == "__main__":
    # Move files to the correct location for Gradio reload to work
    import os
    import shutil
    
    if not os.path.exists("app.py"):
        # This logic assumes we are running from the root of the project
        # and need to move the files from the subdirectory.
        # This is a workaround for Gradio's live reload feature.
        files_to_move = ['app.py', 'data_fetcher.py', 'returns_calculator.py', 'visualizations.py', 'utils.py', 'requirements.txt', '.gitignore']
        for f in files_to_move:
            if os.path.exists(f"equity_analyzer/{f}"):
                shutil.move(f"equity_analyzer/{f}", f)

    app = build_ui()
    app.launch(debug=True)
