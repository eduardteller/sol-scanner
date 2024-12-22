import requests
import json
from todo.find import start
import time

ENDPOINT = "https://programs.shyft.to/v0/graphql/?api_key=WXLnaB1VZbEZMfic&network=mainnet-beta"


def query_lp_by_token(token):
    query = """
    query MyQuery($where: Raydium_LiquidityPoolv4_bool_exp) {
      Raydium_LiquidityPoolv4(where: $where) {
        _updatedAt
        amountWaveRatio
        baseDecimal
        baseLotSize
        baseMint
        baseNeedTakePnl
        baseTotalPnl
        baseVault
        depth
        lpMint
        lpReserve
        lpVault
        marketId
        marketProgramId
        maxOrder
        maxPriceMultiplier
        minPriceMultiplier
        minSeparateDenominator
        minSeparateNumerator
        minSize
        nonce
        openOrders
        orderbookToInitTime
        owner
        pnlDenominator
        pnlNumerator
        poolOpenTime
        punishCoinAmount
        punishPcAmount
        quoteDecimal
        quoteLotSize
        quoteMint
        quoteNeedTakePnl
        quoteTotalPnl
        quoteVault
        resetFlag
        state
        status
        swapBase2QuoteFee
        swapBaseInAmount
        swapBaseOutAmount
        swapFeeDenominator
        swapFeeNumerator
        swapQuote2BaseFee
        swapQuoteInAmount
        swapQuoteOutAmount
        systemDecimalValue
        targetOrders
        tradeFeeDenominator
        tradeFeeNumerator
        volMaxCutRatio
        withdrawQueue
        pubkey
      }
    }
    """
    # variables = {
    #     "where": {
    #         "_or": [
    #             {
    #                 "baseMint": {"_eq": token},
    #                 "quoteMint": {
    #                     "_eq": "So11111111111111111111111111111111111111112"
    #                 },  # SOL mint address
    #             },
    #             {
    #                 "baseMint": {
    #                     "_eq": "So11111111111111111111111111111111111111112"
    #                 },  # SOL mint address
    #                 "quoteMint": {"_eq": token},
    #             },
    #         ]
    #     }
    # }
    variables = {
        "where": {"_or": [{"baseMint": {"_eq": token}}, {"quoteMint": {"_eq": token}}]},
    }

    response = requests.post(ENDPOINT, json={"query": query, "variables": variables})
    data = response.json()
    pools = data.get("data", {}).get("Raydium_LiquidityPoolv4", [])
    print(len(pools))
    for i in pools:
        start(i["pubkey"])
        time.sleep(2)


if __name__ == "__main__":
    query_lp_by_token("DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263")
