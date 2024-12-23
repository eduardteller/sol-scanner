from solana.rpc.api import Client
from solders.pubkey import Pubkey


def get_largest_wallets(client: Client, address: Pubkey) -> str:
    # Get largest accounts for the token mint
    response = client.get_token_largest_accounts(address)
    wallets = []
    # val = response["context"]
    combined = 0
    for i in response.value:
        wallets.append(i.address)
        combined += i.amount.ui_amount

    return {"wallets": wallets, "percent": combined / 10000000}
