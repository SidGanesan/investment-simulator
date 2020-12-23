from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class SimulationResults:
    portfolio_return: float
    portfolio_risk: float
    simulation_mean: List
    simulation_std: List
    x_max: float
    y_max: float
