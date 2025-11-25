import asyncio
from api_client import init_api, api
from db import candles_collection
from config import SYMBOLS, GRANULARITY

async def collect_candles():
    await init_api()
    print("[COLLECTOR] Subscribing to candles...")

    for symbol in SYMBOLS:
        asyncio.create_task(subscribe_symbol(symbol))

async def subscribe_symbol(symbol):
    sub = await api.subscribe({
        "ticks_history": symbol,
        "style": "candles",
        "granularity": GRANULARITY,
        "count": 1,
        "subscribe": 1
    })

    async for msg in sub:
        candle = msg.get("candles", [None])[0]
        if candle:
            candle["symbol"] = symbol
            candles_collection.insert_one(candle)
            print(f"[DB] Saved {symbol} candle: {candle}")

if __name__ == "__main__":
    asyncio.run(collect_candles())
