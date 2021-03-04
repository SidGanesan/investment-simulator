from pprint import pprint

from investment_lambda import simulation
from investment_simulator.portfolios import PortfolioResults

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def handler():
    return {"status": 200, "body": "hello world"}


@app.route("/simulate", methods=["POST"])
def simulation_handler():
    pprint(request.json)
    result: PortfolioResults = simulation.handle(request.json)
    # return jsonify(
    #     graph=[
    #         {
    #             'x': i,
    #             'y': m,
    #             'u1': m + s,
    #             'l1': m - s,
    #             'std': s,
    #         } for (i, (m, s)) in enumerate(zip(result.simulation_mean, result.simulation_std))
    #     ],
    #     portfolio_return=result.portfolio_return,
    #     portfolio_risk=result.portfolio_risk,
    #     y_max=result.y_max,
    #     x_max=result.x_max,
    # )
    return {"status": 200, "body": "simulate"}
