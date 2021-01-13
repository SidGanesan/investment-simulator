import operator as o
from functools import reduce
from typing import List, Dict, Callable


def cumulative_tax(income: float) -> Callable:
    """
    Function that gives the amount of tax due based on the bracket
    :param income: Total Income
    :return: Function that returns tax given bracket
    """

    def inner(bracket: Dict[str, float]) -> float:
        return (
            max((income - bracket["min"]) * bracket["rate"], 0)
            if income <= bracket["max"]
            else bracket["sum"]
        )

    return inner


def accumulated_brackets(bracket: Dict[str, float]) -> Dict[str, float]:
    """
    Adds the cumulative tax paid for a bracket if the income where to
    exceed the maximum point of the tax bracket
    :param bracket: Tax Bracket with min, max, and rate
    :return: new tax bracket with cumulative tax added
    """
    bracket["sum"] = (bracket["max"] - bracket["min"]) * bracket["rate"]
    return bracket


def income_tax(tax_brackets: List[Dict[str, float]]) -> Callable:
    """
    Calculates the amount of income tax to be deducted
    :param tax_brackets: list of brackets
    :return: function that returns tax due given income
    """

    def inner(income: float) -> float:
        cumulative_brackets = tuple(map(accumulated_brackets, tax_brackets))
        return reduce(
            o.add,
            tuple(map(cumulative_tax(income), cumulative_brackets)),
            0,
        )

    return inner


def nz_tax_brackets() -> List[Dict[str, float]]:
    """
    :return: NZ Tax Brackets for April 1st 2021
    """
    return [
        {
            "max": 14_000,
            "min": 0,
            "rate": 0.105,
        },
        {
            "max": 48_000,
            "min": 14_000,
            "rate": 0.175,
        },
        {
            "max": 70_000,
            "min": 48_000,
            "rate": 0.30,
        },
        {
            "max": 180_000,
            "min": 70_000,
            "rate": 0.33,
        },
        {
            "max": float("inf"),
            "min": 180_000,
            "rate": 0.39,
        },
    ]
