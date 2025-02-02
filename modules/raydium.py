from aiohttp import ClientSession


async def get_lp_burn(session: ClientSession, address: str) -> float:
    url = f"https://api-v3.raydium.io/pools/info/mint?mint1={address}&poolType=all&poolSortField=liquidity&sortType=desc&pageSize=1&page=1"
    headers = {"Content-Type": "application/json"}

    try:
        async with session.get(url, headers=headers) as response:
            resp = await response.json()

            if not resp["success"] or resp["data"]["count"] == 0:
                return None

            burn_amount = float(resp["data"]["data"][0]["burnPercent"])

            return burn_amount
    except Exception as e:
        print(f"ERROR LP BURN: {e}")
        return None
