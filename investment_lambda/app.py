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
        "payload": {
            "simulationResults": sim,
            "graphingData": graphs,
        },
    }


@app.route("/portfolio/<string:model>/<string:name>", methods=["GET"])
def get_portfolio_handler(name: str, model: str):
    portfolio = portfolios.get_handler(name, model)
    return {"status": 200, "body": portfolio}


@app.route("/portfolio/", methods=["PUT"])
def add_portfolio_handler(model: str, score: int) -> Dict:
    result = portfolios.put_handler(request.json)
    return {"status": 200, "body": result}
