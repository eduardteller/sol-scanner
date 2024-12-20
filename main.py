# File: solana_token_data.py

import asyncio
from textwrap import indent
import time
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solana.rpc.types import MemcmpOpts
import math
import requests
import json
import textwrap
import time
from datetime import datetime


async def main():
    # token_address = input("Enter Solana token address: ").strip()
    token_address = "DJgt7U4nCBsxox7MD9H3HikMA8soGWuqo287Pxjcpump"

    # async with AsyncClient("https://api.mainnet-beta.solana.com") as client:
    #     pubkey = Pubkey.from_string(token_address)
    #     token_supply = await client.get_token_supply(pubkey)
    #     account_info = await client.get_account_info(pubkey)
    #     rounded_supply = math.ceil(token_supply.value.ui_amount)
    #     print(f"Token supply: {rounded_supply}")
    #     print(f"{account_info.value.data}")

    #     if account_info.value:
    #         data = account_info.value.data

    #         mint_authority_key = Pubkey(bytes(data[:32]))
    #         print("Mint Authority Address:", mint_authority_key)

    #         current_supply = int.from_bytes(data[32:40], "little")
    #         print("Current Token Supply:", current_supply)
    #     else:
    #         print("Token mint account not found.")

    response = requests.get(
        f"https://api.dexscreener.com/latest/dex/tokens/{token_address}",
    )

    data = response.json()

    if data["pairs"] == None:
        print("No DEX")
        return

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

    if pair["priceChange"]["h1"] < 0:
        price_change = f"{price_change}% 🔻"
    else:
        price_change = f"{price_change}% 🔼"

    message = textwrap.dedent(
        f"""
        💊 {name} • ${symbol}
        {token_address}
        
        🕒 Age: {age}
        💰 MC: ${mcap}
        💧 Liq: ${liq}
        💲 Price: ${price}

        🕊️ ATH: ...
        📈 Vol: 1h: ${vol}
        📈 Price: 1h: {price_change}

        🦅 Dex ({url}): Paid✅ {boosts}
        ⚡️ Scans: ... | 🔗 {links}
    
    """
    )

    print(message)


def format_values(value) -> str:
    if value > 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif value > 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif value > 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return f"{value}"


def get_boosts(value) -> str:
    if "boosts" in value and value["boosts"]:
        boosts = f"{value['boosts']['active']} ⚡️"
    else:
        boosts = ""

    return boosts


def get_socials(data) -> str:
    value = data["info"]
    if "socials" not in value or not value["socials"]:
        print("No socials")
        return ""

    for social in value["socials"]:
        string_of_socials = ""
        if social["type"] == "twitter":
            string_of_socials = f"TW ({social['url']})"
        elif social["type"] == "telegram":
            string_of_socials = f"{string_of_socials} | TG ({social['url']})"

    return string_of_socials


def format_time(pair_time) -> str:
    timestamp1 = time.time()
    timestamp2 = pair_time / 1000

    # Convert to datetime objects
    datetime1 = datetime.fromtimestamp(timestamp1)
    datetime2 = datetime.fromtimestamp(timestamp2)

    time_diff = datetime1 - datetime2

    # Extract total seconds
    total_seconds = int(time_diff.total_seconds())

    # Calculate days, hours, minutes, and seconds
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format the output
    if days > 0:
        formatted_time_diff = f"{days}D"
    elif hours > 0:
        formatted_time_diff = f"{hours}H"
    elif minutes > 0:
        formatted_time_diff = f"{minutes}M"
    else:
        formatted_time_diff = f"{seconds}S"

    return formatted_time_diff


if __name__ == "__main__":
    asyncio.run(main())
