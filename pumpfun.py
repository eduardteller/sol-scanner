import requests
import textwrap
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from modules.data_processing import format_values, format_time
from old.holders import get_holders
from modules.largest_accounts import get_largest_wallets
from dexscreener import format_wallets, get_social_links
from pump.pump_creation_time import get_token_creation_time
from pump.pump_metadata import get_pump_metadata
import math
from modules.data_processing import format_time
import json


def pumpfun_routine(address: str, client: AsyncClient) -> str:
    pub = Pubkey.from_string(address)
    age = format_time(get_token_creation_time(pub, client))
    data = get_pump_metadata(address)

    info = data["result"]["token_info"]

    print(json.dumps(data, indent=4))

    name = data["result"]["content"]["metadata"]["name"]
    symbol = data["result"]["content"]["metadata"]["symbol"]
    price = float(info["price_info"]["price_per_token"])
    decimals = int(info["decimals"])
    supply = int(info["supply"]) / 10**decimals
    mcap = format_values(supply * price)
    # links = get_socials(pair)

    holders = get_holders(client, address)

    wallets = get_largest_wallets(client, pub)

    wallets_string = format_wallets(wallets["wallets"])
    price = format(price, "f")

    message = f"""\
        💊  **{name}** • **${symbol}**
        `{address}`

        🕒  Age: {age}
        💰  MC: ${mcap}
        💲  Price: ${price}

        ⚡️  Scans: ... | 🔗 ...
        👥  [Hodls](https://solscan.io/token/{address}#holders): {holders}

        🎯  Top 20 wallets hold: {math.floor(wallets["percent"])}%
        {wallets_string}

        📊 Chart  [Phtn](https://photon-sol.tinyastro.io/en/lp/{address}) | [Brdeye](https://www.birdeye.so/token/{address}?chain=solana)
    """

    return message
