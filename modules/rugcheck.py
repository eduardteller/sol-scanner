from aiohttp import ClientSession


async def get_rugcheck_score(session: ClientSession, address: str):
    url = f"https://api.rugcheck.xyz/v1/tokens/{address}/report/summary"
    headers = {"Content-Type": "application/json"}
    try:
        async with session.get(url, headers=headers) as response:
            return await response.json()
    except Exception as e:
        return {"error": str(e)}
