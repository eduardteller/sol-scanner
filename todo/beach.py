import requests
import json


def get_account_info(pubkey, api_key):
    url = f"https://api.solanabeach.io/v1/account/{pubkey}/transactions"
    headers = {"Accept": "application/json", "Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


# Example usage
pubkey = "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump"
api_key = "18ed571e-9803-41d0-9662-506e80f50f02"
account_info = get_account_info(pubkey, api_key)
print(len(account_info))
