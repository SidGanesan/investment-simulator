from typing import Dict

from investment_lambda.domain import simulation, portfolios

from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def handler():
    return {"status": 200, "body": "hello world"}


@app.route("/simulate", methods=["POST"])
def simulation_handler():
    sim, graphs = simulation.handle(request.json)
    return {
        "status": 200,
        "holdings": {
            "simulationResults": sim,
            "graphingData": graphs,
        },
    }


@app.route("/portfolio/<string:model>/<string:name>", methods=["GET"])
def get_portfolio_handler(model: str, name: str):
    portfolio = portfolios.get_handler(model, name)
    return {
        "status": 200,
        "body": portfolio,
    }


@app.route("/portfolio/<string:model>/all", methods=["GET"])
def get_all_portfolios_handler(model: str):
    all_portfolios = portfolios.get_all_handler(model)
    return {
        "status": 200,
        "body": all_portfolios,
    }


@app.route("/portfolio/", methods=["POST"])
def add_portfolio_handler() -> Dict:
    result = portfolios.put_handler(request.json)
    return {
        "status": 200,
        "body": result,
    }
