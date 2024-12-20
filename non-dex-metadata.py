import requests
import json
import time
from datetime import datetime

# response = requests.post(
#     "https://mainnet.helius-rpc.com/?api-key=c9a8a340-586f-46dc-a789-daff8cbc2915",
#     headers={"Content-Type": "application/json"},
#     json={
#         "jsonrpc": "2.0",
#         "id": "test",
#         "method": "getAsset",
#         "params": {"id": "JDxNt5W1vntc3EShiUYeAP1PRUpTLVSzX5MPUogvpump"},
#     },
# )
# data = response.json()

# json.dump(data, open("out5.json", "w"), indent=2)


from solana.rpc.api import Client
from solders.pubkey import Pubkey

# Initialize the Solana client (use mainnet or your preferred cluster URL)
solana_client = Client(
    "https://mainnet.helius-rpc.com/?api-key=c9a8a340-586f-46dc-a789-daff8cbc2915"
)

# Replace with the mint address of your token
mint_address = Pubkey.from_string("9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump")

# Fetch transaction signatures related to the mint address
signatures = solana_client.get_signatures_for_address(mint_address)


first_signature = signatures.value[len(signatures.value) - 1].block_time
timestamp1 = time.time()
timestamp2 = first_signature

print(f"{timestamp1} {timestamp2} {len(signatures.value)}")

# Convert to datetime objects
datetime1 = datetime.fromtimestamp(timestamp1)
datetime2 = datetime.fromtimestamp(timestamp2)

time_diff = datetime1 - datetime2

# Extract total seconds
total_seconds = int(time_diff.total_seconds())

# Calculate days, hours, minutes, and seconds
days = total_seconds // 86400
hours = (total_seconds % 86400) // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60

# Format the output
if days > 0:
    formatted_time_diff = f"{days}D"
elif hours > 0:
    formatted_time_diff = f"{hours}H"
elif minutes > 0:
    formatted_time_diff = f"{minutes}M"
else:
    formatted_time_diff = f"{seconds}S"

print(formatted_time_diff)

# transaction = solana_client.get_transaction(first_signature)

# if transaction.value[0]:
#     block_time = transaction.value[0]["blockTime"]
#     print(f"Token creation timestamp: {block_time}")
