from typing import Callable

from investment_simulator.tax import income_tax, nz_tax_brackets


def annual_growth(step: int, rate: float) -> float:
    """
    Calculates the rate of compounding for the number of years input
    :param step:
    :param rate:
    :return:
    """
    return (1 + rate) ** step


def continuous_contributions(
    initial_contribution: float, contribution_growth: float = 0.0
) -> Callable:
    """

    :param initial_contribution:
    :param contribution_growth:
    :return:
    """

    def inner(step: int) -> float:
        return initial_contribution * annual_growth(step, contribution_growth)

    return inner


def percentage_income_contributions(
    income: float,
    contribution_rate: float,
    income_growth: float = 0.0,
    tax_function: Callable = (lambda x: 0),
) -> Callable:
    """

    :param income:
    :param contribution_rate:
    :param income_growth:
    :param tax_function:
    :return:
    """

    def inner(step: int) -> float:
        compounded_income = income * annual_growth(step, income_growth)
        return (compounded_income - tax_function(compounded_income)) * contribution_rate

    return inner


def kiwi_saver_contributions(
    income: float,
    contribution_rate: float,
    employer_rate: float,
    income_growth: float,
    gov_contributions: float = 521.43,
) -> Callable:
    """

    :param income:
    :param contribution_rate:
    :param employer_rate:
    :param income_growth:
    :param gov_contributions:
    :return:
    """

    def inner(step: int) -> float:
        return (
            income
            * (contribution_rate + employer_rate)
            * annual_growth(step, income_growth)
            + gov_contributions
        )

    return inner
