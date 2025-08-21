import os
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

# Demo mode: True if MONEYTRACKER_MODE=demo, else False
DEMO_MODE = os.getenv("MONEYTRACKER_MODE", "prod") == "demo"
