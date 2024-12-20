from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solana.rpc.types import MemcmpOpts, DataSliceOpts
import asyncio
import json

# Constants
RPC_URL = "https://warmhearted-cold-liquid.solana-mainnet.quiknode.pro/d66b4f59ba20fb9f1099e45b5f32f2d9a675caea/"
# RPC_URL = "https://mainnet.helius-rpc.com/?api-key=c9a8a340-586f-46dc-a789-daff8cbc2915"
MINT = "EwN47qbxgNwJUoQ2Viu4hx9o88dvW1mN4TCKrUhgpump"
TOKEN_PROGRAM_ID = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
TOKEN_ACC_SIZE = 165

memcmp_opts = MemcmpOpts(offset=0, bytes=MINT)
filterss = [TOKEN_ACC_SIZE, memcmp_opts]


async def main():
    async with AsyncClient(RPC_URL) as client:
        # Fetch accounts from the token program
        resp = await client.get_program_accounts_json_parsed(
            TOKEN_PROGRAM_ID,
            filters=filterss,
        )

        # Filter out zero-balance accounts
        non_zero_accounts = [
            acc
            for acc in resp.value
            if (acc.account.data.parsed["info"]["tokenAmount"]["uiAmount"]) != 0
        ]

        print(len(non_zero_accounts))

        # Process the first 100 accounts
        # first_hundred = non_zero_accounts[:100]
        # for acc in first_hundred:
        #     acc_pubkey = acc["pubkey"]
        #     acc_data = acc["account"]["data"]
        #     balance = int.from_bytes(bytes(acc_data), "little")
        #     print(f"Balance of {acc_pubkey} is {balance}")


# Run the asyncio event loop
asyncio.run(main())
