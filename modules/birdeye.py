from aiohttp import ClientSession
import math
import API_KEYS
import asyncio
import time

ONE_DAY = 86400
birdeye_api_url = "https://public-api.birdeye.so/"

birdeye_headers = {
    "accept": "application/json",
    "x-chain": "solana",
    "X-API-KEY": API_KEYS.BIRDEYE_API,
}


async def get_all_time_high(address: str, supply: int, session: ClientSession) -> float:
    try:

        url = f"{birdeye_api_url}defi/ohlcv?address={address}&type=1M&time_from=0&time_to={math.ceil(time.time())}"

        birdeye_price_data_raw = await session.get(url, headers=birdeye_headers)

        birdeye_price_data = await birdeye_price_data_raw.json()

        if not birdeye_price_data["success"]:
            raise Exception("Failed to fetch price data")

        max_price2 = max(item["h"] for item in birdeye_price_data["data"]["items"])

        return math.floor(float(max_price2) * supply)

    except Exception as e:
        print(f"ERROR ALL TIME HIGH: {e}")
        return 0


async def get_sol_price(session: ClientSession) -> float:
    try:

        url = f"{birdeye_api_url}defi/price?include_liquidity=true&address=So11111111111111111111111111111111111111112"
        sol_price_resp = await session.get(url, headers=birdeye_headers)
        sol_price_resp_json = await sol_price_resp.json()

        if not sol_price_resp_json["success"]:
            raise Exception("Failed to fetch SOL price")

        sol_price = float(sol_price_resp_json["data"]["value"])

        return sol_price
    except Exception as e:
        print(f"ERROR SOL PRICE: {e}")
        return 0


async def get_dev_balance(account: str, session: ClientSession) -> str:
    try:
        get_balance_url = f"{birdeye_api_url}v1/wallet/token_list?wallet={account}"

        get_balance_resp = await session.get(get_balance_url, headers=birdeye_headers)
        get_balance_resp_json = await get_balance_resp.json()

        if not get_balance_resp_json["success"]:
            raise Exception("Failed to fetch balance data")

        balance = float(get_balance_resp_json["data"]["totalUsd"])

        return balance
    except Exception as e:
        print(f"ERROR DEV BALANCE: {e}")
        return "0"


async def get_security(address: str, session: ClientSession) -> int:
    try:
        url = f"{birdeye_api_url}defi/token_security?address={address}"
        resp = await session.get(url, headers=birdeye_headers)
        data = await resp.json()

        if not data["success"]:
            raise Exception("Failed to fetch security data")

        security_data = data["data"]

        creator_address = str(security_data["creatorAddress"])
        creationTime = int(security_data["creationTime"])
        creatorPercentage = int(security_data["creatorPercentage"] * 100)
        top10HolderPercent = int(security_data["top10HolderPercent"] * 100)
        freezeable = bool(
            security_data.get("freezeable", False)
            or security_data.get("freezeAuthority", False)
        )
        mintable = security_data.get("metaplexUpdateAuthority", False)

        if not (
            mintable == "TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM"
            or mintable == "11111111111111111111111111111111"
        ):
            mintable = True
        else:
            mintable = False

        return {
            "creator_address": creator_address,
            "creation_time": creationTime,
            "creator_percentage": creatorPercentage,
            "top_10_holder_percent": top10HolderPercent,
            "freeze": freezeable,
            "mint": mintable,
        }
    except Exception as e:
        print(f"ERROR DEV TOKEN BALANCE: {e}")
        return 0


async def get_meta_pump(address: str, session: ClientSession) -> int:
    try:
        url = f"{birdeye_api_url}defi/token_security?address={address}"
        resp = await session.get(url, headers=birdeye_headers)
        data = await resp.json()

        if not data["success"]:
            raise Exception("Failed to fetch security data")

        security_data = data["data"]

        creator_address = str(security_data["creatorAddress"])
        creationTime = int(security_data["creationTime"])
        creatorPercentage = int(security_data["creatorPercentage"] * 100)
        top10HolderPercent = int(security_data["top10HolderPercent"] * 100)
        freezeable = bool(
            security_data.get("freezeable", False)
            or security_data.get("freezeAuthority", False)
        )
        mintable = security_data.get("metaplexUpdateAuthority", False)

        if not (
            mintable == "TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM"
            or mintable == "11111111111111111111111111111111"
        ):
            mintable = True
        else:
            mintable = False

        return {
            "creator_address": creator_address,
            "creation_time": creationTime,
            "creator_percentage": creatorPercentage,
            "top_10_holder_percent": top10HolderPercent,
            "freeze": freezeable,
            "mint": mintable,
        }
    except Exception as e:
        print(f"ERROR DEV TOKEN BALANCE: {e}")
        return 0


