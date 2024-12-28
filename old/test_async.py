import aiohttp
import asyncio
from asyncio import as_completed
from raydium import get_lp_burn
from rugcheck import get_rugcheck_score
import time
import datetime


async def fetch_data(session, url):
    try:
        async with session.get(url) as response:
            return await response.json()
    except Exception as e:
        return {"error": str(e)}


async def process_endpoints():
    async with aiohttp.ClientSession() as session:
        tasks = [
            get_lp_burn(session, "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump"),
            get_rugcheck_score(session, "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump"),
        ]
        for future in as_completed(tasks):
            result = await future
            # Process each result as it arrives
            if "error" not in result:
                process_result(result)
            else:
                print("Error", result)


def process_result(data):
    # Handle the data processing here
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print("OK", current_time)


# Usage
async def main():
    await process_endpoints()


if __name__ == "__main__":
    asyncio.run(main())
