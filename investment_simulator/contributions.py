from typing import Callable


def annual_growth(step: int, rate: float) -> float:
    """
    Calculates the rate of compounding for the number of years input
    :param step: Number of periods to compound
    :param rate: Growth rate
    :return: Compounding multiple
    """
    return (1 + rate) ** step


def continuous_contributions(
    initial_contribution: float, contribution_growth: float = 0.0
) -> Callable[[int], float]:
    """
    Creates a function that returns a contribution, compounded by the input growth at each step
    :param initial_contribution: Initial amount to be contributed
    :param contribution_growth: Rate at which the contribution grows each step
    :return: function that returns the contribution give a step
    """

    def inner(step: int) -> float:
        return initial_contribution * annual_growth(step, contribution_growth)

    return inner


def percentage_income_contributions(
    income: float,
    contribution_rate: float,
    income_growth: float = 0.0,
    tax_function: Callable[[float], float] = (lambda x: 0),
) -> Callable[[int], float]:
    """
    Creates a function that returns a contribution based on a percentage of input income, compounded
    by the input growth at each step. The contribution is calculated as a percentage of after tax
    income. The tax system is provided as a function itself
    :param income: Total Income
    :param contribution_rate: Percentage of income to be contributed
    :param income_growth: Rate at with income increases each step
    :param tax_function: Function which returns the amount of tax required based on income
    :return: Function that takes a step and returns the contribution
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
) -> Callable[[int], float]:
    """
    Creates a function that returns a contribution based on a percentage of input income, compounded
    by the input growth at each step. The contribution is calculated as a percentage of before tax following
    the New Zealand KiwiSaver retirement savings scheme.
    :param income: Total Income
    :param contribution_rate: Percentage of income to be contributed
    :param employer_rate: Percentage of income matched by employer
    :param income_growth: Rate at with income increases each step
    :param gov_contributions: Constant government contribution
    :return: Function that takes a step and returns the contribution
    """

    def inner(step: int) -> float:
        return income * (contribution_rate + employer_rate) * annual_growth(
            step, income_growth
        ) + min(
            gov_contributions,
            income * annual_growth(step, income_growth) * contribution_rate * 0.5,
        )

    return inner
