# api_client.py
import asyncio
import pandas as pd
from deriv_api import DerivAPI
from config import API_TOKEN, APP_ID, DEMO_MODE

api: DerivAPI | None = None
authorized: bool = False


async def init_api():
    """
    Initialize Deriv WebSocket API and authorize account.
    Handles demo/real mode automatically.
    """
    global api, authorized

    if not API_TOKEN:
        raise ValueError("API_TOKEN is missing. Set it in your .env file.")

    print("[INIT] Connecting to Deriv API...")

    # Initialize API
    api = DerivAPI(access_token=API_TOKEN if not DEMO_MODE else None, app_id=APP_ID, demo=DEMO_MODE)
    await api.api_connect()

    # Authorize account
    auth_response = await api.authorize(API_TOKEN)
    if "error" in auth_response:
        raise Exception(f"[AUTH ERROR] {auth_response['error']['message']}")

    authorized = True
    account = auth_response["authorize"]
    print(f"[INIT] Logged in successfully as {account.get('email')}")
    print(f"[INIT] Balance: {account.get('balance')}")


async def get_account_info() -> dict:
    """
    Get authorized account info.
    Returns: dict with email, account_name, balance
    """
    global api, authorized
    if api is None or not authorized:
        raise RuntimeError("API not initialized. Call init_api() first.")

    try:
        response = await api.authorize(API_TOKEN)
        account = response.get("authorize", {})
        return {
            "email": account.get("email", "N/A"),
            "account_name": account.get("fullname", "N/A"),
            "balance": float(account.get("balance", 0)),
        }
    except Exception as e:
        print(f"[ERROR] Failed to get account info: {e}")
        return {"email": "N/A", "account_name": "N/A", "balance": 0}


async def get_candles(symbol, count=100, interval="1m"):
    """Fetch candle data from Deriv."""
    global api

    if api is None:
        raise RuntimeError("API not initialized.")

    interval_map = {
        "1m": 60,
        "5m": 300,
        "15m": 900,
        "1h": 3600,
        "1d": 86400,
    }

    granularity = interval_map.get(interval, 60)

    try:
        response = await api.ticks_history(
            args={
                "ticks_history": symbol,
                "count": count,
                "style": "candles",
                "granularity": granularity,
                "end": "latest",
            }
        )

        candles = response.get("candles", [])
        if not candles:
            print(f"[WARNING] No candle data for {symbol}")
            return pd.DataFrame()

        # Some candles might not have volume, handle safely
        for candle in candles:
            candle.setdefault("volume", 0)

        df = pd.DataFrame(candles)
        df["close"] = df["close"].astype(float)
        df["open"] = df["open"].astype(float)

        return df

    except Exception as e:
        print(f"[ERROR] Failed to fetch candles for {symbol}: {e}")
        return pd.DataFrame()


async def place_trade(symbol: str, direction: str, amount: float, duration: int) -> str:
    """
    Place a trade on Deriv.
    Returns: "WIN", "LOSS", "UNKNOWN", or "ERROR"
    """
    global api
    if api is None:
        raise RuntimeError("API not initialized.")

    contract_type = "CALL" if direction.upper() == "BUY" else "PUT"

    try:
        trade = await api.buy(
            {
                "contract": symbol,
                "contract_type": contract_type,
                "amount": amount,
                "duration": duration,
                "duration_unit": "m",
            }
        )
        result = trade.get("contract", {}).get("status")
        print(f"[TRADE] Placed {direction} on {symbol} amount {amount}")

        if result in ["won", "profit"]:
            return "WIN"
        elif result in ["lost", "loss"]:
            return "LOSS"
        return "UNKNOWN"

    except Exception as e:
        print(f"[ERROR] Failed to place trade: {e}")
        return "ERROR"
