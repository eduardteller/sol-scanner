from solana.rpc.types import MemcmpOpts
from typing import List, Union
from solana.rpc.api import Client
from solders.pubkey import Pubkey

solana_client = Client("https://explorer-api.mainnet-beta.solana.com/")
memcmp_opts = MemcmpOpts(offset=4, bytes="3Mc6vR")
pubkey = Pubkey.from_string("4Nd1mBQtrMJVYVfKf2PJy9NZUZdTAsp7D4xWLs4gDB4T")
filters: List[Union[int, MemcmpOpts]] = [17, memcmp_opts]
resp = solana_client.get_program_accounts(pubkey, filters=filters)
print(resp.value)
