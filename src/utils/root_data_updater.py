import pandas as pd
import os
from fuzzywuzzy import fuzz


def update_root_csv(root_csv_path, df_transactions, amount_precision=2, description_threshold=90):
    """
    Updates the root CSV file with newly parsed transactions using fuzzy duplicate detection.

    Reports:
        - Count of new transactions added
        - Categorized vs. Uncategorized count and amount
        - Number of duplicates skipped

    Args:
        root_csv_path (str): File path to the root/master CSV.
        df_transactions (pd.DataFrame): DataFrame containing newly parsed transactions.
        amount_precision (int): Decimal places to round Amount for duplicate checking.
        description_threshold (int): Similarity ratio (0–100) above which descriptions are considered duplicates.
    """

    df_transactions["Date"] = pd.to_datetime(df_transactions["Date"], format="%Y%m%d")
    df_transactions["Amount"] = pd.to_numeric(df_transactions["Amount"], errors="coerce").round(amount_precision)

    # Load or initialize root CSV BEFORE trying to use df_root
    if os.path.exists(root_csv_path):
        df_root = pd.read_csv(root_csv_path, parse_dates=["Date"])
        df_root["Amount"] = pd.to_numeric(df_root["Amount"], errors="coerce").round(amount_precision)
    else:
        df_root = pd.DataFrame(columns=df_transactions.columns)

    # Normalize whitespace in Descriptions
    for df in [df_root, df_transactions]:
        df["Description"] = df["Description"].str.replace(r"\s+", " ", regex=True).str.strip()

    # Duplicate detection
    new_rows = []
    duplicate_count = 0
    for _, new_row in df_transactions.iterrows():
        date_match = df_root["Date"] == new_row["Date"]
        amount_match = df_root["Amount"] == new_row["Amount"]
        card_match = df_root["Card"] == new_row["Card"]

        candidates = df_root[date_match & amount_match & card_match]

        is_duplicate = any(
            fuzz.partial_ratio(new_row["Description"], existing_desc) >= description_threshold
            for existing_desc in candidates["Description"]
        )

        if is_duplicate:
            duplicate_count += 1
        else:
            new_rows.append(new_row)

    if not new_rows:
        print("✅ No new transactions found.")
        print(f"🚫 Skipped {duplicate_count} duplicate transactions.")
        return

    # Append and save
    new_df = pd.DataFrame(new_rows, columns=df_transactions.columns)
    combined_df = pd.concat([df_root, new_df], ignore_index=True)
    combined_df.sort_values(by="Date", ascending=False, inplace=True)
    combined_df.to_csv(root_csv_path, index=False)

    # Reporting
    added_count = len(new_df)
    added_total = new_df.loc[new_df["Amount"] > 0, "Amount"].sum()
    categorized_df = new_df[new_df["Category"].str.lower() != "uncategorized"]
    uncategorized_df = new_df[new_df["Category"].str.lower() == "uncategorized"]

    print(f"✅ Added {added_count} new transactions to root CSV, totaling ${added_total:.2f}.")
    print(f"🗂️  Categorized: {len(categorized_df)} | ${categorized_df['Amount'].sum():.2f}")
    print(f"❓ Uncategorized: {len(uncategorized_df)} | ${uncategorized_df['Amount'].sum():.2f}")
    print(f"🚫 Skipped {duplicate_count} duplicate transactions.")