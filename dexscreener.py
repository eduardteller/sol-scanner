import requests
import textwrap
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from data_processing import format_values, format_time
from get_mint_and_freeze import get_mint_and_freeze_authority
from holders import get_holders
from largest_accounts import get_largest_wallets
import json
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
            string_of_socials = f"TW ({social['url']})"
        elif social["type"] == "telegram":
            string_of_socials += f" | TG ({social['url']})"

    if value["websites"][0]:
        string_of_socials += f" | WEB ({value['websites'][0]['url']})"

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

    pair = data["pairs"][0]
    name = pair["baseToken"]["name"]
    symbol = pair["baseToken"]["symbol"]
    url = pair["url"]
    price = pair["priceUsd"]
    mcap = format_values(pair["marketCap"])
    age = format_time(pair["pairCreatedAt"])
    liq = format_values(pair["liquidity"]["usd"])
    price_change = pair["priceChange"]["h1"]
    vol = format_values(pair["volume"]["h1"])
    boosts = get_boosts(pair)
    links = get_socials(pair)

    authority = get_mint_and_freeze_authority(client, pub)

    holders = get_holders(client, address)

    wallets = get_largest_wallets(client, pub)

    wallets_string = get_20_wallets(wallets["wallets"])

    if pair["priceChange"]["h1"] < 0:
        price_change = f"{price_change}% 🔻"
    else:
        price_change = f"{price_change}% 🔼"

    message = textwrap.dedent(
        f"""
        🐦‍⬛  {name} • ${symbol}
        {address}
        
        {authority}
        
        🕒  Age: {age}
        💰  MC: ${mcap}
        💧  Liq: ${liq}(...)
        💲  Price: ${price}

        📈  Vol: 1h: ${vol} | 1d: ...
        📈  Price: 1h: {price_change} | 1d ...

        🦅  Dex ({url}): Paid✅ {boosts}
        ⚡️  Scans: ... | 🔗 {links}
        👥  Hodls (https://solscan.io/token/{address}#holders): {holders}
        
        🔫 Snipers: ...🚨
        🎯 Top 20 wallets hold: {math.floor(wallets["percent"])}%
        {wallets_string}
        
        📊 Chart  DEX (https://dexscreener.com/solana/{address}) | Phtn (https://photon-sol.tinyastro.io/en/lp/{address}) | Brdeye (https://www.birdeye.so/token/{address}?chain=solana)
        """
    )

    return message
