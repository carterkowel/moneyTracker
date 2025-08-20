import os
import json

def load_credit_cards():
    """Load credit card options from config file"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "credit_cards.json")

    with open(config_path, "r") as f:
        return json.load(f)
