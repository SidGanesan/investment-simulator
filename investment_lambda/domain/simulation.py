from pprint import pprint
from typing import Union

import numpy as np

from investment_lambda.domain.portfolios import get_covariance_matrix
from investment_simulator import portfolios as p
from investment_simulator.contributions import continuous_contributions


def simulation_handler(s3Client):
    def handle(model, request):
        r, w, f = get_asset_allocations(request["holdings"])
        covariance_matrix = get_covariance_matrix(s3Client)(model)
        pprint(f)
        result = p.growth_simulation(
            asset_weightings=w,
            annual_returns=r,
            covariance=covariance_matrix,
            steps=request["simulation_length"],
            initial_investment=request["portfolio_balance"],
            fee=f,
            contribution_function=continuous_contributions(
                request["contributions"], 0.02
            ),
        )
        return result, graph_results(result)

    return handle


def get_asset_allocations(holdings):
    returns = list(map(lambda a: a.get("r"), holdings))
    weightings = list(map(lambda a: a.get("weighting"), holdings))
    fees = list(map(lambda a: a.get("fee"), holdings))
    return returns, weightings, np.dot(weightings, fees)


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
