# print_token_response.py
import asyncio
from api_client import init_api, get_account_info

async def print_response():
    await init_api()
    info = await get_account_info()
    print("[API INFO]", info)

if __name__ == "__main__":
    asyncio.run(print_response())
