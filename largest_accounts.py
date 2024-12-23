from solana.rpc.api import Client
from solders.pubkey import Pubkey
import math


def get_largest_wallets(client: Client, address: Pubkey, supply: int) -> str:
    # Get largest accounts for the token mint
    response = client.get_token_largest_accounts(address)
    wallets = []
    # val = response["context"]
    combined = 0
    for i, item in enumerate(response.value):
        wallets.append(item.address)
        combined += item.amount.ui_amount

    return {"wallets": wallets, "percent": f"{(combined / supply) * 100:.2f}"}
