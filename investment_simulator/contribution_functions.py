from functools import partial
from typing import Callable
from pymonad.tools import curry


def annual_growth(step: int, rate: float) -> float:
    return (1 + rate) ** step


def continuous_contributions(
    step: int, initial_contribution: float, contribution_growth: float = 0.0
) -> float:
    return initial_contribution * annual_growth(step, contribution_growth)


def default_contributions() -> Callable:
    return partial(
        continuous_contributions, initial_contribution=0, contribution_growth=0
    )


def percentage_income_contributions(
    income: float,
    contribution_rate: float,
    income_growth: float = 0.0,
    effective_tax_rate: float = 0.0,
) -> Callable:
    def inner(step: int) -> float:
        return (
            income
            * (1 - effective_tax_rate)
            * contribution_rate
            * annual_growth(step, income_growth)
        )

    return inner


def kiwi_saver_contributions(
    income: float,
    contribution_rate: float,
    employer_rate: float,
    income_growth: float,
    effective_tax_rate: float,
    gov_contributions: float = 521.43,
) -> Callable:
    def inner(step: int) -> float:
        return (
            income
            * (1 - effective_tax_rate)
            * (contribution_rate + employer_rate)
            * annual_growth(step, income_growth)
            + gov_contributions
        )

    return inner
