from typing import Union, Sequence, Tuple, Callable
from numpy import ndarray, ones
from numpy.ma import exp
from numpy.random import dirichlet

from investment_simulator.utils import simulation_parameters
from investment_simulator.value_objects.simulation import AllocationResults


def sharpe_calc(rtrn: float, risk: float) -> float:
    """
    Calculate the Sharpe Ratio assumed given continuously compounded return.
    :param rtrn: Continuously compounded return.
    :param risk: Standard deviation of portfolio.
    :return: Sharpe Ratio.
    """
    return (rtrn - 0.01) / risk


def simulate_allocation(
    annual_returns: Union[Sequence[float], ndarray],
    covariance: Union[Sequence[Sequence[float]], ndarray],
) -> Callable:
    """
    Function that calculates a series of statistics about a simulated portfolio.
    :param annual_returns: Vector of annual returns of assets being optimized for.
    :param covariance: Covariance matrix of assets being optimized for.
    :return: Sharpe Ratio, Weightings, Annual Return, Risk
    """

    def inner(
        weights: Union[Sequence[float], ndarray]
    ) -> Tuple[float, ndarray, float, float]:
        rtrn, risk = simulation_parameters(
            asset_weightings=weights,
            annual_returns=annual_returns,
            covariance=covariance,
        )
        return sharpe_calc(exp(rtrn) - 1, risk), weights, exp(rtrn) - 1, risk

    return inner


def allocations_simulation(
    annual_returns: Union[Sequence[float], ndarray],
    covariance: Union[Sequence[Sequence[float]], ndarray],
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
    portfolios = dirichlet(ones(len(annual_returns)), simulations)
    result = max(map(simulate_allocation(annual_returns, covariance), portfolios))
    zipped_result = dict(
        zip(("sharpe_ratio", "weights", "annual_return", "risk"), result)
    )
    return AllocationResults(**zipped_result)
