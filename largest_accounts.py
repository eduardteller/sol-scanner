from solana.rpc.api import Client
from solders.pubkey import Pubkey
from my_types import Wallets


def get_largest_wallets(client: Client, address: Pubkey, supply: int) -> Wallets:
    # Get largest accounts for the token mint
    response = client.get_token_largest_accounts(address)
    wallets = []
    # val = response["context"]
    combined = 0
    for i, item in enumerate(response.value):
        wallets.append(item.address)
        combined += item.amount.ui_amount

    return_object: Wallets = Wallets(
        wallets=wallets, percent=f"{(combined / supply) * 100:.2f}"
    )

    return return_object
