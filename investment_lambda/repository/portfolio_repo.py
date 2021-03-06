from pprint import pprint

from botocore.client import BaseClient

from investment_lambda.repository.portfolio_model import Portfolio


def add_portfolio_to_repo(request):
    def inner(portfolio):
        pprint(portfolio)
        portfolio_model = portfolio.get("model")
        portfolio_name = portfolio.get("name")
        item = Portfolio(
            portfolio_model,
            portfolio_name,
            risk_score=portfolio.get("score"),
            holdings=portfolio.get("holdings"),
            constants=request.get("constants"),
        )
        return item.save()

    return inner


def get_portfolio(s3Client: BaseClient):
    def inner(model: str, name: str):
        item = Portfolio().get(model, name).as_dict()
        return item

    return inner


def get_all_for_model(s3Client: BaseClient):
    def inner(model: str):
        items = map(lambda x: x.as_dict(), Portfolio().query(model))
        return list(items)

    return inner
