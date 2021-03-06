import jsonpickle as j
from typing import Dict, List

from botocore.client import BaseClient

from investment_lambda.repository.portfolio_repo import (
    get_portfolio,
    get_all_for_model,
    put_portfolio_constants,
    put_portfolio,
)
from investment_lambda.types.portfolio import (
    PortfolioConstants,
    Portfolio,
    PortfolioHolding,
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


def validate_constants(model: str):
    def inner(constants: Dict):
        return PortfolioConstants(model=model, **constants)

    return inner


def validate_holdings(holding):
    return PortfolioHolding(**holding)


def validate_portfolios(model: str):
    def inner(portfolio: Dict):
        portfolio["holdings"] = list(map(validate_holdings, portfolio["holdings"]))
        return Portfolio(model=model, **portfolio)

    return inner


def put_handler(s3Client: BaseClient):
    def inner(model: str, request: Dict) -> Dict:
        constants = validate_constants(model)(request["constants"])
        portfolios = list(map(validate_portfolios(model), request["portfolios"]))
        return {
            "constants": put_portfolio_constants(s3Client)(constants),
            "portfolios": list(map(put_portfolio(s3Client), portfolios)),
        }

    return inner


def serialise_portfolio(portfolio: Dict) -> Dict:
    return j.decode(portfolio)
