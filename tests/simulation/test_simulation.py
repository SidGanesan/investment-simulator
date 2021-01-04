from numpy.ma import array

from investment_simulator import portfolio_simulation as ps
import pytest


@pytest.fixture
def simulation_parameters_fixture():
    return [0.5, 0.5], [0.1, 0.1], [[1.0, 0.0], [0.0, 1.0]]


def test_simulation_parameters_l(simulation_parameters_fixture):
    result = ps.simulation_parameters(simulation_parameters_fixture[0],
                                      simulation_parameters_fixture[1],
                                      simulation_parameters_fixture[2])
    assert result == (0.09531017980432493, 0.7071067811865476)


def test_simulation_parameters_np(simulation_parameters_fixture):
    result = ps.simulation_parameters(array(simulation_parameters_fixture[0]),
                                      array(simulation_parameters_fixture[1]),
                                      array(simulation_parameters_fixture[2]))
    assert result == (0.09531017980432493, 0.7071067811865476)
