from solana.rpc.api import Client
from solders.pubkey import Pubkey
from spl.token._layouts import MINT_LAYOUT


client = Client(
    "https://warmhearted-cold-liquid.solana-mainnet.quiknode.pro/d66b4f59ba20fb9f1099e45b5f32f2d9a675caea/"
)

mint_address = Pubkey.from_string("DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263")
mint_account_info = client.get_account_info(mint_address)


mint_data = mint_account_info.value.data
mint_info = MINT_LAYOUT.parse(mint_data)

print(mint_info)

mint_authority = Pubkey.from_bytes(mint_info.mint_authority)
free = Pubkey.from_bytes(mint_info.freeze_authority)

print(f"Mint Authority: {int(mint_info.mint_authority_option)}")
print(f"Freeze Authority: {int(mint_info.freeze_authority_option)}")
