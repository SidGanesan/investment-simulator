import pytest

from investment_simulator.allocations import allocations_simulation


@pytest.fixture
def allocations_parameters_fixture():
    return [0.1, 0.1], [[0.001, 0.0], [0.0, 0.001]]


def test_allocations(allocations_parameters_fixture):
    result = allocations_simulation(
        annual_returns=allocations_parameters_fixture[0],
        covariance=allocations_parameters_fixture[1],
        simulations=10,
    )
    assert round(result.annual_return, 2) == 0.10
    assert round(sum(result.weights) * 100) == 100
