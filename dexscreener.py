from modules.data_processing import format_values
from my_types import DexscreenerData
from aiohttp import ClientSession


def get_dex_boosts(value) -> str:
    if "boosts" in value and value["boosts"]:
        boosts = f"| {value['boosts']['active']} ⚡️"
    else:
        boosts = ""

    return boosts


def get_social_links(data) -> str:
    value = data["info"]
    if "socials" not in value or not value["socials"]:
        print("No socials")
        return ""

    string_of_socials = ""
    for social in value["socials"]:
        if social["type"] == "twitter":
            string_of_socials = f"[TW]({social['url']})"
        elif social["type"] == "telegram":
            string_of_socials += f" | [TG]({social['url']})"

    if value["websites"][0]:
        string_of_socials += f" | [WEB]({value['websites'][0]['url']})"

    return string_of_socials


async def exec_dexscreener(
    address: str, session: ClientSession
) -> DexscreenerData | str:
    try:
        dex_response = await session.get(
            f"https://api.dexscreener.com/latest/dex/tokens/{address}",
        )

        dex_data = await dex_response.json()

        if not dex_data["pairs"]:
            return "pumpfun"

        if "moonshot" in dex_data["pairs"][0]:
            return "moonshot"

        dex_pair = dex_data["pairs"][0]

        name = dex_pair["baseToken"]["name"]
        symbol: str = dex_pair["baseToken"]["symbol"]
        price = dex_pair["priceUsd"]
        liq = dex_pair["liquidity"]["usd"]
        price_change_h = dex_pair["priceChange"]["h1"]
        vol_h = format_values(dex_pair["volume"]["h1"])
        price_change_d = dex_pair["priceChange"]["h24"]
        vol_d = format_values(dex_pair["volume"]["h24"])
        boosts = get_dex_boosts(dex_pair)
        links = get_social_links(dex_pair)

        return DexscreenerData(
            name=name,
            symbol=symbol,
            price=price,
            liq=liq,
            price_change_h=price_change_h,
            vol_h=vol_h,
            price_change_d=price_change_d,
            vol_d=vol_d,
            boosts=boosts,
            links=links,
        )
    except Exception as e:
        return {"error": str(e)}
