# File: solana_token_data.py

import asyncio
from textwrap import indent
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solana.rpc.types import MemcmpOpts
import math
import requests
import json

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"


async def main():
    token_address = input("Enter Solana token address: ").strip()

    # async with AsyncClient("https://api.mainnet-beta.solana.com") as client:
    #     pubkey = Pubkey.from_string(token_address)
    #     token_supply = await client.get_token_supply(pubkey)
    #     rounded_supply = math.ceil(token_supply.value.ui_amount)
    #     print(f"Token supply: {rounded_supply}")

    response = requests.get(
        "https://api.dexscreener.com/latest/dex/tokens/BYyVSrheDtBe4PUYqW98SCwkotipXy7yydpb2dPTpump",
    )

    data = response.json()
    (json.dump(data, open("out.json", "w"), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
