# import packages
import numpy as np
import pandas as pd
import re
import fitz as pymupdf
from datetime import datetime
import math
import os
import shutil
import base64
import tempfile

# Core Functions:
def determine_statement_type(file_path):
    """
    Determines the file type and associated card type from the given statement file.

    Args:
        file_path (str): Path to the input statement file.

    Returns:
        tuple:
            - file_type (str): 'csv' or 'pdf' depending on the file extension.
            - card_type (str): One of 'bmo_cashback', 'scotia_momentum', or 'scotia_scene'.
    """
    ext = file_path.lower().split(".")[-1]
    if ext == "csv":
        with open(file_path, "r") as f:
            content = f.read()

        if "Transaction Amount" in content and "Card #" in content:
            return "csv", "bmo_cashback"
        elif "Momentum" in file_path:
            return "csv", "scotia_momentum"
        elif "Scene" in file_path:
            return "csv", "scotia_scene"

    elif ext == "pdf":
        # text, lines = read_pdf(file_path)
        # if any("BMO CashBack" in l for l in lines):
        return "pdf", "bmo_cashback"
    
        # elif "Momentum" in text:
        #     return "pdf", "scotia_momentum"
        # elif "SCENE" in text:
        #     return "pdf", "scotia_scene"

    return None, None

def process_statement(file_path, file_type, card_type):
    """
    Processes a statement file and returns a standardized DataFrame of transactions.

    This function dispatches the input file to the appropriate handler based on its
    type (CSV or PDF) and card type (e.g., BMO Cashback, Scotia Momentum, or Scotia Scene).

    Args:
        file_path (str): Path to the statement file.
        file_type (str): File extension/type — expected to be either 'csv' or 'pdf'.
        card_type (str): Identifier for the credit card type — expected to be one of
                         'bmo_cashback', 'scotia_momentum', or 'scotia_scene'.

    Returns:
        pd.DataFrame: A standardized DataFrame of transactions with columns:
                      ['Date', 'Amount', 'Description', 'Card', 'Category', 'Necessity']

    Raises:
        ValueError: If the file type or card type is unrecognized or unsupported.
    """
    if file_type == "csv":
        if card_type == "bmo_cashback":
            df = process_bmo_csv(file_path)
        elif card_type == "scotia_momentum":
            df = process_scotia_csv(file_path, card_type)
        elif card_type == "scotia_scene":
            df = process_scotia_csv(file_path, card_type)
        else:
            raise ValueError("Unknown card type for CSV")

    elif file_type == "pdf":
        if card_type == "bmo_cashback":
            df = process_bmo_pdf(file_path)
        elif card_type == "scotia_momentum":
            df = process_scotia_pdf(file_path, card_type)
        elif card_type == "scotia_scene":
            df = process_scotia_pdf(file_path, card_type)
        else:
            raise ValueError("Unknown card type for PDF")

    else:
        raise ValueError("Unsupported file type")
    
    # Remove all Payments to Card
    df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce')
    df = df.drop(df[df.Amount < 0].index)
    df["Amount"] = df["Amount"].round(2)

    return df

# Card Specific Functions:
def process_bmo_csv(csv_path):
    """
    Process a BMO CSV statement into a standardized DataFrame and extract subtotal info.

    Args:
        csv_path (str): Path to the input CSV file.

    Returns:
        pd.DataFrame: DataFrame of parsed transactions with columns:
            ['Date', 'Amount', 'Description', 'Card', 'Category', 'Necessity']
    """
    df_raw = pd.read_csv(csv_path, skiprows=1)  # skip timestamp row

    # Rename and select needed columns
    df = df_raw.rename(columns={
        "Transaction Date": "Date",
        "Transaction Amount": "Amount",
        "Description": "Description"
    })[["Date", "Amount", "Description"]]

    # Add fixed columns
    df["Card"] = "bmo_cashback"
    df["Category"] = pd.NA
    df["Necessity"] = pd.NA

    # Format date
    df["Date"] = pd.to_datetime(df["Date"], format='%Y%m%d')

    return df

