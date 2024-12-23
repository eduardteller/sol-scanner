import requests
import json

url = "https://public-api.birdeye.so/defi/token_creation_info?address=JDxNt5W1vntc3EShiUYeAP1PRUpTLVSzX5MPUogvpump"

headers = {
    "accept": "application/json",
    "x-chain": "solana",
    "X-API-KEY": "8f9116c123b24a57b4b9a39ad33362c6",
}

response = requests.get(url, headers=headers)

data = response.json()

print(json.dumps(data))
