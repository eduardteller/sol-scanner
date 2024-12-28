import requests
import textwrap
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from modules.data_processing import format_values, format_time
from old.holders import get_holders
from modules.largest_accounts import get_largest_wallets
from dexscreener import format_wallets, get_social_links
import math


def moonshot_routine(address: str, client: AsyncClient) -> str:
    response = requests.get(
        f"https://api.dexscreener.com/latest/dex/tokens/{address}",
    )

    pub = Pubkey.from_string(address)

    data = response.json()

    pair = data["pairs"][0]
    name = pair["baseToken"]["name"]
    symbol = pair["baseToken"]["symbol"]
    price = pair["priceUsd"]
    mcap = format_values(pair["fdv"])
    age = format_time(pair["pairCreatedAt"])
    price_change = pair["priceChange"]["h1"]
    vol = format_values(pair["volume"]["h1"])
    links = get_social_links(pair)

    holders = get_holders(client, address)

    wallets = get_largest_wallets(client, pub)

    wallets_string = format_wallets(wallets["wallets"])

    if pair["priceChange"]["h1"] < 0:
        price_change = f"{price_change}% 🔻"
    else:
        price_change = f"{price_change}% 🔼"

    message = textwrap.dedent(
        f"""
    🌕  {name} • ${symbol}
    `{address}`
    
    🕒  Age: {age}
    💰  MC: ${mcap}
    💲  Price: ${price}

    📈  Vol: 1h: ${vol} | 1d: ...
    📈  Price: 1h: {price_change} | 1d ...

    ⚡️  Scans: ... | 🔗 {links}
    👥  [Hodls](https://solscan.io/token/{address}#holders): {holders}
    
    🔫 Snipers: ...
    🎯 Top 20 wallets hold: {math.floor(wallets["percent"])}%
    {wallets_string}
    
    📊 Chart  [DEX](https://dexscreener.com/solana/{address}) | [Phtn](https://photon-sol.tinyastro.io/en/lp/{address}) | [Brdeye](https://www.birdeye.so/token/{address}?chain=solana)
    """
    )

    return message
