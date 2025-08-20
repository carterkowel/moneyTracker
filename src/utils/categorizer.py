# Import Packages
import pandas as pd
import json
import os
import re

# Helper Functions
def normalize(text):
    """
    Normalize input text by lowercasing and removing non-alphanumeric characters.

    Args:
        text (str): The input string.

    Returns:
        str: Normalized string.
    """
    return re.sub(r'\W+', '', (text or "").lower())

def load_rules(rule_path):
    """
    Load and normalize rule mappings from JSON file.

    Args:
        rule_path (str): Path to the rule_mapping.json file.

    Returns:
        dict[str, list[str]]: Mapping of category -> list of normalized keywords.
    """
    with open(rule_path, "r", encoding="utf-8") as f:
        raw_rules = json.load(f)
    return {
        category: [normalize(keyword) for keyword in keywords]
        for category, keywords in raw_rules.items()
    }

def assign_category(description, rules):
    """
    Assign a category to a transaction based on keyword matching.

    Args:
        description (str): The transaction description.
        rules (dict[str, list[str]]): Category keyword rules.

    Returns:
        str: Assigned category or 'Uncategorized'.
    """
    desc_norm = normalize(description)
    for category, keywords in rules.items():
        if any(kw in desc_norm for kw in keywords):
            return category.capitalize()
    return "Uncategorized"

def load_necessity_map(json_path):
    """
    Load necessity mapping and invert it to category -> necessity.

    Args:
        json_path (str): Path to the necessity_mapping.json file.

    Returns:
        dict[str, str]: Mapping of category -> 'Need' or 'Want'.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        necessity_data = json.load(f)
    cat_to_nec = {}
    for necessity, categories in necessity_data.items():
        for cat in categories:
            cat_to_nec[cat.strip().lower()] = necessity
    return cat_to_nec

# Main Functions
def assign_necessities(df):
    """
    Categorizes and labels transactions with 'Necessity'.

    This function:
    - Applies necessity labels based on the category.
    - Returns a modified DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Categorized DataFrame with new 'Necessity' column.
    """
    # Load category and necessity mappings
    script_dir = os.path.dirname(os.path.abspath(__file__))
    necessity_path = os.path.join(script_dir, "..", "config", "necessity_mapping.json")

    necessity_map = load_necessity_map(necessity_path)

    df = df.copy()

    if "Category" not in df.columns:
        raise KeyError("'Category' column not found in input DataFrame")

    # Assign category and necessity
    df["Necessity"] = df["Category"].apply(
        lambda cat: necessity_map.get(str(cat).strip().lower(), "Unknown")
    )

    return df

def assign_categories(df):
    """
    Categorizes and labels transactions with 'Category'.

    This function:
    - Applies category rules based on keywords in transaction descriptions.
    - Applies necessity labels based on the category.
    - Returns a modified DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame with at least a 'Description' and 'Amount' column.

    Returns:
        pd.DataFrame: Categorized DataFrame with new 'Category' and 'Necessity' columns.
    """
    # Load category and necessity mappings
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rule_path = os.path.join(script_dir, "..", "config", "rule_mapping.json")

    rules = load_rules(rule_path)

    df = df.copy()

    if "Description" not in df.columns:
        raise KeyError("'Description' column not found in input DataFrame")

    # Assign category and necessity
    df["Category"] = df["Description"].apply(lambda x: assign_category(x, rules))

    return df
