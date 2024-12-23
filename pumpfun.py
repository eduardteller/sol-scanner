import requests
import textwrap
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from data_processing import format_values, format_time
from holders import get_holders
from largest_accounts import get_largest_wallets
from dexscreener import get_20_wallets, get_socials
from pump_creation_time import get_token_creation_time
from pump_metadata import get_pump_metadata
import math
from data_processing import format_time
import json


def pumpfun_routine(address: str, client: Client) -> str:
    pub = Pubkey.from_string(address)
    age = format_time(get_token_creation_time(pub, client))
    data = get_pump_metadata(address)

    info = data["result"]["token_info"]

    name = data["result"]["content"]["metadata"]["name"]
    symbol = data["result"]["content"]["metadata"]["symbol"]
    price = float(info["price_info"]["price_per_token"])
    decimals = int(info["decimals"])
    supply = int(info["supply"]) / 10**decimals
    mcap = format_values(supply * price)
    # links = get_socials(pair)

    holders = get_holders(client, address)

    wallets = get_largest_wallets(client, pub)

    wallets_string = get_20_wallets(wallets["wallets"])
    price = format(price, "f")

    message = textwrap.dedent(
        f"""💊  {name} • ${symbol}\n`{address}`\n\n🕒  Age: {age}\n💰  MC: ${mcap}\n💲  Price: ${price}\n\n⚡️  Scans: ... | 🔗 ...\n👥  [Hodls](https://solscan.io/token/{address}#holders): {holders}\n\n🎯  Top 20 wallets hold: {math.floor(wallets["percent"])}%\n{wallets_string}\n\n📊 Chart  [Phtn](https://photon-sol.tinyastro.io/en/lp/{address}) | [Brdeye](https://www.birdeye.so/token/{address}?chain=solana)"""
    )

    return message