def process_scotia_csv(csv_path, card_type):
    """
    Process a Scotia CSV statement into a standardized DataFrame and extract subtotal info.

    Args:
        csv_path (str): Path to the input CSV file.
        card_type (str): Identifier for the credit card type — expected to be one of
                    'scotia_momentum', or 'scotia_scene'.

    Returns:
        pd.DataFrame: DataFrame of parsed transactions with columns:
            ['Date', 'Amount', 'Description', 'Card', 'Category', 'Necessity']
    """
    df_raw = pd.read_csv(csv_path)

    # Rename and select relevant columns
    df = df_raw[["Date", "Amount", "Description"]].copy()


    # Add standard columns
    df["Card"] = card_type
    df["Category"] = pd.NA
    df["Necessity"] = pd.NA

    # Clean formatting
    df["Date"] = pd.to_datetime(df["Date"], format='%Y-%m-%d')
    df["Amount"] = df["Amount"].astype(float)

    return df

def process_bmo_pdf(pdf_path):
    """
    Process a BMO PDF statement into a standardized DataFrame and extract subtotal info.

    Args:
        csv_path (str): Path to the input CSV file.

    Returns:
        pd.DataFrame: DataFrame of parsed transactions with columns:
            ['Date', 'Amount', 'Description', 'Card', 'Category', 'Necessity']
    """
    text, lines = read_pdf(pdf_path)
    if "Grocery Bonus" in text:
        #old format of statement
        info = extract_old_statement_info(lines)
        df = extract_old_statement_transactions(text, info["statement_period"])
    else:
        info = extract_statement_info(lines)
        df = extract_statement_transactions(text, info["statement_period"])
    
    subtotal_sanity_check(df, info["subtotal"])

    return df

def process_scotia_pdf(pdf_path, card_type):
    """
    Process a Scotia PDF statement into a standardized DataFrame and extract subtotal info.

    Args:
        csv_path (str): Path to the input CSV file.
        card_type (str): Identifier for the credit card type — expected to be one of
                    'scotia_momentum', or 'scotia_scene'.
    Returns:
        pd.DataFrame: DataFrame of parsed transactions with columns:
            ['Date', 'Amount', 'Description', 'Card', 'Category', 'Necessity']
    """
    #TODO
    ...

# Helper Functions:
def read_pdf(pdf_path):
    """
    Extract text content from a PDF file for analysis.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        tuple:
            - text (str): Full text content of the PDF.
            - lines (list of str): List of individual lines extracted from the text.
    """
    doc = pymupdf.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    lines = text.splitlines()
    return text, lines

def extract_statement_info(lines):
    """
    Extract subtotal, groceries total, and statement period from statement text.

    Args:
        lines (list of str): List of lines from the PDF statement.

    Returns:
        dict: Dictionary containing:
            - 'subtotal' (float): Total spending amount.
            - 'groceries_total' (float): Implied total grocery spend (derived from cashback).
            - 'statement_period' (dict): Mapping of month abbreviations to years, e.g. {'Dec': 2023, 'Jan': 2024}.

    Raises:
        ValueError: If any required field is missing in the statement.
    """
    cashback_rate = 0.025

    subtotal = None
    groceries_total = None
    statement_period = None

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Subtotal
        if subtotal is None and stripped_line.startswith("Subtotal for") and i + 1 < len(lines):
            subtotal = float(lines[i + 1].strip().replace(",", "").replace("$", ""))

        # Groceries
        elif groceries_total is None and stripped_line == "Groceries" and i + 1 < len(lines):
            groceries_cashback = float(lines[i + 1].strip().lstrip("$")) # Remove $ (format: $1.99)
            groceries_total = groceries_cashback / cashback_rate

        # Statement Period
        elif statement_period is None and stripped_line == "Statement period" and i + 1 < len(lines):
            statement_period_text = lines[i + 1].strip()
            date_match = re.match(
                r"([A-Za-z]+)\.?\s+\d{1,2},\s+(\d{4})\s*-\s*([A-Za-z]+)\.?\s+\d{1,2},\s+(\d{4})",
                statement_period_text
            ) # Note: Statement period format: (format: Month. Day, Year - Month. Day, Year )
            if date_match:
                month1, year1, month2, year2 = date_match.groups()
                month1 = month1[:3].capitalize()
                month2 = month2[:3].capitalize()
                statement_period = {
                    month1: int(year1),
                    month2: int(year2)
                }

    # Validate all expected fields are found
    missing = []
    if subtotal is None:
        missing.append("subtotal")
    if groceries_total is None:
        missing.append("groceries_total")
    if statement_period is None:
        missing.append("statement_period")

    if missing:
        raise ValueError(f"Aborted, failed to extract the following from the statement:\n{', '.join(missing)}")
    
    return {
        "subtotal": subtotal,
        "groceries_total": groceries_total,
        "statement_period": statement_period,
    }

