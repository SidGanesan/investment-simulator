import random
from functools import partial
from typing import Union, Tuple, Any
from collections.abc import Sequence
import numpy as np
from numpy.ma import sqrt

from .value_objects.simulation import SimulationResults

__all__ = [
    "monte_carlo_sim",
    "random_walk",
]


def simulation_return(
    weights: Union[Sequence[float], np.ndarray],
    asset_returns: Union[Sequence[float], np.ndarray],
) -> float:
    if not isinstance(weights, np.ndarray):
        weights = np.ndarray(weights)
    if not isinstance(asset_returns, np.ndarray):
        asset_returns = np.ndarray(asset_returns)
    return weights.dot(asset_returns)


def simulation_risk(
    weights: Union[Sequence[float], np.ndarray],
    covariance: Union[Sequence[Sequence[float]], np.ndarray],
) -> float:
    if not isinstance(weights, np.ndarray):
        weights = np.ndarray(weights)
    if not isinstance(covariance, np.ndarray):
        covariance = np.ndarray(covariance)
    return sqrt(matMult(matMult(weights, covariance), [[x] for x in weights])[0])


def get_graph_vectors(result: np.ndarray) -> Tuple[Any, Any]:
    return np.average(result, axis=-1).tolist(), np.ma.std(result, axis=-1).tolist()


def simulation_parameters(
    asset_weightings: Union[Sequence[float], np.ndarray],
    annual_returns: Union[Sequence[float], np.ndarray],
    covariance: Union[Sequence[Sequence[float]], np.ndarray],
    fee: float = 0
) -> Tuple[float, float]:
    portfolio_return = np.log(1 + simulation_return(asset_weightings, annual_returns) - fee)
    portfolio_risk = simulation_risk(np.array(asset_weightings), covariance)
    return portfolio_return, portfolio_risk


def monte_carlo_sim(
    asset_weightings: Union[Sequence[float], np.ndarray],
    annual_returns: Union[Sequence[float], np.ndarray],
    covariance: Union[Sequence[Sequence[float]], np.ndarray],
    steps: int,
    initial_investment: float = 1,
    fee: float = 0.0,
    adds: int = 0,
) -> SimulationResults:
    investment_return, investment_risk = simulation_parameters(asset_weightings, annual_returns, covariance, fee)
    partial_random_walk = partial(random_walk,
                                  annual_return=investment_return,
                                  investment_risk=investment_risk,
                                  period=steps,
                                  step=1,
                                  contributions=adds)
    result = np.apply_along_axis(partial_random_walk, -1, np.ones((1_000, 1)) * initial_investment)
    mean, var = get_graph_vectors(result.T)
    return SimulationResults(portfolio_return=np.math.exp(investment_return) - 1,
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
    return investment * np.math.exp(random.normalvariate(continuous_return - 0.5 * investment_risk ** 2, investment_risk))


def random_walk(
    simulation: np.array,
    annual_return: float,
    investment_risk: float,
    period: int,
    step: int,
    contributions: float = 0,
    contribution_growth: float = 0.0,
) -> Union[np.ndarray, list]:
    if step >= period:
        return np.append(simulation, investment_multiple(annual_return, investment_risk, simulation[-1]))
    else:
        return random_walk(np.append(simulation, investment_multiple(annual_return, investment_risk, simulation[-1]) + contributions * (1 + contribution_growth) ** step),
                           annual_return, investment_risk, period, step + 1, contributions, contribution_growth)


def matMult(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Matrix multiplication
    :param a: vector/matrix a
    :param b: vector/matrix b
    :return: cross product of a and b
    """
    return np.matmul(a, b)
