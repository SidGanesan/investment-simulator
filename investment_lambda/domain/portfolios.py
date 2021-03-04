import json
from typing import Dict, List

from investment_lambda.repository.portfolio_repo import (
    add_portfolio_to_repo,
    get_portfolio,
)


def post_handler(request: Dict) -> Dict:
    result = get_portfolio(request["name"], request["score"])

    return result


def put_handler(request: Dict) -> List[Dict]:
    if not validate_add_portfolio(request):
        raise Exception("invalid portfolio")
    result = list(map(add_portfolio_to_repo, request["portfolios"]))
    return result


def validate_add_portfolio(request) -> bool:
    return True
