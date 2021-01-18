import pytest
from numpy import log, sqrt

from investment_simulator import portfolios as ps
from investment_simulator.portfolios import PortfolioResults, InvestmentResults


@pytest.fixture
def simulation_parameters_fixture():
    return [0.5, 0.5], [0.1, 0.1], [[0.001, 0.0], [0.0, 0.001]]


def test_monte_carlo(simulation_parameters_fixture):
    steps = 10
    result = ps.growth_simulation(
        simulation_parameters_fixture[0],
        simulation_parameters_fixture[1],
        simulation_parameters_fixture[2],
        steps,
    )
    assert isinstance(result, PortfolioResults)
    assert len(result.simulation_mean) == steps + 1  # add one for initial step


def test_simulation_parameters_l(simulation_parameters_fixture):
    result = ps.simulation_parameters(
        simulation_parameters_fixture[0],
        simulation_parameters_fixture[1],
        simulation_parameters_fixture[2],
    )
    assert result == (log(1.1), sqrt(0.0005))


def test_success_probability(simulation_parameters_fixture):
    steps = 10
    result = ps.growth_simulation(
        asset_weightings=simulation_parameters_fixture[0],
        annual_returns=simulation_parameters_fixture[1],
        covariance=simulation_parameters_fixture[2],
        steps=steps,
        investment_goal=2.5,
    )
    assert isinstance(result, InvestmentResults)
    assert pytest.approx(result.probability, 0)
    assert pytest.approx(result.probability, 1)
    assert pytest.approx(result.additional_savings, 0)
