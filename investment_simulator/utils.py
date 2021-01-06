from typing import Union, Sequence
from numpy import ndarray, array, matmul
from numpy.ma import sqrt, exp
from numpy.random import normal


def simulation_return(
    weights: Union[Sequence[float], ndarray],
    asset_returns: Union[Sequence[float], ndarray],
) -> float:
    """
    Calculate the return of a portfolio based on asset weights and returns
    of the assets. The weightings and returns are assumed to be indexed the
    same.
    :param weights: Vector of portfolio allocation weights adding to 1
    :param asset_returns: Vector of asset returns as percentages
    :return: return as a percentage
    """
    if not isinstance(weights, ndarray):
        weights = array(weights)
    if not isinstance(asset_returns, ndarray):
        asset_returns = array(asset_returns)
    return weights.dot(asset_returns)


def simulation_risk(
    weights: Union[Sequence[float], ndarray],
    covariance: Union[Sequence[Sequence[float]], ndarray],
) -> float:
    """
    Calculate the cross product of the asset weights and the covariance matrix
    to obtain the risk of the portfolio. The weightings and covariance matrix
    are assumed to be indexed the same.
    :param weights: Vector of portfolio allocation weights
    :param covariance: Covariance matrix of portfolio allocations
    :return: standard deviation of portfolio
    """
    if not isinstance(weights, ndarray):
        weights = array(weights)
    if not isinstance(covariance, ndarray):
        covariance = array(covariance)
    return sqrt(
        matMult(matMult(weights, covariance), [[x] for x in weights])[
            0
        ]  # Unwrap result from list
    )


def matMult(
    a: Union[
        Sequence[float], Sequence[Sequence[float]], ndarray
    ],  # 1D list, 2D list, or ndarray
    b: Union[
        Sequence[float], Sequence[Sequence[float]], ndarray
    ],  # 1D list, 2D list, or ndarray
) -> ndarray:
    """
    Matrix multiplication with type checks
    :param a: vector/matrix a
    :param b: vector/matrix b
    :return: cross product of a and b
    """
    if not isinstance(a, ndarray):
        a = array(a)
    if not isinstance(b, ndarray):
        b = array(b)
    return matmul(a, b)


def stochastic_compounding(
    continuous_return: float,
    investment_risk: float,
    investment: float,
) -> float:
    """
    Compound returns for a period randomly based on a normal distribution of returns.
    :param continuous_return: Continuously compounded return as a percentage
    :param investment_risk: Risk measured as standard deviation as a percentage
    :param investment: Dollar amount being compounded
    :return: investment after one period
    """
    return investment * exp(
        normal(continuous_return - 0.5 * investment_risk ** 2, investment_risk)
    )
