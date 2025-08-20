
import os
import pandas as pd

# Get the base project directory (two levels up from this file)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CLEANED_DIR = os.path.join(DATA_DIR, "cleaned")

def read_root_csv(file_name="root.csv"):
    """
    Reads the root CSV file from the cleaned data folder.

    Parameters:
        file_name (str): The name of the CSV file. Defaults to "root.csv".

    Returns:
        pd.DataFrame: The loaded DataFrame, or an empty DataFrame if not found.
    """
    file_path = os.path.join(CLEANED_DIR, file_name)

    if not os.path.exists(file_path):
        print(f"[WARN] File not found: {file_path}")
        return pd.DataFrame()

    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"[ERROR] Failed to read CSV {file_path}: {e}")
        return pd.DataFrame()

def write_root_csv(df, file_name="root.csv"):
    """
    Writes a DataFrame to the root CSV file in the cleaned data folder.

    Parameters:
        df (pd.DataFrame): DataFrame to save.
        file_name (str): The name of the CSV file. Defaults to "root.csv".
    """
    file_path = os.path.join(CLEANED_DIR, file_name)

    try:
        df.to_csv(file_path, index=False)
        print(f"[INFO] Saved DataFrame to {file_path}")
    except Exception as e:
        print(f"[ERROR] Failed to write CSV {file_path}: {e}")
