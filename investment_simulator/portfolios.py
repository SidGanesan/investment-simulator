from functools import partial
from typing import Union, Tuple, List, Sequence, Callable

from numpy import ndarray, ones, append, apply_along_axis, array
from numpy.ma import exp, std, mean, log

from .contributions import continuous_contributions
from .utils import simulation_return, simulation_risk, stochastic_compounding
from .value_objects.simulation import SimulationResults

__all__ = [
    "monte_carlo_sim",
    "random_walk",
]


def get_graph_vectors(result: ndarray) -> Tuple[List[float], List[float]]:
    """
    Calculates lists of the mean simulation result and standard deviation
    :param result: Matrix of simulations
    :return: mean outcome and standard deviation of each step in the simulation
    """
    return mean(result, axis=-1).tolist(), std(result, axis=-1).tolist()


def simulation_parameters(
    asset_weightings: Union[Sequence[float], ndarray],
    annual_returns: Union[Sequence[float], ndarray],
    covariance: Union[Sequence[Sequence[float]], ndarray],
    fee: float = 0,
) -> Tuple[float, float]:
    """
    Calculate the continuously compounded return and standard deviation of
    the portfolio.
    :param asset_weightings: Vector of portfolio allocation weights adding to 1
    :param annual_returns: Vector of asset returns as percentages
    :param covariance: Covariance matrix of portfolio allocations
    :param fee: percentage based annual fee on holdings. Default 0
    :return: Tuple of continuously compounded return and standard deviation
    """
    portfolio_return = log(
        1
        + simulation_return(weights=asset_weightings, asset_returns=annual_returns)
        - fee
    )
    portfolio_risk = simulation_risk(
        weights=array(asset_weightings),
        covariance=covariance,
    )
    return portfolio_return, portfolio_risk


def monte_carlo_sim(
    asset_weightings: Union[Sequence[float], ndarray],
    annual_returns: Union[Sequence[float], ndarray],
    covariance: Union[Sequence[Sequence[float]], ndarray],
    steps: int,
    initial_investment: float = 1,
    fee: float = 0.0,
    simulations: int = 1_000,
    contribution_function: Callable = continuous_contributions(0.0, 0.0),
) -> SimulationResults:
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
    :param contribution_function: Function that gives additional contributions
    to the portfolio at regular intervals
    :return: SimulationResult Object that wraps key statistics of the simulation
    """
    investment_return, investment_risk = simulation_parameters(
        asset_weightings=asset_weightings,
        annual_returns=annual_returns,
        covariance=covariance,
        fee=fee,
    )
    partial_random_walk = partial(
        random_walk,
        annual_return=investment_return,
        investment_risk=investment_risk,
        period=steps,
        step=1,
        contribution_function=contribution_function,
    )
    result = apply_along_axis(
        partial_random_walk, -1, ones((simulations, 1)) * initial_investment
    )
    mean, var = get_graph_vectors(result.T)
    return SimulationResults(
        portfolio_return=exp(investment_return) - 1,
        portfolio_risk=investment_risk,
        simulation_mean=mean,
        simulation_std=var,
        x_max=steps,
        y_max=max(mean) + max(var),
    )


def random_walk(
    simulation: ndarray,
    annual_return: float,
    investment_risk: float,
    period: int,
    step: int,
    contribution_function: Callable = continuous_contributions(0.0, 0.0),
) -> Union[ndarray, list]:
    """
    Recursive implementation of a Gaussian Random Walk to model a portfolio
    :param simulation: Previous steps in the simulation
    :param annual_return: Annual return of the portfolio being modeled
    :param investment_risk: Standard deviation of the portfolio being modeled
    :param period: current step of the random walk
    :param step: total steps in the random walk
    :param contribution_function: Function that gives additional contributions
    to the portfolio at regular intervals
    :return: Single simulation of a random walk
    """
    if step >= period:
        return append(
            simulation,
            stochastic_compounding(
                continuous_return=annual_return,
                investment_risk=investment_risk,
                investment=simulation[-1],
            ),
        )
    else:
        return random_walk(
            simulation=append(
                simulation,
                stochastic_compounding(
                    continuous_return=annual_return,
                    investment_risk=investment_risk,
                    investment=simulation[-1],
                )
                + contribution_function(step),
            ),
            annual_return=annual_return,
            investment_risk=investment_risk,
            period=period,
            step=step + 1,
            contribution_function=contribution_function,
        )
