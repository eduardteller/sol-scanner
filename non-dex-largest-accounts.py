import math
from solana.rpc.api import Client
import json
from solders.pubkey import Pubkey

# Initialize Solana RPC client
solana_client = Client(
    "https://warmhearted-cold-liquid.solana-mainnet.quiknode.pro/d66b4f59ba20fb9f1099e45b5f32f2d9a675caea/"
)

# Token mint address for the meme token
TOKEN_MINT = Pubkey.from_string("Ak1a2MYuJJSMkvK4d4d6SnBVKNVMqEULb3YnLJYppump")

# Get largest accounts for the token mint
response = solana_client.get_token_largest_accounts(TOKEN_MINT)

# val = response["context"]
combined = 0
for i in response.value:
    print(i.amount.ui_amount_string)
    combined += i.amount.ui_amount

print(f"Total {math.ceil(combined)}")
print(f"{math.ceil(combined / 10000000)}%")

# Parse results
# print(json.dumps(response["value"], indent=2))
