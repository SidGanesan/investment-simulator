import json
from pprint import pprint

from investment_lambda.repository.portfolio_model import Portfolio


def add_portfolio_to_repo(portfolio):
    pprint(portfolio)
    portfolio_name = portfolio["name"]
    risk_score = portfolio["score"]
    item = Portfolio(
        portfolio_name,
        risk_score,
        make_up=portfolio["make_up"],
    )
    return item.save()


def get_portfolio(name: str, score: int):
    repo = Portfolio()
    item = dict(repo.get(name, score))
    item["make_up"] = json.loads(item["make_up"])
    return dict(item)
