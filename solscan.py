import requests
import math
from datetime import datetime
from solana.rpc.api import Client
from largest_accounts import get_largest_wallets
from solders.pubkey import Pubkey
from data_processing import format_time, format_values
from my_types import SolscanData

ONE_DAY = 86400

solscan_headers = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3MzQ5NzIxODg2MDgsImVtYWlsIjoiZWR1YXJkdGVsbGVyMUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJhcGlWZXJzaW9uIjoidjIiLCJpYXQiOjE3MzQ5NzIxODh9.IFTQ4byOepGx1DalTcaNoVsB38faQ0hHHTVwJ3EH2iM"
}

solscan_account_data_url = "https://pro-api.solscan.io/v2.0/account/detail"
solscan_account_balance_change_url = (
    "https://pro-api.solscan.io/v2.0/account/balance_change"
)

solscan_price_url = "https://pro-api.solscan.io/v2.0/token/price"
solscan_meta_url = "https://pro-api.solscan.io/v2.0/token/meta"
birdeye_price_history_url = "https://public-api.birdeye.so/defi/history_price"


def get_ath(creation_timestamp: int, address: str, supply: int) -> float:
    current_date = datetime.now().strftime("%Y%m%d")
    token_creation = datetime.fromtimestamp(creation_timestamp).strftime("%Y%m%d")

    solscan_filter = f"time[]={token_creation}&time[]={current_date}"

    solscan_url = f"{solscan_price_url}?address={address}&{solscan_filter}"

    solscan_price_history = requests.get(solscan_url, headers=solscan_headers)

    solscan_price_history_processed = solscan_price_history.json()

    if (
        not solscan_price_history_processed["success"]
        or not solscan_price_history_processed["data"]
    ):
        return 0

    max_price_obj = max(
        solscan_price_history_processed["data"], key=lambda item: item["price"]
    )

    max_price_date = str(max_price_obj["date"])
    max_price_date_format = datetime.strptime(max_price_date, "%Y%m%d")
    unix_timestamp = int(max_price_date_format.timestamp())

    after = unix_timestamp - (ONE_DAY * 2)
    before = unix_timestamp + (ONE_DAY * 2)

    birdeye_url = f"{birdeye_price_history_url}?address=9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump&address_type=token&type=15m&time_from={after}&time_to={before}"

    birdeye_headers = {
        "accept": "application/json",
        "x-chain": "solana",
        "X-API-KEY": "8f9116c123b24a57b4b9a39ad33362c6",
    }

    birdeye_price_data_raw = requests.get(birdeye_url, headers=birdeye_headers)

    birdeye_price_data = birdeye_price_data_raw.json()

    max_price2 = max(item["value"] for item in birdeye_price_data["data"]["items"])

    return math.floor(float(max_price2) * supply)


def solana_price() -> float:
    sol_price_url = (
        f"{solscan_price_url}?address=So11111111111111111111111111111111111111112"
    )

    sol_price_resp = requests.get(sol_price_url, headers=solscan_headers)

    sol_price_resp_json = sol_price_resp.json()

    sol_price = float(sol_price_resp_json["data"][0]["price"])

    return sol_price


def dev_balance(account: str) -> str:
    get_balance_url = f"{solscan_account_data_url}?address={account}"

    get_balance_resp = requests.get(get_balance_url, headers=solscan_headers)

    get_balance_resp_json = get_balance_resp.json()

    balance = f"{(int(get_balance_resp_json['data']['lamports']) / 1000000000):.2f}"

    return balance


def dev_balance_change(account: str, address: str) -> int:
    get_balance_change_url = f"{solscan_account_balance_change_url}?address={account}&token={address}&page_size=10&page=1&remove_spam=true&flow=in&sort_by=block_time&sort_order=desc"

    get_balance_change_resp = requests.get(
        get_balance_change_url, headers=solscan_headers
    )

    get_balance_change_resp_json = get_balance_change_resp.json()

    if not get_balance_change_resp_json["data"]:
        return 0

    element = min(
        get_balance_change_resp_json["data"], key=lambda item: item["block_time"]
    )

    buy_order = math.floor(
        int(element["amount"]) / (10 ** int(element["token_decimals"]))
    )

    return buy_order


def dev_holding_sauce(account: str, address: str) -> int:
    url = f"https://pro-api.solscan.io/v2.0/account/token-accounts?address={account}&type=token&page=1&page_size=30&hide_zero=true"

    resp = requests.get(url, headers=solscan_headers)

    data = resp.json()

    token_balance = 0

    for item in data["data"]:
        if item["token_address"] == address:
            token_balance = math.floor(
                int(item["amount"]) / (10 ** int(item["token_decimals"]))
            )
            break

    return token_balance


def solscan_start(solana_client: Client, address: str, pubkey: Pubkey) -> SolscanData:
    token_meta_url = f"{solscan_meta_url}?address={address}"

    solscan_token_meta_resp = requests.get(
        token_meta_url, headers=solscan_headers
    ).json()

    if not solscan_token_meta_resp["success"] or not solscan_token_meta_resp["data"]:
        print("Failed to fetch metadata")
        exit()

    token_name = solscan_token_meta_resp["data"]["name"]
    token_symbol: str = solscan_token_meta_resp["data"]["symbol"]
    token_icon_url = solscan_token_meta_resp["data"]["icon"]

    token_mint_auth = solscan_token_meta_resp["data"]["mint_authority"]
    token_freeze_auth = solscan_token_meta_resp["data"]["freeze_authority"]

    token_age = format_time(int(solscan_token_meta_resp["data"]["created_time"]))

    token_supply_decimals = int(solscan_token_meta_resp["data"]["decimals"])
    token_supply: int = math.floor(
        int(solscan_token_meta_resp["data"]["supply"]) / (10**token_supply_decimals)
    )

    tokern_price = float(solscan_token_meta_resp["data"]["price"])
    token_mcap: int = solscan_token_meta_resp["data"]["market_cap"]
    token_holders: int = solscan_token_meta_resp["data"]["holder"]

    token_creator: str = solscan_token_meta_resp["data"]["creator"]

    token_ath: int = get_ath(
        int(solscan_token_meta_resp["data"]["created_time"]), address, token_supply
    )

    token_top20_wallets = get_largest_wallets(solana_client, pubkey, token_supply)

    return_object: SolscanData = SolscanData(
        token_name=token_name,
        token_symbol=token_symbol,
        token_creator=token_creator,
        token_icon_url=token_icon_url,
        token_mint_auth=token_mint_auth,
        token_freeze_auth=token_freeze_auth,
        token_price=tokern_price,
        token_supply=token_supply,
        token_mcap=token_mcap,
        token_age=token_age,
        token_holders=token_holders,
        token_ath=token_ath,
        token_top20_wallets=token_top20_wallets,
    )

    return return_object
