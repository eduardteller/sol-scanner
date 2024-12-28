import textwrap
from aiohttp import ClientSession
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from dexscreener import exec_dexscreener
from my_types import DexscreenerData, SolscanData
import math
from modules.raydium import get_lp_burn
from modules.solscan import (
    exec_solscan,
    get_sol_price,
    get_dev_balance,
    get_dev_balance_change,
    get_dev_token_balance,
)
from modules.rugcheck import get_rugcheck_score
from modules.data_processing import format_values, format_wallets
import asyncio

pump_fun_program_pubkey = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"


async def exec_main(address: str) -> str:
    solana_client = AsyncClient(
        "https://mainnet.helius-rpc.com/?api-key=c9a8a340-586f-46dc-a789-daff8cbc2915"
    )
    session = ClientSession()

    try:
        public_key = Pubkey.from_string(address)

        dex_response = await exec_dexscreener(address, session)

        if dex_response == "pumpfun":
            return {
                "icon": "https://en.wikipedia.org/wiki/Solana_(blockchain_platform)#/media/File:Solana_logo.png",
                "message": "pumpfun",
            }

        if dex_response == "moonshot":
            return {
                "icon": "https://en.wikipedia.org/wiki/Solana_(blockchain_platform)#/media/File:Solana_logo.png",
                "message": "moonshot",
            }

        final = await dexscreener_routine(
            dex_response, address, solana_client, session, public_key
        )

        return final

    except Exception as e:
        print(f"ERROR!!!: {e}")
        return {"error": str(e)}

    finally:
        await solana_client.close()
        await session.close()


async def dexscreener_routine(
    data: DexscreenerData,
    address: str,
    rpc_client: AsyncClient,
    session: ClientSession,
    public_key: str,
) -> str:
    try:
        # sol_data, sol_price, rug, burn = await asyncio.gather(
        #     exec_solscan(rpc_client, address, public_key, session),
        #     get_sol_price(session),
        #     get_rugcheck_score(session, address),
        #     get_lp_burn(session, address),
        # )
        sol_data, sol_price, burn = await asyncio.gather(
            exec_solscan(rpc_client, address, public_key, session),
            get_sol_price(session),
            get_lp_burn(session, address),
        )

        if not sol_data:
            return {
                "icon": "https://en.wikipedia.org/wiki/Solana_(blockchain_platform)#/media/File:Solana_logo.png",
                "text": textwrap.dedent("ERROR SOLCAN"),
            }

        sol_data: SolscanData = sol_data

        dev_balance_sol, dev_balance_change_var, dev_holding_amount = (
            await asyncio.gather(
                get_dev_balance(sol_data.token_creator, session),
                get_dev_balance_change(sol_data.token_creator, address, session),
                get_dev_token_balance(sol_data.token_creator, address, session),
            )
        )

        dev_snipe_percent = (
            f"{(dev_balance_change_var / sol_data.token_supply * 100):.2f}"
        )

        if dev_holding_amount:
            dev_holding_amount = math.floor(
                dev_holding_amount / sol_data.token_supply * 100
            )

        # rug_score = f"📢  [Rug Score](https://rugcheck.xyz/tokens/{address}): {rug['score']} {('✅' if int(rug['score']) < 400 else '🚨')}"

        wallets_string = format_wallets(sol_data.token_top20_wallets.wallets)

        price_change_h = (
            f"{data.price_change_h}% 🔻"
            if data.price_change_h < 0
            else f"{data.price_change_h}% 🔼"
        )
        price_change_d = (
            f"{data.price_change_d}% 🔻"
            if data.price_change_d < 0
            else f"{data.price_change_d}% 🔼"
        )

        return_message = f"""\
        💠  **{data.name}** • **${(data.symbol.upper())}**
        `{address}`
        
        ➕  **Mint**: {"No ✅" if not sol_data.token_mint_auth else "Yes 🚨"} | 🧊 **Freeze**: {"No ✅" if not sol_data.token_freeze_auth else "Yes 🚨"}
        🌊  LP: {math.floor(burn)}% Burnt
        
        🕒  **Age**: {sol_data.token_age} 
        💵  **Price**: ${data.price}
        💰  **MC**: ${format_values(sol_data.token_mcap)}
        💧  **Liq**: ${format_values(data.liq)} ({math.floor(data.liq / sol_price)} SOL)

        🕊️  **ATH**: ${format_values(sol_data.token_ath)} ({(sol_data.token_ath / sol_data.token_mcap):.2f}X)
        📈  **Vol**: 1h: ${data.vol_h} | 1d: ${data.vol_d}
        📈  **Price**: 1h: {price_change_h} | 1d: {price_change_d}

        🦅  [DexS](https://dexscreener.com/solana/{address}): Paid ✅ {f"{data.boosts}" if data.boosts else ""}
        🔗  {data.links}
        👥  [Hodls](https://solscan.io/token/{address}#holders): {sol_data.token_holders} | Top: {sol_data.token_top20_wallets.percent}%

        🛠️ [Dev](https://solscan.io/account/{sol_data.token_creator}) : {dev_balance_sol} SOL | {dev_holding_amount}% ${(data.symbol.upper())}
        ┗ Sniped: {dev_snipe_percent}%
        
        📊 **Chart**  [DEX](https://dexscreener.com/solana/{address}) | [Phtn](https://photon-sol.tinyastro.io/en/lp/{address}) | [Brdeye](https://www.birdeye.so/token/{address}?chain=solana)
        """

        return {
            "icon": "https://en.wikipedia.org/wiki/Solana_(blockchain_platform)#/media/File:Solana_logo.png",
            "text": textwrap.dedent(return_message),
        }

    except Exception as e:
        print(f"ERROR DEXSCREENR ROUTINE: {e}")
        return {
            "icon": "https://en.wikipedia.org/wiki/Solana_(blockchain_platform)#/media/File:Solana_logo.png",
            "text": textwrap.dedent("ERROR DEXSCREENR ROUTINE"),
        }


# asyncio.run(exec_main("2zMMhcVQEXDtdE6vsFS7S7D5oUodfJHE8vd1gnBouauv"))
