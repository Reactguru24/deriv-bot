# main.py
import asyncio
from api_client import init_api, get_candles
from trade_manager import execute_trade
from config import MODEL_PATH, SYMBOLS, GRANULARITY
from train_model import initialize_model, update_model

async def main():
    # Initialize API
    await init_api()

    # Initialize ML model
    model = initialize_model()
    print("[BOT] Loaded model, starting trading loop...")

    while True:
        for symbol in SYMBOLS:
            try:
                # Fetch latest candle
                candles = await get_candles(symbol, count=1, interval="1m")
                if candles.empty:
                    print(f"[WARNING] No candle data for {symbol}")
                    continue

                candle = candles.iloc[-1]

                # Safely extract open/close (handle missing fields)
                open_price = float(candle.get("open", 0))
                close_price = float(candle.get("close", 0))

                # Make prediction
                prediction = model.predict([[open_price, close_price]])[0]

                # Execute trade based on prediction
                await execute_trade(prediction, symbol)

                # Prepare data to update model
                X_new = [[open_price, close_price]]
                y_new = [prediction]  # For now using predicted as label; replace with actual trade result if available

                # Update ML model
                model = update_model(model, X_new, y_new)

            except Exception as e:
                print(f"[ERROR] Failed processing {symbol}: {e}")

        # Wait for next candle
        await asyncio.sleep(GRANULARITY)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[BOT] Stopped manually.")
