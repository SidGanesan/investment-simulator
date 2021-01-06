import operator as o
from functools import reduce
from typing import List, Dict, Callable, Optional


def cumulative_tax(income: float) -> Callable:
    """

    :param income:
    :return:
    """

    def inner(bracket: Dict[str, Optional[float]]) -> float:
        """

        :param bracket:
        :return:
        """
        if bracket["max"] is None:  # must handle maximum bracket case first
            return max((income - bracket["min"]) * bracket["rate"], 0)
        if income <= bracket["max"]:  # income
            return max((income - bracket["min"]) * bracket["rate"], 0)
        else:
            return bracket["sum"]

    return inner


def accumulated_brackets(
    bracket: Dict[str, Optional[float]]
) -> Dict[str, Optional[float]]:
    """
    Adds the cumulative tax paid for a bracket if the income where to
    exceed the maximum point of the tax bracket
    :param bracket: Tax Bracket with min, max, and rate
    :return: new tax bracket with cumulative tax added
    """
    if bracket["max"] is not None:
        bracket["sum"] = (bracket["max"] - bracket["min"]) * bracket["rate"]
    else:
        bracket["sum"] = 0
    return bracket


def income_tax(tax_brackets: List[Dict[str, Optional[float]]]) -> Callable:
    """
    Calculates the amount of income tax to be deducted
    :param tax_brackets: list of brackets
    :return:
    """

    def inner(income: float) -> float:
        """

        :param income:
        :return:
        """
        cumulative_brackets = tuple(map(accumulated_brackets, tax_brackets))
        return reduce(
            o.add,
            tuple(map(cumulative_tax(income), cumulative_brackets)),
            0,
        )

    return inner


def nz_tax_brackets() -> List[Dict[str, Optional[float]]]:
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
            "max": None,
            "min": 180_000,
            "rate": 0.39,
        },
    ]
