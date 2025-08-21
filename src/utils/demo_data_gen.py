import os
import random
import pandas as pd
from datetime import datetime, timedelta

CATEGORIES = {
    "Groceries": [
        "hmart", "no frills", "save on foods", "safeway",
        "superstore", "loblaws", "t&t supermarket", "walmart",
        "marketplace iga", "persia foods", "whole foods", "solo market",
        "bosa foods", "kin's farm", "east west market", "real canadian superstore",
        "costco", "cobs", "food hub market"
    ],
    "Miscellaneous": [],
    "Recreation/entertainment": [
        "cineplex", "rec room", "grandview lanes", "escape room", "solo karaoke",
        "bicycle rentals", "pne", "concert"
    ],
    "Restaurants": [
        "mcdonald's", "tim hortons", "a&w", "subway", "pho", "sushi",
        "ramen", "pizza", "cafe", "tacos", "pub", "grill", "burger",
        "restaurant", "chai", "hotpot", "noodles", "gelato", "kfc",
        "cactus club", "uber eats", "door dash"
    ],
    "Shopping": [
        "aritzia", "urban outfitters", "gap", "nike", "winners", "thrift",
        "vintage", "shoppers drug mart", "london drugs", "amazon", "dollarama",
        "ikea", "uniqlo", "muji"
    ],
    "Transportation": [
        "uber", "lyft", "evo", "mobi", "transit", "honk", "parking",
        "compass", "taxi", "shell", "esso"
    ],
    "Travel": [
        "air canada", "westjet", "flair", "amtrak", "airbnb",
        "bc ferries", "yvr", "airport", "lufthansa"
    ],
    "Wellbeing/Health Care": [
        "pharmacy", "clinic", "physio", "massage", "dentist", "dental", "health"
    ]
}

NECESSITY = {
    "Needs": ["Groceries", "Transportation", "Wellbeing/Health Care"],
    "Wants": ["Restaurants", "Shopping", "Travel", "Miscellaneous", "Recreation/entertainment"]
}

CATEGORY_WEIGHTS = {
    "Groceries": 12,
    "Restaurants": 10,
    "Shopping": 6,
    "Transportation": 8,
    "Travel": 2,
    "Wellbeing/Health Care": 3,
    "Recreation/entertainment": 3,
    "Miscellaneous": 1
}

CATEGORY_AMOUNTS = {
    "Groceries": (20, 150),
    "Restaurants": (10, 60),
    "Shopping": (15, 200),
    "Transportation": (3, 50),
    "Travel": (50, 600),
    "Wellbeing/Health Care": (20, 120),
    "Recreation/entertainment": (15, 100),
    "Miscellaneous": (5, 80)
}

def generate_transactions(start_date="2023-01-01", end_date="2024-12-31"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    days = (end - start).days + 1

    records = []

    for day_offset in range(days):
        date = start + timedelta(days=day_offset)

        # Random number of transactions per day (0–3)
        num_txns = random.choices([0, 1, 2, 3], weights=[0.5, 0.3, 0.15, 0.05])[0]
        for _ in range(num_txns):
            category = random.choices(
                list(CATEGORY_WEIGHTS.keys()),
                weights=CATEGORY_WEIGHTS.values()
            )[0]

            if not CATEGORIES[category]:
                desc = "misc expense"
            else:
                desc = random.choice(CATEGORIES[category])

            amount = round(random.uniform(*CATEGORY_AMOUNTS[category]), 2)

            necessity = "Needs" if category in NECESSITY["Needs"] else "Wants"

            records.append([
                date.strftime("%Y-%m-%d"),
                amount,
                desc,
                "demo_card",
                category,
                necessity
            ])

    return pd.DataFrame(records, columns=["Date", "Amount", "Description", "Card", "Category", "Necessity"])

if __name__ == "__main__":
    df = generate_transactions()

    # Ensure output directory exists
    output_dir = os.path.join("src", "data", "demo")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "demo.csv")
    df.to_csv(output_path, index=False)

    print(f"✅ Demo data generated: {output_path} ({len(df)} rows)")
