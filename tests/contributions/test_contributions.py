from investment_simulator.contribution_functions import *


def test_annual_growth():
    result = annual_growth(1, 0.1)
    assert result == 1.1


def test_continuous():
    result = continuous_contributions(100, 0.1)(1)
    assert round(result) == 110  # stupid 110.00000000000001 error


def test_income():
    result = percentage_income_contributions(10_000, 0.1)
    assert result(1) == 1_000
