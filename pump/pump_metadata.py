import requests


def get_pump_metadata(address: str):
    response = requests.post(
        "https://mainnet.helius-rpc.com/?api-key=c9a8a340-586f-46dc-a789-daff8cbc2915",
        headers={"Content-Type": "application/json"},
        json={
            "jsonrpc": "2.0",
            "id": "get-pump-metadata",
            "method": "getAsset",
            "params": {"id": address},
        },
    )
    data = response.json()

    return data
