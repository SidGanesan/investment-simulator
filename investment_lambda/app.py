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


@app.route("/portfolio", methods=["POST"])
def get_portfolio_handler():
    portfolio = portfolios.post_handler(request.json)
    return {"status": 200, "body": portfolio}


@app.route("/portfolio", methods=["PUT"])
def add_portfolio_handler():
    result = portfolios.put_handler(request.json)
    return {"status": 200, "body": result}