def extract_old_statement_info(lines):
    """
    Extract subtotal, groceries total, and statement period from old style of statement text (bmo pdfs Jan 2023 and older).

    Args:
        lines (list of str): List of lines from the PDF statement.

    Returns:
        dict: Dictionary containing:
            - 'subtotal' (float): Total spending amount.
            - 'groceries_total' (float): Implied total grocery spend (derived from cashback).
            - 'statement_period' (dict): Mapping of month abbreviations to years, e.g. {'Dec': 2023, 'Jan': 2024}.

    Raises:
        ValueError: If any required field is missing in the statement.
    """
    cashback_rate = 0.025

    subtotal = None
    groceries_total = None
    statement_period = None

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Subtotal
        if subtotal is None and stripped_line.startswith("Purchases and other charges") and i + 1 < len(lines):
            subtotal = float(lines[i + 1].strip().replace(",", "").replace("+", "").replace("$", ""))

        # Groceries
        elif groceries_total is None and stripped_line == "Grocery Bonus - 2.5%" and i + 1 < len(lines):
            groceries_cashback = float(lines[i + 1].strip().lstrip("$")) # Remove $ (format: $1.99)
            groceries_total = groceries_cashback / cashback_rate

        # Statement Period
        elif statement_period is None and stripped_line == "PERIOD COVERED BY THIS STATEMENT" and i + 1 < len(lines):
            statement_period_text = lines[i + 1].strip()
            date_match = re.match(
                r"([A-Za-z]+)\.?\s+\d{1,2},\s+(\d{4})\s*-\s*([A-Za-z]+)\.?\s+\d{1,2},\s+(\d{4})",
                statement_period_text
            ) # Note: Statement period format: (format: Month. Day, Year - Month. Day, Year )
            if date_match:
                month1, year1, month2, year2 = date_match.groups()
                month1 = month1[:3].capitalize()
                month2 = month2[:3].capitalize()
                statement_period = {
                    month1: int(year1),
                    month2: int(year2)
                }

    # Validate all expected fields are found
    missing = []
    if subtotal is None:
        missing.append("subtotal")
    if groceries_total is None:
        missing.append("groceries_total")
    if statement_period is None:
        missing.append("statement_period")

    if missing:
        raise ValueError(f"Aborted, failed to extract the following from the statement:\n{', '.join(missing)}")
    
    return {
        "subtotal": subtotal,
        "groceries_total": groceries_total,
        "statement_period": statement_period,
    }

