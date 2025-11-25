# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env automatically

API_TOKEN = os.getenv("API_TOKEN")
APP_ID = os.getenv("APP_ID", "1089")
DEMO_MODE = True

if not API_TOKEN:
    raise ValueError("API_TOKEN not found in .env")

SYMBOLS = ["R_100", "R_75", "R_50"]  # valid demo symbols
GRANULARITY = 60  # 1-minute candles
TRADE_RISK = 0.02  # Risk 2% of balance per trade

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env")

DB_NAME = "deriv_bot_db"
MODEL_PATH = "models/model.pkl"
