from dataclasses import dataclass

import numpy as np
from typing import Union, Tuple, List, Sequence, Callable
from dataclasses import asdict

from investment_simulator.contributions import continuous_contributions
from investment_simulator.utils import simulation_parameters, annuity
import scipy.stats as stats

ArrayLike = Union[Sequence[float], np.ndarray]
ArrayLike2D = Union[Sequence[ArrayLike], np.ndarray]


@dataclass(frozen=True)
class PortfolioResults:
    portfolio_return: float
    portfolio_risk: float
    simulation_mean: List[float]
    simulation_std: List[float]


@dataclass(frozen=True)
class InvestmentResults(PortfolioResults):
    goal: float
    probability: float
    additional_savings: float


__all__ = [
    "growth_simulation",
    "PortfolioResults",
    "InvestmentResults",
]


def growth_simulation(
    asset_weightings: ArrayLike,
    annual_returns: ArrayLike,
    covariance: ArrayLike2D,
    steps: int,
    initial_investment: float = 1,
    fee: float = 0.0,
    simulations: int = 1_000,
    contribution_function: Callable[[int], float] = continuous_contributions(0.0, 0.0),
    investment_goal: float = 0,
    random_gen: np.random.Generator = np.random,
) -> Union[PortfolioResults, InvestmentResults]:
    """
    Calculates a Monte Carlo Simulation of a given Portfolio and asset metrics.
    to model the potential growth of the portfolio over time.
    :param asset_weightings: Vector of portfolio allocation weights adding to 1.
    :param annual_returns: Vector of asset returns as percentages.
    :param covariance: Covariance matrix of portfolio allocations.
    :param steps: Number of years to simulate.
    :param initial_investment: Initial value of the portfolio.
    :param fee: percentage based annual fee on holdings. Default 0.
    :param simulations: Number of simulations run.
    :param contribution_function: Function that gives additional contributions to the portfolio at regular intervals.
    :param investment_goal: Desired end amount of investment.
    :param random_gen: The random generator to use. Default np.random.
    :return: SimulationResult Object that wraps key statistics of the simulation.
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
        simulation[step] = simulation[step - 1] * random_walk[
            step
        ] + contribution_function(step)

    mean_, std = get_graph_vectors(simulation)

    result = PortfolioResults(
        portfolio_return=np.exp(investment_return) - 1,
        portfolio_risk=investment_risk,
        simulation_mean=mean_,
        simulation_std=std,
    )

    return (
        result
        if investment_goal == 0
        else success_probabilities(investment_goal, result)
    )


def difference_annuity(
    result: float,
    goal: float,
    required_return: float,
    period: int,
) -> float:
    """
    Calculate the annuity require to make up payments to reach a median goal level.
    :param result: Current median outcome of sim.
    :param goal: Required median outcome.
    :param required_return: Percentage annual return.
    :param period: Duration of investment.
    :return: The positive goal required to meet goal.
    """
    return max(annuity(goal - result, required_return, period), 0)


def success_probabilities(goal: float, sim: PortfolioResults) -> InvestmentResults:
    """
    Calculate the probability of achieving a goal given investments simulation. This assumes the
    normal distribution of outcomes.
    :param goal: Desired amount at end of investing period.
    :param sim: Portfolio Simulation.
    :return: Investment Goal.
    """
    # Calculate Z score
    _mean = sim.simulation_mean[-1]
    _std = sim.simulation_std[-1]
    _probability = 1 - stats.norm(_mean, _std).cdf(
        goal
    )  # Cumulative probability of achieving goal

    return InvestmentResults(
        **asdict(sim),
        goal=goal,
        probability=_probability,
        additional_savings=difference_annuity(
            result=_mean,
            goal=goal,
            required_return=sim.portfolio_return,
            period=len(sim.simulation_mean) - 1,
        ),
    )


def get_graph_vectors(result: np.ndarray) -> Tuple[List[float], List[float]]:
    """
    Calculates lists of the mean simulation result and standard deviation.
    :param result: Matrix of simulations.
    :return: mean outcome and standard deviation of each step in the simulation.
    """
    # noinspection PyUnresolvedReferences
    mean_ = np.mean(np.array(result), axis=-1)  # numpy types broken
    # noinspection PyUnresolvedReferences
    std = np.sqrt(
        np.mean((result - np.expand_dims(mean_, 1)) ** 2, axis=-1)
    )  # numpy types broken
    return mean_.tolist(), std.tolist()
