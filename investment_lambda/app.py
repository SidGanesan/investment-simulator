from typing import Dict

import boto3
from flask import Flask, request
from flask_cors import CORS

from investment_lambda.domain import simulation, portfolios, questionnaire

app = Flask(__name__)
CORS(app)

s3Client = boto3.client(
    "s3", region_name="ap-southeast-2", endpoint_url="http://localhost:4566/"
)


@app.route("/")
def handler():
    return {"status_code": 200, "body": "hello world"}


@app.route("/simulate", methods=["POST"])
def simulation_handler():
    sim, graphs = simulation.handle(request.json)
    return {
        "status_code": 200,
        "body": {
            "simulationResults": sim,
            "graphingData": graphs,
        },
    }


@app.route("/portfolio/<string:model>/<string:name>", methods=["GET"])
def get_portfolio_handler(model: str, name: str):
    portfolio = portfolios.get_handler(s3Client)(model, name)
    return {
        "status_code": 200,
        "body": portfolio,
    }


@app.route("/portfolio/<string:model>/all", methods=["GET"])
def get_all_portfolios_handler(model: str):
    all_portfolios = portfolios.get_all_handler(s3Client)(model)
    return {
        "status_code": 200,
        "body": all_portfolios,
    }


@app.route("/portfolio/<string:model>", methods=["POST"])
def add_portfolio_handler(model: str) -> Dict:
    result = portfolios.put_handler(s3Client)(model, request.json)
    return {
        "status_code": 200,
        "body": result,
    }


@app.route("/questionnaire/<string:model>", methods=["GET"])
def get_questions_handler(model: str):
    result = questionnaire.get_questions_handler(s3Client)(model)
    return {
        "status_code": 200,
        "body": result,
    }


@app.route("/questionnaire", methods=["POST"])
def add_questions_handler() -> Dict:
    result = questionnaire.add_questions(s3Client)(request.json)
    return {
        "status_code": 200,
        "body": result,
    }


@app.errorhandler(Exception)
def handle_generic_exception(e):
    return {
        "status_code": 500,
        "body": str(e),
    }
