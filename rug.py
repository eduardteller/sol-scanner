import requests


# 1. Setup Solana connection and wallet
def check_rug(address: str):
    # 5. Send the POST request to RugCheck API
    url = f"https://api.rugcheck.xyz/v1/tokens/{address}/report/summary"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        resp = response.json()
        return resp

    return None
