from dataclasses import asdict
from pprint import pprint

from investment_lambda.domain import simulation
from investment_simulator.portfolios import PortfolioResults

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def handler():
    return {"status": 200, "body": "hello world"}


@app.route("/simulate", methods=["POST"])
def simulation_handler():
    pprint(request.json)
    sim, graphs = simulation.handle(request.json)
    return {
        "status": 200,
        "payload": {
            "simulationResults": sim,
            "graphingData": graphs,
        },
    }
