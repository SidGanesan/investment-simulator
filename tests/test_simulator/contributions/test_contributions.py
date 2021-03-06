import pytest

from investment_simulator.contributions import (
    annual_growth,
    continuous_contributions,
    percentage_income_contributions,
    kiwi_saver_contributions,
)


def test_annual_growth():
    result = annual_growth(1, 0.1)
    assert result == 1.1


def test_continuous():
    result = continuous_contributions(100, 0.1)(1)
    assert result == pytest.approx(110.00, 0.005)


def test_income():
    result_1 = percentage_income_contributions(10_000, 0.1)(1)
    result_10 = percentage_income_contributions(10_000, 0.1, 0.1)(10)
    assert result_1 == pytest.approx(1_000.00, 0.005)
    assert result_10 == pytest.approx(2_593.74, 0.005)


def test_kiwi_saver():
    result_1 = kiwi_saver_contributions(75_000, 0.04, 0.04, 0, 0)(1)
    result_10 = kiwi_saver_contributions(75_000, 0.04, 0.04, 0.1, 0)(10)
    assert result_1 == pytest.approx(6_000.00, 0.005)
    assert result_10 == pytest.approx(15562.45, 0.005)
