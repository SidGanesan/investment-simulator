import json
from typing import Dict, List

from investment_lambda.repository.portfolio_repo import (
    add_portfolio_to_repo,
    get_portfolio,
    get_all_for_model,
)


def get_handler(model: str, name: str) -> Dict:
    result = serialise_portfolio(get_portfolio(model, name))
    return result


def get_all_handler(model: str):
    result = list(map(serialise_portfolio, get_all_for_model(model)))
    return result


def put_handler(request: Dict) -> List[Dict]:
    if not validate_add_portfolio(request):
        raise Exception("invalid portfolio")
    result = list(map(add_portfolio_to_repo(request), request["portfolios"]))
    return result


def validate_add_portfolio(request) -> bool:
    return True


def serialise_portfolio(portfolio: Dict) -> Dict:
    portfolio["holdings"] = json.loads(portfolio["holdings"])
    del portfolio["constants"]
    return portfolio
