import requests
import json
from solana.rpc.api import Client
from solders.pubkey import Pubkey

GQL_ENDPOINT = "https://programs.shyft.to/v0/graphql/?api_key=WXLnaB1VZbEZMfic&network=mainnet-beta"
RPC_ENDPOINT = "https://rpc.shyft.to?api_key=WXLnaB1VZbEZMfic"

# Create a Solana client to fetch on-chain data
solana_client = Client(RPC_ENDPOINT)


def query_lp_mint_info(address: str):
    query = """
    query MyQuery($where: Raydium_LiquidityPoolv4_bool_exp) {
      Raydium_LiquidityPoolv4(where: $where) {
        baseMint
        lpMint
        lpReserve
      }
    }
    """
    variables = {"where": {"pubkey": {"_eq": address}}}
    try:
        response = requests.post(
            GQL_ENDPOINT, json={"query": query, "variables": variables}, timeout=10
        )
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.RequestException as err:
        print(f"Request exception: {err}")
    except json.JSONDecodeError:
        print("Failed to decode JSON. Response content:")
        print(response.text)
    return None


def get_burn_percentage(lp_reserve, actual_supply):
    max_lp_supply = max(actual_supply, lp_reserve - 1)
    burn_amt = max_lp_supply - actual_supply
    return (burn_amt / max_lp_supply) * 100 if max_lp_supply else 0


def start(address):
    # Query for a specific pool
    info = query_lp_mint_info(address)
    data = info.get("data", {}).get("Raydium_LiquidityPoolv4", [])
    if not data:
        print("No data found for the given address.")
        exit()

    lp_mint = data[0]["lpMint"]
    lp_reserve_raw = data[0]["lpReserve"]

    # Fetch on-chain mint info
    parsed_acc_info = solana_client.get_account_info_json_parsed(
        Pubkey.from_string(lp_mint)
    )
    # mint_info = parsed_acc_info["result"]["value"]["data"]["parsed"]["info"]
    mint_info = parsed_acc_info.value.data.parsed["info"]

    decimals = mint_info["decimals"]
    supply_raw = mint_info["supply"]

    # Convert raw supply/reserve based on decimals
    lp_reserve = lp_reserve_raw / (10**decimals)
    actual_supply = float(supply_raw) / (10**decimals)

    # print(f"lpMint: {lp_mint}")
    burn_pct = get_burn_percentage(lp_reserve, actual_supply)

    if int(burn_pct) < 90:
        return

    print("-----------------")
    print(f"Reserve: {lp_reserve}")
    print(f"Actual Supply: {actual_supply}")

    print(f"{burn_pct} LP burned")
