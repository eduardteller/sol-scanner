from solana.rpc.api import Client
from solders.pubkey import Pubkey


def get_token_creation_time(mint_address: Pubkey, client: Client) -> int | None:
    before = None
    try:
        signatures = client.get_signatures_for_address(
            mint_address,
            limit=1000,
        )

        while len(signatures.value) == 1000:
            before = signatures.value[-1].signature
            signatures = client.get_signatures_for_address(
                account=mint_address, limit=1000, before=before
            )

        if signatures.value:
            return signatures.value[-1].block_time
        else:
            return None  # or handle as needed
    except Exception as e:
        print(f"Error fetching signatures: {e}")
        return None
