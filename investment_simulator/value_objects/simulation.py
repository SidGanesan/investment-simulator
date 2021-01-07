from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class PortfolioResults:
    portfolio_return: float
    portfolio_risk: float
    simulation_mean: List
    simulation_std: List
    x_max: float
    y_max: float


@dataclass(frozen=True)
class AllocationResults:
    sharpe_ratio: float
    annual_return: float
    risk: float
    weights: List
