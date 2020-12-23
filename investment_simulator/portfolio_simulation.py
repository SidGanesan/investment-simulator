import random
from functools import partial
from typing import Union, Tuple, Any
from collections.abc import Sequence
import numpy as np
from numpy.ma import sqrt

from .value_objects.simulation import SimulationResults


def simulation_return(wghts: Union[Sequence[float], np.ndarray],
                      asset_returns: Union[Sequence[float], np.ndarray]) -> float:
    if (type(wghts) != np.ndarray) & (type(asset_returns) != np.ndarray):
        return np.array(wghts).dot(np.array(asset_returns))
    else:
        return wghts.dot(asset_returns)


def sim_std(wghts: Union[Sequence[float], np.ndarray],
            covariance: Union[Sequence[Sequence[float]], np.ndarray]) -> float:
    if (type(wghts) != np.ndarray) & (type(covariance) != np.ndarray):
        return sqrt(matMult(matMult(np.ndarray(wghts), np.ndarray(covariance)), [[x] for x in np.ndarray(wghts)])[0])
    else:
        return sqrt(matMult(matMult(wghts, covariance), [[x] for x in wghts])[0])


def get_graph_vectors(result: np.ndarray) -> Tuple[Any, Any]:
    return np.average(result, axis=-1).tolist(), np.ma.std(result, axis=-1).tolist()


def monte_carlo_sim(asset_weightings: Union[Sequence[float], np.ndarray],
                    annual_returns: Union[Sequence[float], np.ndarray],
                    convariance: Union[Sequence[Sequence[float]], np.ndarray],
                    steps: int,
                    initial_investment: float = 1,
                    fee: float = 0.0,
                    adds: int = 0) -> SimulationResults:
    rtrn = np.log(1 + simulation_return(asset_weightings, annual_returns) - fee)
    std = sim_std(np.array(asset_weightings), convariance)
    partial_random_walk = partial(random_walk,
                                  annual_return=rtrn,
                                  std=std,
                                  period=steps,
                                  step=1, contributions=adds)
    result = np.apply_along_axis(partial_random_walk, -1, np.ones((1_000, 1)) * initial_investment)
    mean, var = get_graph_vectors(result.T)
    return SimulationResults(portfolio_return=np.math.exp(rtrn) - 1,
                             portfolio_risk=std,
                             simulation_mean=mean,
                             simulation_std=var,
                             x_max=steps,
                             y_max=max(mean) + max(var))


def black_shcoles(rtrn: float, std: float, init: float) -> float:
    return init * np.math.exp(random.normalvariate(rtrn - 0.5 * std ** 2, std))


def random_walk(simulation: np.array, annual_return: float, std: float, period: int, step: int, contributions: float = 0,
    contribution_growth: float = 0.0) -> Union[np.ndarray, list]:
    if step >= period:
        return np.append(simulation, black_shcoles(annual_return, std, simulation[-1]))
    else:
        return random_walk(np.append(simulation, black_shcoles(annual_return, std, simulation[-1]) + contributions * (1 + contribution_growth) ** step),
                           annual_return, std, period, step + 1, contributions, contribution_growth
        )


def matMult(a, b):
    """
    Matrix multiplication
    :param a: vector/matrix a
    :param b: vector/matrix b
    :return: cross product of a and b

    """
    return np.matmul(a, b)