def extract_statement_transactions(statement_text, statement_period):
    """
    Extracts and parses all credit card transactions from the full statement text.

    This function:
    1. Extracts the relevant transaction sections from the raw PDF text.
    2. Parses each transaction into a structured DataFrame with date, amount, and description.
    3. Ensures all transaction records are correctly formatted or raises errors if parsing fails.

    Args:
        statement_text (str): Full text content extracted from the credit card statement PDF.
        statement_period (dict): Mapping of 3-letter month names to corresponding years 
                                 (e.g., {'Dec': 2023, 'Jan': 2024}).

    Returns:
        pd.DataFrame: DataFrame of parsed transactions with fields: Date, Amount, Description, Card, Category, Necessity.

    Raises:
        ValueError: If transaction sections cannot be extracted or any transaction is malformed.
    """

    def extract_transaction_sections(statement_text):
        """
        Extracts all blocks of transaction data from a credit card statement's full statement text.

        This function identifies transaction sections by locating known headers 
        (e.g., "TRANS DATE POSTING DATE ...") and capturing all text between them 
        and the next known end marker (e.g., "Subtotal for ...", "continued on next page", 
        or "BMO CashBack Mastercard"). It supports statements that span multiple pages.

        Args:
            statement_text (str): The full extracted text from a PDF credit card statement.

        Returns:
            str: Combined text of all transaction sections extracted from the full statement.

        Raises:
            ValueError: If no transaction headers are found (start pattern not matched).
            ValueError: If an end pattern is not found after a start pattern.

        """
        # Normalize line endings
        statement_text = statement_text.replace("\r\n", "\n").replace("\r", "\n")

        # Start of each transaction section
        start_pattern = re.compile(
            r"TRANS\s+DATE\s+POSTING\s+DATE\s+DESCRIPTION\s+AMOUNT\s+\(\$\)\n"
            r"(Card number:.*?\n)?",
            re.IGNORECASE
        )

        # Possible end of a section (both continued or final totals)
        end_pattern = re.compile(
            r"(Subtotal for .+?|(?:\(\s*)?continued on next page)",
            re.IGNORECASE
        )

        transaction_sections = []
        start_positions = [m.end() for m in start_pattern.finditer(statement_text)]

        if not start_positions:
            raise ValueError("No transaction headers found — unable to locate start of transaction section.")


        for start_pos in start_positions:
            after_start = statement_text[start_pos:]
            end_match = end_pattern.search(after_start)

            if end_match:
                section = after_start[:end_match.start()].strip()
            else:
                raise ValueError("Unable to extract transaction section: end pattern not found after start.")

            transaction_sections.append(section)

        combined_text = "\n".join(transaction_sections)

        return combined_text

    def parse_transactions(transactions_text, statement_period):
        """
        Parses individual transactions from extracted text blocks into structured data.

        Each transaction consists of:
        - A date line (month + day)
        - One or more description lines
        - A line containing the amount (may end in 'CR' for credits)

        Args:
            transactions_text (str): Combined text block of all transactions.
            statement_period (dict): Dictionary of {month_abbr: year} used to complete the full transaction date.

        Returns:
            pd.DataFrame: DataFrame containing all parsed transaction records.

        Raises:
            ValueError: If any part of a transaction (date, amount, format) is invalid or missing.
        """

        def is_amount_line(line):
            """Returns True if the line is a properly formatted amount line (e.g., 19.99 or 450.00 CR)."""
            return re.match(r"^\$?\s*-?\d{1,3}(?:,\d{3})*\.\d{2}(?:\s*CR)?$", line.strip())
        
        lines = transactions_text.splitlines()
        transactions = []
        i = 0

        while i < len(lines) - 1:
            date_line = lines[i].strip()
            parts = date_line.split()

            # Handle split dates across two lines (e.g., 'Jul. 1' then 'Jul. 3')
            if len(parts) == 2 and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                date_line = f"{date_line} {next_line}"
                parts = date_line.split()
                i += 1  # Skip the extra date line we just consumed

            if len(parts) >= 2:
                trans_month_raw = parts[0]
                trans_day = parts[1]
                trans_month = trans_month_raw.replace(".", "")[:3].capitalize()

                try:
                    trans_day = int(trans_day)
                except ValueError:
                    raise ValueError(f"Invalid transaction day: '{trans_day}' in line '{date_line}'")


                year = statement_period.get(trans_month)
                if not year:
                    raise ValueError(f"Unknown month '{trans_month}' in line: '{date_line}'")


                try:
                    date_obj = datetime.strptime(f"{year} {trans_month} {trans_day}", "%Y %b %d")
                    trans_date = date_obj.strftime("%Y%m%d")
                except ValueError:
                    raise ValueError(f"Invalid date format: '{date_line}'")



                desc_lines = []
                j = i + 1
                while j < len(lines):
                    candidate = lines[j].strip()
                    if is_amount_line(candidate):
                        amount_line = candidate
                        break
                    desc_lines.append(candidate)
                    j += 1
                else:
                    raise ValueError(f"Missing amount for transaction starting at line {i}: '{date_line}'")


                description = ' '.join(desc_lines)                    
                is_credit = amount_line.endswith("CR")
                amount_str = amount_line.replace("CR", "").replace(",", "").replace("$", "").strip()

                try:
                    amount = float(amount_str)
                    if is_credit:
                        amount = -amount
                except ValueError:
                    raise ValueError(f"Invalid amount format: '{amount_line}'")


                transactions.append({
                    "Date": trans_date,
                    "Amount": round(amount, 2),
                    "Description": description,
                    "Card": "bmo_cashback",
                    "Category": pd.NA,
                    "Necessity": pd.NA
                })

                i = j + 1
            else:
                i += 1

        df = pd.DataFrame(transactions)
        df["Date"] = pd.to_datetime(df["Date"], format='%Y%m%d')
        return df

    try:
        transactions_text = extract_transaction_sections(statement_text)
    except ValueError as e:
        return
    try:
        df = parse_transactions(transactions_text, statement_period)
    except ValueError as e:
        return
    
    return df

