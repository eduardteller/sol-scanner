import textwrap
from aiohttp import ClientSession
import API_KEYS
import math
from modules.raydium import get_lp_burn
from modules.birdeye import get_birdeye_data
from modules.data_processing import format_values, format_time
import asyncio


async def exec_main(address: str) -> str:

    session = ClientSession()
    try:
        final = await start_routine(address, session)
        # print(final["text"])
        return final

    except Exception as e:
        print(f"ERROR exec_main: {e}")
        exit(1)

    finally:
        await session.close()


async def is_valid_image_url(session: ClientSession, url: str) -> bool:
    try:
        async with session.head(url, timeout=5) as response:
            if response.status != 200:
                return False

            content_type = response.headers.get("Content-Type", "")
            return content_type.startswith("image/")
    except Exception as e:
        return False


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


async def start_routine(
    address: str,
    session: ClientSession,
) -> str:
    try:
        birdeye, burn, dex = await asyncio.gather(
            get_birdeye_data(address, session),
            get_lp_burn(session, address),
            get_dex(session, address),
        )

        print(birdeye["creation_time"])

        if not birdeye:
            raise Exception("Failed to fetch data")

        if not dex:
            dex_type = "💊"

        else:
            if dex["dexId"] == "pumpfun":
                dex_type = "💊"
            elif dex["dexId"] == "moonshot":
                dex_type = "🌕"
            else:
                dex_type = "💠"

        if dex and not (dex["dexId"] == "pumpfun"):
            price_change_h = (
                f"{dex['priceChange']['h1']}% 🔻"
                if dex["priceChange"]["h1"] < 0
                else f"{dex['priceChange']['h1']}% 🔼"
            )
            price_change_d = (
                f"{dex['priceChange']['h24']}% 🔻"
                if dex["priceChange"]["h24"] < 0
                else f"{dex['priceChange']['h24']}% 🔼"
            )

        if not dex or dex["dexId"] == "pumpfun":
            return_message = f"""\
            {dex_type}  **{birdeye["name"]}** • **${(birdeye["symbol"].upper())}**
            `{address}`
            
            ➕  **Mint**: {"No ✅" if not birdeye['mint'] else "Yes 🚨"} | 🧊 **Freeze**: {"No ✅" if not birdeye['freeze'] else "Yes 🚨"}
            
            🕒  **Age**: {format_time(birdeye['creation_time'])} 
            💵  **Price**: ${birdeye['price']:.10f}
            💰  **MC**: ${format_values(birdeye['mcap'])}

            🕊️  **ATH**: ${format_values(birdeye['ath'])} ({(birdeye['ath'] / birdeye['mcap']):.2f}X)

            🔗  {f"[X]({birdeye['twitter']})" if birdeye['twitter'] else ""} {f"[T]({birdeye['telegram']})" if birdeye['telegram'] else ""} {f"[W]({birdeye['website']})" if birdeye['website'] else ""}
            👥  [Hodls](https://solscan.io/token/{address}#holders): {birdeye['holders']} {f"| Top: {birdeye['top_10_holder_percent']}%"}

            🛠️ [Dev](https://solscan.io/account/{birdeye['creator_address']}) : {birdeye['creator_balance']} SOL | {birdeye['creator_percentage']}% ${(birdeye['symbol'].upper())}
            
            📊 **Chart**  [DEX](https://dexscreener.com/solana/{address}) | [Phtn](https://photon-sol.tinyastro.io/en/lp/{address}) | [Brdeye](https://www.birdeye.so/token/{address}?chain=solana)
            """

        elif dex["dexId"] == "moonshot":
            return_message = f"""\
            {dex_type}  **{birdeye["name"]}** • **${(birdeye["symbol"].upper())}**
            `{address}`
            
            ➕  **Mint**: {"No ✅" if not birdeye['mint'] else "Yes 🚨"} | 🧊 **Freeze**: {"No ✅" if not birdeye['freeze'] else "Yes 🚨"}
            
            🕒  **Age**: {format_time(birdeye['creation_time'])} 
            💵  **Price**: ${birdeye['price']:.10f}
            💰  **MC**: ${format_values(birdeye['mcap'])}

            📈  **Vol**: 1h: ${format_values(dex["volume"]["h1"])} | 1d: ${format_values(dex["volume"]["h24"])}
            📈  **Price**: 1h: {price_change_h} | 1d: {price_change_d}

            🔗  {f"[X]({birdeye['twitter']})" if birdeye['twitter'] else ""} {f"[T]({birdeye['telegram']})" if birdeye['telegram'] else ""} {f"[W]({birdeye['website']})" if birdeye['website'] else ""}
            👥  [Hodls](https://solscan.io/token/{address}#holders): {birdeye['holders']} {f"| Top: {birdeye['top_10_holder_percent']}%"}

            🛠️ [Dev](https://solscan.io/account/{birdeye['creator_address']}) : {birdeye['creator_balance']} SOL | {birdeye['creator_percentage']}% ${(birdeye['symbol'].upper())}
            
            📊 **Chart**  [DEX](https://dexscreener.com/solana/{address}) | [Phtn](https://photon-sol.tinyastro.io/en/lp/{address}) | [Brdeye](https://www.birdeye.so/token/{address}?chain=solana)
            """

        else:
            return_message = f"""\
            {dex_type}  **{birdeye["name"]}** • **${(birdeye["symbol"].upper())}**
            `{address}`
            
            ➕  **Mint**: {"No ✅" if not birdeye['mint'] else "Yes 🚨"} | 🧊 **Freeze**: {"No ✅" if not birdeye['freeze'] else "Yes 🚨"}
            🌊  LP: {math.floor(burn)}% Burnt
            
            🕒  **Age**: {format_time(birdeye['creation_time'])} 
            💵  **Price**: ${birdeye['price']:.10f}
            💰  **MC**: ${format_values(birdeye['mcap'])} | **FDV**: ${format_values(birdeye['fdv'])}
            💧  **Liq**: ${format_values(birdeye['liquidity'])} ({math.floor(birdeye['liquidity'] / birdeye['sol_price'])} SOL)

            🕊️  **ATH**: ${format_values(birdeye['ath'])} ({(birdeye['ath'] / birdeye['mcap']):.2f}X)
            📈  **Vol**: 1h: ${format_values(dex["volume"]["h1"])} | 1d: ${format_values(dex["volume"]["h24"])}
            📈  **Price**: 1h: {price_change_h} | 1d: {price_change_d}

            🔗  {f"[X]({birdeye['twitter']})" if birdeye['twitter'] else ""} {f"[T]({birdeye['telegram']})" if birdeye['telegram'] else ""} {f"[W]({birdeye['website']})" if birdeye['website'] else ""}
            👥  [Hodls](https://solscan.io/token/{address}#holders): {birdeye['holders']} {f"| Top: {birdeye['top_10_holder_percent']}%"}

            🛠️ [Dev](https://solscan.io/account/{birdeye['creator_address']}) : {birdeye['creator_balance']} SOL | {birdeye['creator_percentage']}% ${(birdeye['symbol'].upper())}
            
            📊 **Chart**  [DEX](https://dexscreener.com/solana/{address}) | [Phtn](https://photon-sol.tinyastro.io/en/lp/{address}) | [Brdeye](https://www.birdeye.so/token/{address}?chain=solana)
            """

        return {
            "icon": birdeye["icon"],
            "text": textwrap.dedent(return_message),
        }

    except Exception as e:
        print(f"ERROR MAIN ROUTINE: {e}")
        return None


# exec_main("9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump")
# asyncio.run(exec_main("BoEy2KhaWGgBCZNjBZX7RXKHuB8qWV37H4qYj97hpump"))
# asyncio.run(exec_main("BNu5McPaw1YUfLcsxKoQtiurvM33rA7jsW1rdYM2moon"))
