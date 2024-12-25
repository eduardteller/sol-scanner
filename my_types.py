from dataclasses import dataclass
from typing import Any, List


@dataclass
class Wallets:
    wallets: List[str]
    percent: str


@dataclass
class SolscanData:
    token_name: str
    token_symbol: str
    token_icon_url: str
    token_mint_auth: Any
    token_freeze_auth: Any
    token_price: float
    token_supply: int
    token_mcap: int
    token_age: str
    token_holders: int
    token_ath: int
    token_top20_wallets: Wallets
