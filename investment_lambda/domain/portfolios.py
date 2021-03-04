import json
from typing import Dict, List

from investment_lambda.repository.portfolio_repo import (
    add_portfolio_to_repo,
    get_portfolio,
)


def get_handler(name: str, model: str) -> Dict:
    result = get_portfolio(name, model)
    return result


def put_handler(request: Dict) -> List[Dict]:
    if not validate_add_portfolio(request):
        raise Exception("invalid portfolio")
    result = list(map(add_portfolio_to_repo(request), request["portfolios"]))
    return result


def validate_add_portfolio(request) -> bool:
    return True