async def get_dex(session: ClientSession, address: str) -> bool:
    try:
        birdeye_headers = {
            "accept": "application/json",
            "x-chain": "solana",
            "X-API-KEY": API_KEYS.BIRDEYE_API,
        }
        url = f"https://api.dexscreener.com/tokens/v1/solana/{address}"
        resp = await session.get(url, headers=birdeye_headers)
        data = await resp.json()

        if not data or not data[0]:
            raise Exception("Failed to fetch data")

        return data[0]
    except Exception as e:
        print(f"ERROR DEX: {e}")
        return False


async def moonshot_holders(session: ClientSession, address: str) -> bool:
    try:
        birdeye_headers = {
            "accept": "application/json",
            "x-chain": "solana",
            "X-API-KEY": API_KEYS.BIRDEYE_API,
        }
        url = f"https://public-api.birdeye.so/defi/v3/token/trade-data/single?address={address}"
        resp = await session.get(url, headers=birdeye_headers)
        data = await resp.json()

        if not data["success"]:
            raise Exception("Failed to fetch data")

        return int(data["data"]["holder"])
    except Exception as e:
        print(f"ERROR DEX: {e}")
        return False


async def get_birdeye_data(
    address: str,
    session: ClientSession,
):
    try:
        token_meta_url = f"{birdeye_api_url}defi/token_overview?address={address}"

        solscan_token_meta_resp = await session.get(
            token_meta_url, headers=birdeye_headers
        )
        solscan_token_meta_resp = await solscan_token_meta_resp.json()

        if not solscan_token_meta_resp["success"]:
            raise Exception("Failed to fetch token meta data")

        token_data = solscan_token_meta_resp["data"]

        if not token_data:
            data = await get_dex(session, address)

            # meta
            token_name = data["baseToken"]["name"]
            token_symbol: str = data["baseToken"]["symbol"]
            token_icon_url = data["info"]["imageUrl"]

            # price/cap
            token_mcap = int(data["fdv"])
            token_fdv = int(data["fdv"])
            token_price = float(data["priceUsd"])

            token_supply = 1000000000
            token_supply_decimals = 0
            token_liq = 0

            twitter = None
            website = None
            telegram = None

            if "websites" in data["info"] and len(data["info"]["websites"]):
                website = data["info"]["websites"][0]["url"]

            if "socials" in data["info"] and data["info"]["socials"]:
                socials_dict = {
                    social["type"]: social["url"]
                    for social in data["info"]["socials"]
                    if "type" in social and "url" in social
                }
                twitter = socials_dict.get("twitter")
                telegram = socials_dict.get("telegram")

            # holders
            token_holders = await moonshot_holders(session, address)

        else:
            # meta
            token_name = token_data["name"]
            token_symbol: str = token_data["symbol"]
            token_icon_url = token_data["logoURI"]

            # price/cap
            token_mcap = int(token_data["realMc"])
            token_fdv = int(token_data["mc"])
            token_price = float(token_data["price"])
            token_supply_decimals = int(token_data["decimals"])
            token_supply = int(token_data["supply"])
            token_liq = int(token_data["liquidity"])

            socials = token_data["extensions"]

            twitter = None
            website = None
            telegram = None

            print(socials)

            if socials:
                twitter = socials["twitter"] if "twitter" in socials else None
                website = socials["website"] if "website" in socials else None
                telegram = socials["telegram"] if "telegram" in socials else None

            # holders
            token_holders = int(token_data["holder"])

        ath, security, sol_price, dev_balance_usd = await asyncio.gather(
            get_all_time_high(
                address,
                token_supply,
                session=session,
            ),
            get_security(address, session),
            get_sol_price(session),
            get_dev_balance(address, session),
        )

        dev_balance_sol = int(dev_balance_usd / sol_price)

        return_object = {
            "name": token_name,
            "symbol": token_symbol,
            "icon": token_icon_url,
            "mcap": token_mcap,
            "fdv": token_fdv,
            "price": token_price,
            "supply": token_supply,
            "supply_decimals": token_supply_decimals,
            "liquidity": token_liq,
            "holders": token_holders,
            "ath": ath,
            "creator_address": security["creator_address"],
            "creation_time": security["creation_time"],
            "creator_percentage": security["creator_percentage"],
            "creator_balance": dev_balance_sol,
            "top_10_holder_percent": security["top_10_holder_percent"],
            "freeze": security["freeze"],
            "mint": security["mint"],
            "twitter": twitter,
            "website": website,
            "telegram": telegram,
            "sol_price": sol_price,
        }

        return return_object

    except Exception as e:
        print(f"ERROR BIRDEYE: {e}")
        return None
