from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from my_types import Wallets


async def get_largest_wallets(
    client: AsyncClient, address: Pubkey, supply: int
) -> Wallets:
    try:
        # Get largest accounts for the token mint
        response = await client.get_token_largest_accounts(address)
        wallets = []
        # val = response["context"]
        combined = 0
        for item in response.value:
            wallets.append(item.address)
            combined += item.amount.ui_amount

        return_object: Wallets = Wallets(
            wallets=wallets, percent=f"{(combined / supply) * 100:.2f}"
        )

        return return_object

    except Exception as e:
        print(f"ERROR GET LARGEST WALLETS: {e}")
        return Wallets(wallets=[], percent="0.00")
