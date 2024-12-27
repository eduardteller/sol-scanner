import requests
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from data_processing import format_values, format_time
from get_mint_and_freeze import get_mint_and_freeze_authority
from holders import get_holders
from largest_accounts import get_largest_wallets
from my_types import SolscanData
from solscan import (
    solscan_start,
    solana_price,
    dev_balance,
    dev_balance_change,
    dev_holding_sauce,
)
import math
from typing import List
from rug import check_rug


def get_20_wallets(wallets: List[str]) -> str:
    return_string = ""
    for i, idx in enumerate(wallets):
        return_string += f"[🐳](https://solscan.io/account/{idx})"
        if i == 10:
            return_string += "\n"

    return return_string


def get_boosts(value) -> str:
    if "boosts" in value and value["boosts"]:
        boosts = f"| {value['boosts']['active']} ⚡️"
    else:
        boosts = ""

    return boosts


def get_socials(data) -> str:
    value = data["info"]
    if "socials" not in value or not value["socials"]:
        print("No socials")
        return ""

    string_of_socials = ""
    for social in value["socials"]:
        if social["type"] == "twitter":
            string_of_socials = f"[TW]({social['url']})"
        elif social["type"] == "telegram":
            string_of_socials += f" | [TG]({social['url']})"

    if value["websites"][0]:
        string_of_socials += f" | [WEB]({value['websites'][0]['url']})"

    return string_of_socials


def dexscreener_routine(address: str, client: Client) -> str:
    response = requests.get(
        f"https://api.dexscreener.com/latest/dex/tokens/{address}",
    )

    pub = Pubkey.from_string(address)

    data = response.json()

    if not data["pairs"]:
        return "pumpfun"

    if "moonshot" in data["pairs"][0]:
        return "moonshot"

    sol_data: SolscanData = solscan_start(client, address, pub)
    sol_price: float = solana_price()

    dev_balance_sol = dev_balance(sol_data.token_creator)
    dev_balance_change_var = dev_balance_change(
        sol_data.token_creator,
        address,
    )
    # dev_snipe_percent = f"{(dev_balance_change_var / sol_data.token_supply):.2f}"
    dev_snipe_percent = f"{(dev_balance_change_var / sol_data.token_supply * 100):.2f}"
    dev_holding_amoutn = dev_holding_sauce(sol_data.token_creator, address)

    if dev_holding_amoutn:
        dev_holding_amoutn = math.floor(
            dev_holding_amoutn / sol_data.token_supply * 100
        )

    pair = data["pairs"][0]

    # mcap_raw = pair["marketCap"]
    # mcap = format_values(pair["marketCap"])
    # age = format_time(pair["pairCreatedAt"])
    
    name = pair["baseToken"]["name"]
    symbol: str = pair["baseToken"]["symbol"]
    price = pair["priceUsd"]
    liq_raw = pair["liquidity"]["usd"]
    liq = format_values(pair["liquidity"]["usd"])
    price_change_h = pair["priceChange"]["h1"]
    vol_h = format_values(pair["volume"]["h1"])
    price_change_d = pair["priceChange"]["h24"]
    vol_d = format_values(pair["volume"]["h24"])
    boosts = get_boosts(pair)
    links = get_socials(pair)

    rug = check_rug(address)

    wallets_string = get_20_wallets(sol_data.token_top20_wallets.wallets)

    price_change_h = f"{price_change_h}% 🔻" if price_change_h < 0 else f"{price_change_h}% 🔼"
    price_change_d = f"{price_change_d}% 🔻" if price_change_d < 0 else f"{price_change_d}% 🔼"

    rug_score = (
        f"📢  [Rug Score](https://rugcheck.xyz/tokens/{address}): {rug['score']} {"✅" if int(rug["score"]) < 400 else "🚨"}"
    )

    message2 = f"""\
    💠  **{name}** • **${(symbol.upper())}**
    `{address}`
    
    ➕  **Mint**: {"No ✅" if not sol_data.token_mint_auth else "Yes 🚨"} | 🧊 **Freeze**: {"No ✅" if not sol_data.token_freeze_auth else "Yes 🚨"}

    {rug_score}

    🕒  **Age**: {sol_data.token_age} 
    💵  **Price**: ${price}
    💰  **MC**: ${format_values(sol_data.token_mcap)}
    💧  **Liq**: ${liq} ({math.floor(liq_raw / sol_price)} SOL)

    🕊️  **ATH**: ${format_values(sol_data.token_ath)} ({(sol_data.token_ath / sol_data.token_mcap):.2f}X)
    📈  **Vol**: 1h: ${vol_h} | 1d: ${vol_d}
    📈  **Price**: 1h: {price_change_h} | 1d: {price_change_d}

    🦅  [DexS](https://dexscreener.com/solana/{address}): Paid ✅ {f"{boosts}" if boosts else ""}
    🔗  {links}
    👥  [Hodls](https://solscan.io/token/{address}#holders): {sol_data.token_holders} | Top: {sol_data.token_top20_wallets.percent}%

    🛠️ [Dev](https://solscan.io/account/{sol_data.token_creator}) : {dev_balance_sol} SOL | {dev_holding_amoutn}% ${(symbol.upper())}
    ┗ Sniped: {dev_snipe_percent}%
    
    📊 **Chart**  [DEX](https://dexscreener.com/solana/{address}) | [Phtn](https://photon-sol.tinyastro.io/en/lp/{address}) | [Brdeye](https://www.birdeye.so/token/{address}?chain=solana)
    """

    return {
        "message": message2,
        "image": sol_data.token_icon_url,
    }
