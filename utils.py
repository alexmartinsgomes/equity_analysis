import pandas as pd

def format_summary_for_display(summary: dict) -> pd.DataFrame:
    """
    Formats the summary dictionary into a DataFrame for clean display in Gradio.

    Args:
        summary (dict): The dictionary of summary statistics.

    Returns:
        pd.DataFrame: A formatted DataFrame with 'Metric' and 'Value' columns.
    """
    if not summary:
        return pd.DataFrame(columns=['Metric', 'Value'])
        
    summary_df = pd.DataFrame(list(summary.items()), columns=['Metric', 'Value'])
    return summary_df

import tempfile
import os

def save_df_to_temp_csv(df: pd.DataFrame, filename: str) -> str:
    """
    Saves a DataFrame to a temporary CSV file with a specific name and returns the path.
    """
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, filename)
    df.to_csv(temp_path, index=True)
    return temp_path

