import numpy as np
from typing import Union, Sequence, Tuple

ArrayLike = Union[Sequence[float], np.ndarray]
ArrayLike2D = Union[Sequence[ArrayLike], np.ndarray]


def simulation_parameters(
    asset_weightings: ArrayLike,
    annual_returns: ArrayLike,
    covariance: ArrayLike2D,
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
    portfolio_return = np.log(
        1
        + simulation_return(weights=asset_weightings, asset_returns=annual_returns)
        - fee
    )
    portfolio_risk = simulation_risk(
        weights=np.array(asset_weightings),
        covariance=covariance,
    )
    return portfolio_return, portfolio_risk


def simulation_return(
    weights: ArrayLike,
    asset_returns: ArrayLike,
) -> float:
    """
    Calculate the return of a portfolio based on asset weights and returns
    of the assets. The weightings and returns are assumed to be indexed the
    same.
    :param weights: Vector of portfolio allocation weights adding to 1
    :param asset_returns: Vector of asset returns as percentages
    :return: return as a percentage
    """
    if not isinstance(weights, np.ndarray):
        weights = np.array(weights)
    if not isinstance(asset_returns, np.ndarray):
        asset_returns = np.array(asset_returns)
    return float(weights.dot(asset_returns))


def simulation_risk(
    weights: ArrayLike,
    covariance: ArrayLike2D,
) -> float:
    """
    Calculate the cross product of the asset weights and the covariance matrix
    to obtain the risk of the portfolio. The weightings and covariance matrix
    are assumed to be indexed the same.
    :param weights: Vector of portfolio allocation weights
    :param covariance: Covariance matrix of portfolio allocations
    :return: standard deviation of portfolio
    """
    if not isinstance(weights, np.ndarray):
        weights = np.array(weights)
    if not isinstance(covariance, np.ndarray):
        covariance = np.array(covariance)
    return np.sqrt(
        np.matmul(np.matmul(weights, covariance), np.expand_dims(weights, 1))
    ).item()


def annuity(tot_sum: float, required_return: float, period: int) -> float:
    """
    Calculate the annuity payments for a given sum and period, at the rate of return given.
    :param tot_sum: Present Value of the annuity required
    :param required_return: Return required for annuity
    :param period: Duration
    :return: Annual payments Annuity
    """
    v = 1 / (1 + required_return)
    a_t = (1 - v ** period) / required_return
    return tot_sum / a_t