def extract_old_statement_transactions(statement_text, statement_period):
    """
    Extracts and parses all credit card transactions from the full statement text.

    Args:
        statement_text (str): Full text content extracted from the credit card statement PDF.
        statement_period (dict): Mapping of 3-letter month names to corresponding years 
                                 (e.g., {'Dec': 2023, 'Jan': 2024}).

    Returns:
        pd.DataFrame: DataFrame of parsed transactions with fields: Date, Amount, Description, Card, Category, Necessity.

    Raises:
        ValueError: If transaction sections cannot be extracted or any transaction is malformed.
    """

    def extract_transaction_sections(statement_text):
        """
        Extracts all blocks of transaction data from a credit card statement's full statement text.

        Returns:
            str: Combined text of all transaction sections extracted from the full statement.
        """
        # Normalize line endings
        text = statement_text.replace("\r\n", "\n").replace("\r", "\n")

        # Find all start headers
        start_pattern = re.compile(
            r"DATE\s+DESCRIPTION\s+REFERENCE NO\.\s+AMOUNT\s+\(\$\)\n(?:Card Number:\s*\d{4}\s\d{4}\s\d{4}\s\d{4})?",
            re.IGNORECASE
        )

        end_pattern = re.compile(
            r"(\d{16}\s+\d{13,}\s+\d{13,}|Bonus reward\(s\) this statement)",
            re.IGNORECASE
        )


        transaction_sections = []

        for match in start_pattern.finditer(text):
            start_pos = match.end()
            after_start = text[start_pos:]

            end_match = end_pattern.search(after_start)
            if end_match:
                section = after_start[:end_match.start()].strip()
            else:
                section = after_start.strip()  # fallback: take until end of doc

            transaction_sections.append(section)

        if not transaction_sections:
            raise ValueError("No transaction sections found.")

        return "\n".join(transaction_sections)


    def parse_transactions(transactions_text, statement_period):
        """
        Parses transactions from text into a DataFrame.
        
        Args:
            transactions_text (str): Full raw text of all transactions.
            statement_period (dict): e.g. {'Apr': 2024, 'May': 2024}
            
        Returns:
            pd.DataFrame: Parsed transactions
        """
        
        def is_date_line(line):
            return bool(re.match(r"^[A-Z][a-z]{2}\.?\s+\d{1,2}$", line.strip()))

        def is_amount_line(line):
            return bool(re.match(r"^\$?\d[\d,]*\.\d{2}( CR)?$", line.strip()) or re.match(r"^\d+\.\d{2}( CR)?$", line.strip()))

        lines = [line.strip() for line in transactions_text.splitlines() if line.strip()]
        transactions = []
        i = 0

        while i < len(lines):
            # Detect date line
            if not is_date_line(lines[i]):
                i += 1
                continue

            # Parse transaction date
            try:
                month_abbr, day = lines[i].replace(".", "").split()
                year = statement_period.get(month_abbr)
                if not year:
                    raise ValueError(f"Month '{month_abbr}' not found in statement_period.")
                trans_date = datetime.strptime(f"{year} {month_abbr} {day}", "%Y %b %d").strftime("%Y%m%d")
            except Exception as e:
                raise ValueError(f"Invalid transaction date at line {i}: {lines[i]} — {e}")

            i += 1  # skip posting date (line i+1)
            if i >= len(lines): break
            i += 1

            # Collect description lines until amount is found
            desc_lines = []
            while i < len(lines) and not is_amount_line(lines[i]):
                desc_lines.append(lines[i])
                i += 1

            if i >= len(lines):
                break  # amount line not found; possibly malformed at end

            # Last desc line is the reference, remove it
            if desc_lines:
                desc_lines = desc_lines[:-1]

            amount_line = lines[i]
            i += 1

            is_credit = amount_line.endswith("CR")
            amount_str = amount_line.replace("CR", "").replace(",", "").replace("$", "").strip()

            try:
                amount = float(amount_str)
                if is_credit:
                    amount = -amount
            except ValueError:
                raise ValueError(f"Invalid amount format: '{amount_line}'")

            transactions.append({
                "Date": trans_date,
                "Amount": round(amount, 2),
                "Description": " ".join(desc_lines),
                "Card": "bmo_cashback",
                "Category": pd.NA,
                "Necessity": pd.NA
            })
            # print(f"Date: {trans_date}")
            # print(f"Amount: {amount}")
            # print(f"Description: {' | '.join(desc_lines)}")
            # print("-" * 20)

        return pd.DataFrame(transactions)

    # Main extraction flow
    try:
        transactions_text = extract_transaction_sections(statement_text)
    except ValueError as e:
        print(f"Transaction extraction failed: {e}")
        return None

    try:
        df = parse_transactions(transactions_text, statement_period)
    except ValueError as e:
        print(f"Transaction parsing failed: {e}")
        return None

    df["Date"] = pd.to_datetime(df["Date"], format='%Y%m%d')

    return df

