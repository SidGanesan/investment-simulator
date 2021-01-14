from numpy import ones

from investment_simulator import portfolios as ps


def test_graph_vectors():
    result_mean, result_std = ps.get_graph_vectors(ones((100, 1)))
    assert result_std[0] == 0
    assert result_mean[0] == 1
