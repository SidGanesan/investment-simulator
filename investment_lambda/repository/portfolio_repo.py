import jsonpickle as j
from botocore.client import BaseClient

from investment_lambda.infra.s3 import get_from_s3, put_into_s3, list_from_s3
from investment_lambda.types.portfolio import PortfolioConstants, Portfolio

bucket_name = "model.portfolio.jarden.io"


def get_portfolio(s3Client: BaseClient):
    def inner(model: str, name: str):
        return get_from_s3(s3Client)(key="portfolios/" + model + "/" + name)

    return inner


def get_constants(s3Client: BaseClient):
    def inner(model: str):
        return get_from_s3(s3Client)(key="portfolios/" + model + "/constants")

    return inner


def get_all_for_model(s3Client: BaseClient):
    def inner(model: str):
        portfolio_keys = list_from_s3(s3Client)("portfolios/" + model + "/")
        portfolios = map(
            get_from_s3(s3Client), list(map(lambda x: x["Key"], portfolio_keys))
        )
        return list(portfolios)

    return inner


def put_portfolio_constants(s3Client: BaseClient):
    def inner(constants: PortfolioConstants):
        return put_into_s3(s3Client)(
            j.encode(constants), "portfolios/" + constants.model + "/constants"
        )

    return inner


def put_portfolio(s3Client: BaseClient):
    def inner(portfolio: Portfolio):
        return put_into_s3(s3Client)(
            j.encode(portfolio), "portfolios/" + portfolio.model + "/" + portfolio.name
        )

    return inner
