# trade_manager.py
from api_client import api, get_account_info
from config import TRADE_RISK

async def execute_trade(prediction, symbol):
    """
    Places a trade based on the prediction.
    prediction: 1=UP (BUY), 0=DOWN (SELL)
    symbol: market symbol (e.g., "R_100")
    """
    if api is None:
        raise RuntimeError("API not initialized.")

    # Fetch current demo balance
    account_info = await get_account_info()
    balance = account_info['balance']
    if balance <= 0:
        print(f"[WARNING] Insufficient balance: {balance}. Skipping trade.")
        return

    direction = "BUY" if prediction == 1 else "SELL"
    amount = balance * TRADE_RISK  # Use percentage of current balance
    duration = 1  # minutes

    print(f"[TRADE] Placing {direction} trade on {symbol} amount={amount:.2f} (balance: {balance:.2f})")

    try:
        contract_type = "CALL" if direction == "BUY" else "PUT"
        trade = await api.buy({
            "contract": symbol,
            "contract_type": contract_type,
            "amount": amount,
            "duration": duration,
            "duration_unit": "m",
        })
        print("[TRADE RESULT]", trade)
    except Exception as e:
        print(f"[ERROR] Failed to place trade on {symbol}: {e}")