def subtotal_sanity_check(df_transactions, expected_subtotal):
    """
    Compares subtotal to sum of charges only and raise error if totals differ by more than 10 cents

    Args:
        df_transactions (df): Df of all transactions extracted
        expected_subtotal (int): Subtotal posted on the statement 

    Raises:
        ValueError: If there is a mismatch between expected subtotal and sum of transactions.
    """
    transaction_total = df_transactions.loc[df_transactions["Amount"] > 0, "Amount"].sum()

    # Identify cashback and refund credits
    refunds_mask = (
        (df_transactions["Amount"] < 0) &
        (~df_transactions["Description"].str.contains("PAYMENT RECEIVED - THANK YOU", case=False, na=False))
    )

    refunds_total = df_transactions.loc[refunds_mask, "Amount"].sum()

    # Raise error if totals differ by more than 10 cents
    if not (math.isclose(transaction_total, expected_subtotal, abs_tol=0.1) or math.isclose(transaction_total, expected_subtotal-refunds_total, abs_tol=0.1)):
        print(f"⚠️ Sanity check failed: transaction total (${transaction_total:.2f}) ≠ expected subtotal (${expected_subtotal:.2f})")
        raise ValueError("Mismatch between expected subtotal and sum of transactions.")

# Main Function:
def process_uploaded_statements(list_of_contents, list_of_names):
    all_transactions = []
    output_log = ""

    with tempfile.TemporaryDirectory() as tmpdir:
        for content, name in zip(list_of_contents, list_of_names):
            df_transactions = None  # initialize at start of each iteration
            try:
                # output_log += f"📄 Processing file: {name}\n"
                
                header, encoded = content.split(",", 1)
                file_data = base64.b64decode(encoded)
                
                tmp_file_path = os.path.join(tmpdir, name)
                with open(tmp_file_path, "wb") as f:
                    f.write(file_data)

                file_type, card_type = determine_statement_type(tmp_file_path)
                if not file_type or not card_type:
                    output_log += f"❌ Unknown format for '{name}' — skipping.\n"
                    continue

                df_transactions = process_statement(tmp_file_path, file_type, card_type)
                subtotal = df_transactions.loc[df_transactions["Amount"] > 0, "Amount"].sum()
                output_log += f"✅ File {name} processed successfully: {len(df_transactions)} transactions totaling ${subtotal:.2f}\n"
                all_transactions.append(df_transactions)

            except Exception as e:
                output_log += f"❌ Error processing '{name}': {e}\n\n"
                # Do NOT reference df_transactions here, it may be None or unassigned
                continue

    if not all_transactions:
        return None, output_log

    combined_df = pd.concat(all_transactions, ignore_index=True)
    output_log += "\n❓ Would you like to proceed with these updates? If so, click below:\n"
    return combined_df, output_log