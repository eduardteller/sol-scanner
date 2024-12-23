import requests
import math
from datetime import datetime
from solana.rpc.api import Client
from largest_accounts import get_largest_wallets
from solders.pubkey import Pubkey

solana_client = Client(
    "https://warmhearted-cold-liquid.solana-mainnet.quiknode.pro/d66b4f59ba20fb9f1099e45b5f32f2d9a675caea/"
)


ONE_DAY = 86400

from data_processing import format_time, format_values

solscan_headers = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3MzQ5NzIxODg2MDgsImVtYWlsIjoiZWR1YXJkdGVsbGVyMUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJhcGlWZXJzaW9uIjoidjIiLCJpYXQiOjE3MzQ5NzIxODh9.IFTQ4byOepGx1DalTcaNoVsB38faQ0hHHTVwJ3EH2iM"
}
address = "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump"

pubkey = Pubkey.from_string(address)


def get_ath(creation_timestamp: int, address: str, supply: int) -> float:
    current_date = datetime.now().strftime("%Y%m%d")
    token_creation = datetime.fromtimestamp(creation_timestamp).strftime("%Y%m%d")

    solscan_filter = f"time[]={token_creation}&time[]={current_date}"

    solscan_url = f"https://pro-api.solscan.io/v2.0/token/price?address={address}&{solscan_filter}"

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

    birdeye_url = f"https://public-api.birdeye.so/defi/history_price?address=9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump&address_type=token&type=15m&time_from={after}&time_to={before}"

    birdeye_headers = {
        "accept": "application/json",
        "x-chain": "solana",
        "X-API-KEY": "8f9116c123b24a57b4b9a39ad33362c6",
    }

    birdeye_price_data_raw = requests.get(birdeye_url, headers=birdeye_headers)

    birdeye_price_data = birdeye_price_data_raw.json()

    max_price2 = max(item["value"] for item in birdeye_price_data["data"]["items"])

    return math.ceil(float(max_price2) * supply)


url = f"https://pro-api.solscan.io/v2.0/token/meta?address={address}"

url2 = "https://pro-api.solscan.io/v2.0/token/price?address=So11111111111111111111111111111111111111112"

response = requests.get(url2, headers=solscan_headers)

sol_price_response = response.json()

sol_price = float(sol_price_response["data"][0]["price"])

meta = requests.get(url, headers=solscan_headers).json()

if not meta["success"] or not meta["data"]:
    print("Failed to fetch metadata")
    exit()

name = meta["data"]["name"]
symbol: str = meta["data"]["symbol"]
image_url = meta["data"]["icon"]

mint = meta["data"]["mint_authority"]
freeze = meta["data"]["freeze_authority"]

age = format_time(int(meta["data"]["created_time"]))

decimals = int(meta["data"]["decimals"])
supply: int = math.floor(int(meta["data"]["supply"]) / (10**decimals))

price = float(meta["data"]["price"])
mcap = meta["data"]["market_cap"]
holders = meta["data"]["holder"]

ath = get_ath(int(meta["data"]["created_time"]), address, supply)

wallets = get_largest_wallets(solana_client, pubkey, supply)

# print(json.dumps(meta, indent=2))
return_message = f"""\
💠  {name} • ${(symbol.upper())}
{address}
➕  Mint: {"No 🤍" if not mint else "Yes 🚨"} | 🧊 Freeze: {"No 🤍" if not freeze else "Yes 🚨"}

🕒  Age: {age} 
💵  Price: ${price}
💰  MC: ${format_values(mcap)}
💧  Liq: $14.9M (40418 SOL)

🕊️  ATH: ${format_values(ath)} ({(ath / mcap):.2f}X)
📈  Vol: 1h: $9.8M  | 1d: $64.2M
📈  Price: 1h: 18%🔼 | 1d: 1%🔼

🦅  DexS: Paid✅ | Boosts:  
⚡️  Scans: ... | 🔗 ...
👥  Hodls: {holders} | Top: {wallets["percent"]}%

🎯  First 20: 0 Fresh

🛠️ Dev : 0 SOL | 0% $FARTCOIN
┗ Sniped: 6.7% 🤍
"""

# print(return_message)
