import requests
import json
from find import start

ENDPOINT = "https://programs.shyft.to/v0/graphql/?api_key=WXLnaB1VZbEZMfic&network=mainnet-beta"


def query_lp_pair(token_one, token_two):
    query = f"""
    query MyQuery {{
      Raydium_LiquidityPoolv4(
        where: {{
          baseMint: {{_eq: "{token_one}"}},
          quoteMint: {{_eq: "{token_two}"}}
        }}
        order_by: {{poolOpenTime: desc}}
      ) {{
        baseDecimal
        baseLotSize
        baseMint
        baseVault
        lpMint
        lpReserve
        lpVault
        marketId
        marketProgramId
        openOrders
        owner
        poolOpenTime
        quoteDecimal
        quoteLotSize
        quoteMint
        quoteNeedTakePnl
        quoteTotalPnl
        quoteVault
        status
        pubkey
      }}
    }}
    """
    response = requests.post(ENDPOINT, json={"query": query})
    result = response.json()
    pools = result.get("data", {}).get("Raydium_LiquidityPoolv4", [])

    for i in pools:
        start(i["pubkey"])


if __name__ == "__main__":
    query_lp_pair(
        "So11111111111111111111111111111111111111112",
        "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
    )
