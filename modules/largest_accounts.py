from calendar import c
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from my_types import Wallets


async def get_largest_wallets(
    client: AsyncClient, address: Pubkey, supply: int, pump: bool
) -> Wallets:
    try:
        # Get largest accounts for the token mint
        response = await client.get_token_largest_accounts(address)
        wallets = []
        # val = response["context"]
        combined = 0
        for i, item in enumerate(response.value):
            if i == 0 and pump:
                continue
            if i > 10:
                break
            wallets.append(item.address)
            combined += item.amount.ui_amount

        return_object: Wallets = Wallets(
            wallets=wallets, percent=float(f"{(combined / supply) * 100:.2f}")
        )

        return return_object

    except Exception as e:
        print(f"ERROR GET LARGEST WALLETS: {e}")
        return Wallets(wallets=[], percent=0.0)
