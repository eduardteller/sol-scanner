from solana.rpc.api import Client
from solders.pubkey import Pubkey

solana_client = Client(
    "https://warmhearted-cold-liquid.solana-mainnet.quiknode.pro/d66b4f59ba20fb9f1099e45b5f32f2d9a675caea/"
)


def get_token_creation_time(mint_address: Pubkey) -> int | None:
    before = None
    try:
        signatures = solana_client.get_signatures_for_address(
            mint_address,
            limit=1000,
        )

        while len(signatures.value) == 1000:
            before = signatures.value[-1].signature
            signatures = solana_client.get_signatures_for_address(
                account=mint_address, limit=1000, before=before
            )

        if signatures.value:
            return signatures.value[-1].block_time
        else:
            return None  # or handle as needed
    except Exception as e:
        print(f"Error fetching signatures: {e}")
        return None


mint_address = Pubkey.from_string("JDxNt5W1vntc3EShiUYeAP1PRUpTLVSzX5MPUogvpump")

t = get_token_creation_time(mint_address)
