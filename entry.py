import textwrap
from solana.rpc.api import Client
from dexscreener import dexscreener_routine
from pumpfun import pumpfun_routine
from moonshot import moonshot_routine

solana_client = Client(
    "https://warmhearted-cold-liquid.solana-mainnet.quiknode.pro/d66b4f59ba20fb9f1099e45b5f32f2d9a675caea/"
)


def main(address: str) -> str:
    token_address = address
    response = dexscreener_routine(token_address, solana_client)

    if response == "pumpfun":
        response = pumpfun_routine(token_address, solana_client)
    elif response == "moonshot":
        response = moonshot_routine(token_address, solana_client)

    # print(textwrap.dedent(response))
    print((response))

    # return textwrap.dedent(response)


main("9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump")
