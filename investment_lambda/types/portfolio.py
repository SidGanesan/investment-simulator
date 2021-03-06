from dataclasses import dataclass


@dataclass
class PortfolioHolding:
    asset: str
    weight: float
    fee: float
    r: float


@dataclass
class Portfolio:
    model: str
    name: str
    score: int
    holdings: PortfolioHolding
