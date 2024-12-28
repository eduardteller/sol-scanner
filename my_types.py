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
    token_creator: str
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


@dataclass
class DexscreenerData:
    name: str
    symbol: str
    price: float
    liq: float
    price_change_h: float
    vol_h: str
    price_change_d: float
    vol_d: str
    boosts: str
    links: str
