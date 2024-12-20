from jsonrpcclient import request, parse, Ok
import logging
import requests

from solana.rpc.api import Client

solana_client = Client(
    "https://warmhearted-cold-liquid.solana-mainnet.quiknode.pro/d66b4f59ba20fb9f1099e45b5f32f2d9a675caea/"
)
print(solana_client.get_program_accounts("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"))
