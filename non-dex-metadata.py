import requests
import json
import time
from datetime import datetime

response = requests.post(
    "https://mainnet.helius-rpc.com/?api-key=c9a8a340-586f-46dc-a789-daff8cbc2915",
    headers={"Content-Type": "application/json"},
    json={
        "jsonrpc": "2.0",
        "id": "test",
        "method": "getAsset",
        "params": {"id": "Ak1a2MYuJJSMkvK4d4d6SnBVKNVMqEULb3YnLJYppump"},
    },
)
data = response.json()

print(json.dumps(data, indent=2, ensure_ascii=False))
