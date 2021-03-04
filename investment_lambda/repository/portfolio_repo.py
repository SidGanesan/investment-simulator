import json
from pprint import pprint

from investment_lambda.repository.portfolio_model import Portfolio


def add_portfolio_to_repo(request):
    def inner(portfolio):
        pprint(portfolio)
        portfolio_name = portfolio.get("name")
        portfolio_model = portfolio.get("model")
        item = Portfolio(
            portfolio_name,
            portfolio_model,
            risk_score=portfolio.get("score"),
            make_up=portfolio.get("make_up"),
            constants=request.get("constants"),
        )
        return item.save()

    return inner


def get_portfolio(name: str, model: str):
    repo = Portfolio()
    item = dict(repo.get(name, model))
    item["make_up"] = json.loads(item["make_up"])
    return dict(item)
