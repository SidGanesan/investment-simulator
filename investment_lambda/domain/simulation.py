from typing import Union

from investment_simulator import portfolios as p


def handle(event):
    r, w = get_asset_allocations(event["holdings"])
    result = p.growth_simulation(r, w, covariance_matrix, event["simulation_length"])
    return result, graph_results(result)


def get_asset_allocations(holdings):
    returns = list(map(lambda a: a.get("return"), holdings))
    weightings = list(map(lambda a: a.get("weighting"), holdings))
    return returns, weightings


def graph_results(result: Union[p.PortfolioResults, p.InvestmentResults]):
    return {
        "graph_points": [
            {
                "x": i,
                "y": m,
                "u1": m + s,
                "l1": m - s,
                "std": s,
            }
            for (i, (m, s)) in enumerate(
                zip(result.simulation_mean, result.simulation_std)
            )
        ],
        "y_max": len(result.simulation_mean) - 1,
        "x_max": max(result.simulation_mean) + max(result.simulation_std),
    }


covariance_matrix = [
    [
        0.000,
        0.000,
        -0.002,
        0.000,
        0.000,
        -0.001,
        0.001,
    ],
    [
        0.000,
        0.001,
        -0.002,
        -0.002,
        -0.002,
        -0.001,
        0.001,
    ],
    [
        -0.002,
        -0.002,
        0.024,
        0.020,
        0.016,
        0.016,
        -0.001,
    ],
    [
        0.000,
        -0.002,
        0.020,
        0.031,
        0.019,
        -0.013,
        0.002,
    ],
    [
        0.000,
        -0.002,
        0.016,
        0.019,
        0.021,
        0.011,
        0.007,
    ],
    [
        -0.001,
        -0.001,
        0.016,
        0.013,
        0.011,
        0.017,
        -0.001,
    ],
    [
        0.001,
        0.001,
        -0.002,
        0.002,
        0.007,
        -0.001,
        0.010,
    ],
]
