from numpy import ones
from investment_simulator import portfolio_simulation as ps


def test_graph_vectors():
    result_mean, result_std = ps.get_graph_vectors(ones(100))
    assert result_std == 0
    assert result_mean == 1
