from dataclasses import dataclass

import numpy as np
from typing import Tuple, Callable, List

from investment_simulator.utils import simulation_parameters, ArrayLike, ArrayLike2D


@dataclass(frozen=True)
class AllocationResults:
    sharpe_ratio: float
    annual_return: float
    risk: float
    weights: List[float]

    def __lt__(self, other: "AllocationResults"):
        return self.sharpe_ratio < other.sharpe_ratio


def sharpe_calc(rtrn: float, risk: float, rf: float) -> float:
    """
    Calculate the Sharpe Ratio assumed given continuously compounded return.
    :param rtrn: Continuously compounded return.
    :param risk: Standard deviation of portfolio.
    :param rf: Risk free rate of return.
    :return: Sharpe Ratio.
    """
    return (rtrn - rf) / risk


def simulate_allocation(
    annual_returns: ArrayLike, covariance: ArrayLike2D, risk_free_rate: float = 0.0025
) -> Callable[[ArrayLike], AllocationResults]:
    """
    Function that calculates a series of statistics about a simulated portfolio.
    :param annual_returns: Vector of annual returns of assets being optimized for.
    :param covariance: Covariance matrix of assets being optimized for.
    :param risk_free_rate: Risk Free Rate of Return. 10yr Govt Bonds Yield .
    :return: Sharpe Ratio, Weightings, Annual Return, Risk.
    """

    def inner(weights: ArrayLike) -> AllocationResults:
        rtrn, risk = simulation_parameters(
            asset_weightings=weights,
            annual_returns=annual_returns,
            covariance=covariance,
        )
        return AllocationResults(
            sharpe_calc(np.exp(rtrn) - 1, risk, risk_free_rate),
            np.exp(rtrn) - 1,
            risk,
            weights if not isinstance(weights, np.ndarray) else weights.tolist(),
        )

    return inner


def allocations_simulation(
    annual_returns: ArrayLike,
    covariance: ArrayLike2D,
    simulations: int = 1_000,
) -> AllocationResults:
    """
    Calculates the optimum portfolio weightings for a given set of returns and covariance
    of assets
    :param annual_returns: Vector of annual returns of assets being optimized for.
    :param covariance: Covariance matrix of assets being optimized for.
    :param simulations: Number of simulations run.
    :return: AllocationResults Value Object.
    """
    portfolios = np.random.dirichlet(np.ones(len(annual_returns)), simulations)
    return max(map(simulate_allocation(annual_returns, covariance), portfolios))
