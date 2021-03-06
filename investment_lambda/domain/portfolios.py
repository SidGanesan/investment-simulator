import json
from typing import Dict, List

from botocore.client import BaseClient

from investment_lambda.repository.portfolio_repo import (
    add_portfolio_to_repo,
    get_portfolio,
    get_all_for_model,
)


def get_handler(s3Client: BaseClient):
    def inner(model: str, name: str):
        result = serialise_portfolio(get_portfolio(s3Client)(model, name))
        return result

    return inner


def get_all_handler(s3Client: BaseClient):
    def inner(model: str):
        result = list(map(serialise_portfolio, get_all_for_model(s3Client)(model)))
        return result

    return inner


def put_handler(s3Client: BaseClient):
    def inner(request: Dict) -> List[Dict]:
        result = list(map(add_portfolio_to_repo(request), request["portfolios"]))
        return result

    return inner


def serialise_portfolio(s3Client: BaseClient):
    def inner(portfolio: Dict) -> Dict:
        portfolio["holdings"] = json.loads(portfolio["holdings"])
        del portfolio["constants"]
        return portfolio

    return inner


# def validate_portfolio
