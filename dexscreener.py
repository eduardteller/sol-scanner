import requests
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from data_processing import format_values, format_time
from get_mint_and_freeze import get_mint_and_freeze_authority
from holders import get_holders
from largest_accounts import get_largest_wallets
from my_types import SolscanData
from solscan import solscan_start, solana_price
import math
from typing import List


def get_20_wallets(wallets: List[str]) -> str:
    return_string = ""
    for i, idx in enumerate(wallets):
        return_string += f"[🐳](https://solscan.io/account/{idx})"
        if i == 10:
            return_string += "\n"

    return return_string


def get_boosts(value) -> str:
    if "boosts" in value and value["boosts"]:
        boosts = f"| {value['boosts']['active']} ⚡️"
    else:
        boosts = ""

    return boosts


def get_socials(data) -> str:
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


def dexscreener_routine(address: str, client: Client) -> str:
    response = requests.get(
        f"https://api.dexscreener.com/latest/dex/tokens/{address}",
    )

    pub = Pubkey.from_string(address)

    data = response.json()

    if not data["pairs"]:
        return "pumpfun"

    if "moonshot" in data["pairs"][0]:
        return "moonshot"

    sol_data: SolscanData = solscan_start(client, address, pub)
    sol_price: float = solana_price()

    pair = data["pairs"][0]

    name = pair["baseToken"]["name"]
    symbol: str = pair["baseToken"]["symbol"]
    price = pair["priceUsd"]
    # mcap_raw = pair["marketCap"]
    # mcap = format_values(pair["marketCap"])
    liq_raw = pair["liquidity"]["usd"]
    liq = format_values(pair["liquidity"]["usd"])
    price_change_h = pair["priceChange"]["h1"]
    vol_h = format_values(pair["volume"]["h1"])
    price_change_d = pair["priceChange"]["h24"]
    vol_d = format_values(pair["volume"]["h24"])
    boosts = get_boosts(pair)
    links = get_socials(pair)
    # age = format_time(pair["pairCreatedAt"])

    wallets_string = get_20_wallets(sol_data.token_top20_wallets.wallets)

    if price_change_h < 0:
        price_change_h = f"{price_change_h}% 🔻"
    else:
        price_change_h = f"{price_change_h}% 🔼"

    if price_change_d < 0:
        price_change_d = f"{price_change_d}% 🔻"
    else:
        price_change_d = f"{price_change_d}% 🔼"

    # message = textwrap.dedent(
    #     f"""
    # 🐦‍⬛  {name} • ${symbol}
    # `{address}`

    # {authority}

    # 🕒  Age: {age}
    # 💰  MC: ${mcap}
    # 💧  Liq: ${liq}(...)
    # 💲  Price: ${price}

    # 📈  Vol: 1h: ${vol} | 1d: ...
    # 📈  Price: 1h: {price_change} | 1d ...

    # 🦅  [Dex]({url}): Paid✅ {boosts}
    # ⚡️  Scans: ... | 🔗 {links}
    # 👥  [Hodls](https://solscan.io/token/{address}#holders): {holders}

    # 🔫 Snipers: ...🚨
    # 🎯 Top 20 wallets hold: {math.floor(wallets["percent"])}%
    # {wallets_string}

    # 📊 Chart  [DEX](https://dexscreener.com/solana/{address}) | [Phtn](https://photon-sol.tinyastro.io/en/lp/{address}) | [Brdeye](https://www.birdeye.so/token/{address}?chain=solana)
    # """
    # )

    message2 = f"""\
    💠  {name} • ${(symbol.upper())}
    `{address}`
    
    ➕  Mint: {"No 🤍" if not sol_data.token_mint_auth else "Yes 🚨"} | 🧊 Freeze: {"No 🤍" if not sol_data.token_freeze_auth else "Yes 🚨"}

    🕒  Age: {sol_data.token_age} 
    💵  Price: ${price}
    💰  MC: ${format_values(sol_data.token_mcap)}
    💧  Liq: ${liq} ({math.floor(liq_raw / sol_price)} SOL)

    🕊️  ATH: ${format_values(sol_data.token_ath)} ({(sol_data.token_ath / sol_data.token_mcap):.2f}X)
    📈  Vol: 1h: ${vol_h} | 1d: ${vol_d}
    📈  Price: 1h: {price_change_h} | 1d: {price_change_d}

    🦅  DexS: Paid✅ {f"{boosts}" if boosts else ""}
    ⚡️  Scans: ... | 🔗 {links}
    👥  Hodls: {sol_data.token_holders} | Top: {sol_data.token_top20_wallets.percent}%

    🎯  First 20: ... Fresh
    {wallets_string}

    🛠️ Dev : ... SOL | ...% $FARTCOIN
    ┗ Sniped: ...% 🤍
    
    📊 Chart  [DEX](https://dexscreener.com/solana/{address}) | [Phtn](https://photon-sol.tinyastro.io/en/lp/{address}) | [Brdeye](https://www.birdeye.so/token/{address}?chain=solana)
    """

    return message2
