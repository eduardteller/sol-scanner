from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solana.rpc.types import MemcmpOpts

# Constants
TOKEN_PROGRAM_ID = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
TOKEN_ACC_SIZE = 165


def get_holders(client: AsyncClient, mint: str) -> int:

    memcmp_opts = MemcmpOpts(offset=0, bytes=mint)
    filters = [TOKEN_ACC_SIZE, memcmp_opts]
    # Fetch accounts from the token program
    resp = client.get_program_accounts_json_parsed(
        TOKEN_PROGRAM_ID,
        filters=filters,
    )

    # Filter out zero-balance accounts
    non_zero_accounts = [
        acc
        for acc in resp.value
        if (acc.account.data.parsed["info"]["tokenAmount"]["uiAmount"]) != 0
    ]

    return len(non_zero_accounts)
