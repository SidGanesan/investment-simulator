from functools import partial
from typing import Union, Tuple, Any
from collections.abc import Sequence
from numpy import ndarray, ones, append, matmul, apply_along_axis, array
from numpy.ma import sqrt, exp, std, mean, log
from numpy.random import normal

from .value_objects.simulation import SimulationResults

__all__ = [
    "monte_carlo_sim",
    "random_walk",
]


def simulation_return(
    weights: Union[Sequence[float], ndarray],
    asset_returns: Union[Sequence[float], ndarray],
) -> float:
    if not isinstance(weights, ndarray):
        weights = ndarray(weights)
    if not isinstance(asset_returns, ndarray):
        asset_returns = ndarray(asset_returns)
    return weights.dot(asset_returns)


def simulation_risk(
    weights: Union[Sequence[float], ndarray],
    covariance: Union[Sequence[Sequence[float]], ndarray],
) -> float:
    if not isinstance(weights, ndarray):
        weights = ndarray(weights)
    if not isinstance(covariance, ndarray):
        covariance = ndarray(covariance)
    return sqrt(matMult(matMult(weights, covariance), [[x] for x in weights])[0])


def matMult(
    a: Union[Sequence[float], Sequence[Sequence[float]], ndarray],  # 1D list, 2D list, or ndarray
    b: Union[Sequence[float], Sequence[Sequence[float]], ndarray],  # 1D list, 2D list, or ndarray
) -> ndarray:
    """
    Matrix multiplication
    :param a: vector/matrix a
    :param b: vector/matrix b
    :return: cross product of a and b
    """
    if not isinstance(a, ndarray):
        a = ndarray(a)
    if not isinstance(b, ndarray):
        b = ndarray(b)
    return matmul(a, b)


def get_graph_vectors(result: ndarray) -> Tuple[Any, Any]:
    return mean(result, axis=-1).tolist(), std(result, axis=-1).tolist()


def simulation_parameters(
    asset_weightings: Union[Sequence[float], ndarray],
    annual_returns: Union[Sequence[float], ndarray],
    covariance: Union[Sequence[Sequence[float]], ndarray],
    fee: float = 0
) -> Tuple[float, float]:
    portfolio_return = log(1 + simulation_return(asset_weightings, annual_returns) - fee)
    portfolio_risk = simulation_risk(array(asset_weightings), covariance)
    return portfolio_return, portfolio_risk


def monte_carlo_sim(
    asset_weightings: Union[Sequence[float], ndarray],
    annual_returns: Union[Sequence[float], ndarray],
    covariance: Union[Sequence[Sequence[float]], ndarray],
    steps: int,
    initial_investment: float = 1,
    fee: float = 0.0,
    adds: int = 0,
    simulations: int = 1_000,
) -> SimulationResults:
    investment_return, investment_risk = simulation_parameters(asset_weightings, annual_returns, covariance, fee)
    partial_random_walk = partial(random_walk,
                                  annual_return=investment_return,
                                  investment_risk=investment_risk,
                                  period=steps,
                                  step=1,
                                  contributions=adds)
    result = apply_along_axis(partial_random_walk, -1, ones((simulations, 1)) * initial_investment)
    mean, var = get_graph_vectors(result.T)
    return SimulationResults(portfolio_return=exp(investment_return) - 1,
                             portfolio_risk=investment_risk,
                             simulation_mean=mean,
                             simulation_std=var,
                             x_max=steps,
                             y_max=max(mean) + max(var))


def investment_multiple(
    continuous_return: float,
    investment_risk: float,
    investment: float,
) -> float:
    return investment * exp(normal(continuous_return - 0.5 * investment_risk ** 2, investment_risk))


def random_walk(
    simulation: ndarray,
    annual_return: float,
    investment_risk: float,
    period: int,
    step: int,
    contributions: float = 0,
    contribution_growth: float = 0.0,
) -> Union[ndarray, list]:
    if step >= period:
        return append(simulation, investment_multiple(annual_return, investment_risk, simulation[-1]))
    else:
        return random_walk(append(simulation, investment_multiple(annual_return, investment_risk, simulation[-1]) + contributions * (1 + contribution_growth) ** step),
                           annual_return, investment_risk, period, step + 1, contributions, contribution_growth)