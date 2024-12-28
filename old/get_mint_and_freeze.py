from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from spl.token._layouts import MINT_LAYOUT


def get_mint_and_freeze_authority(client: AsyncClient, address: Pubkey) -> str:

    return_string = ""

    mint_account_info = client.get_account_info(address)

    mint_data = mint_account_info.value.data
    mint_info = MINT_LAYOUT.parse(mint_data)

    mint_auth = int(mint_info.mint_authority_option)
    freeze_auth = int(mint_info.freeze_authority_option)

    if mint_auth > 0:
        return_string += "🚨 Mint authority is enabled 🚨\n"
    else:
        return_string += "➕ Mint: ✅"

    if freeze_auth > 0:
        return_string += "🚨 Freeze authority is enabled 🚨\n"
    else:
        return_string += " | ➕ Freeze: ✅"

    return return_string
