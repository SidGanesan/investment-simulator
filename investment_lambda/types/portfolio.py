from dataclasses import dataclass
from typing import List


@dataclass
class PortfolioConstants:
    model: str
    covariance_matrix: List[List[float]]


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
