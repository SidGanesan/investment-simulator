from typing import Callable


def annual_growth(step: int, rate: float) -> float:
    return (1 + rate) ** step


def continuous_contributions(
    initial_contribution: float, contribution_growth: float = 0.0
) -> Callable:
    def inner(step: int) -> float:
        return initial_contribution * annual_growth(step, contribution_growth)

    return inner


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
