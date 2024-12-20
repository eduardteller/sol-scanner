from solders.pubkey import Pubkey
from solana.rpc.types import MemcmpOpts
from solana.rpc.async_api import AsyncClient
import asyncio

token_to_search = "JDxNt5W1vntc3EShiUYeAP1PRUpTLVSzX5MPUogvpump"
TOKEN_PROGRAM_ID = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")


async def get_token_holders():
    # Define filters to get SPL token accounts for the specified mint address
    filters = [
        MemcmpOpts(offset=0, bytes=token_to_search),
    ]  # Token account size,
    async with AsyncClient("https://api.mainnet-beta.solana.com") as client:
        response = await client.get_program_accounts(
            TOKEN_PROGRAM_ID,
            filters=filters,
        )
        print(response.value[0].account.lamports)


if __name__ == "__main__":
    asyncio.run(get_token_holders())
