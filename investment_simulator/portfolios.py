from dataclasses import dataclass

import numpy as np
from typing import Union, Tuple, List, Sequence, Callable

from investment_simulator.contributions import continuous_contributions
from investment_simulator.utils import simulation_parameters

ArrayLike = Union[Sequence[float], np.ndarray]
ArrayLike2D = Union[Sequence[ArrayLike], np.ndarray]


@dataclass(frozen=True)
class PortfolioResults:
    portfolio_return: float
    portfolio_risk: float
    simulation_mean: List[float]
    simulation_std: List[float]


__all__ = [
    "growth_simulation",
    "PortfolioResults",
]


def get_graph_vectors(result: np.ndarray) -> Tuple[List[float], List[float]]:
    """
    Calculates lists of the mean simulation result and standard deviation
    :param result: Matrix of simulations
    :return: mean outcome and standard deviation of each step in the simulation
    """
    mean_ = np.mean(np.array(result), axis=-1)
    std = np.sqrt(np.mean((result - np.expand_dims(mean_, 1)) ** 2, axis=-1))
    return mean_.tolist(), std.tolist()


def growth_simulation(
    asset_weightings: ArrayLike,
    annual_returns: ArrayLike,
    covariance: ArrayLike2D,
    steps: int,
    initial_investment: float = 1,
    fee: float = 0.0,
    simulations: int = 1_000,
    contribution_function: Callable[[int], float] = continuous_contributions(0.0, 0.0),
    random_gen: np.random.Generator = np.random,
) -> PortfolioResults:
    """
    Calculates a Monte Carlo Simulation of a given Portfolio and asset metrics
    to model the potential growth of the portfolio over time.
    :param asset_weightings: Vector of portfolio allocation weights adding to 1
    :param annual_returns: Vector of asset returns as percentages
    :param covariance: Covariance matrix of portfolio allocations
    :param steps: Number of years to simulate
    :param initial_investment: Initial value of the portfolio
    :param fee: percentage based annual fee on holdings. Default 0
    :param simulations: Number of simulations run
    :param contribution_function: Function that gives additional contributions to the portfolio at regular intervals
    :param random_gen: The random generator to use. Default np.random
    :return: SimulationResult Object that wraps key statistics of the simulation
    """
    investment_return, investment_risk = simulation_parameters(
        asset_weightings=asset_weightings,
        annual_returns=annual_returns,
        covariance=covariance,
        fee=fee,
    )
    simulation = np.empty((steps + 1, simulations), dtype=np.float32)
    simulation[0] = initial_investment

    random_walk = np.exp(
        random_gen.normal(
            investment_return - 0.5 * investment_risk ** 2,
            investment_risk,
            simulation.shape,
        )
    )
    for step in range(1, steps + 1):
        simulation[step] = simulation[step - 1] * random_walk[step]

    mean_, std = get_graph_vectors(simulation)
    for step in range(1, steps):
        mean_[step] += contribution_function(step)

    return PortfolioResults(
        portfolio_return=np.exp(investment_return) - 1,
        portfolio_risk=investment_risk,
        simulation_mean=mean_,
        simulation_std=std,
    )
