import jsonpickle as j
from botocore.client import BaseClient

from investment_lambda.types.portfolio import PortfolioConstants, Portfolio

bucket_name = "model.portfolio.jarden.io"


def get_portfolio(s3Client: BaseClient):
    def inner(model: str, name: str):
        pass

    return inner


def get_all_for_model(s3Client: BaseClient):
    def inner(model: str):
        pass

    return inner


def put_portfolio_constants(s3Client: BaseClient):
    def inner(constants: PortfolioConstants):
        return s3Client.put_object(
            Body=j.encode(constants),
            Bucket=bucket_name,
            Key="portfolios/" + constants.model,
        )

    return inner


def put_portfolio(s3Client: BaseClient):
    def inner(portfolio: Portfolio):
        return s3Client.put_object(
            Body=j.encode(portfolio),
            Bucket=bucket_name,
            Key="portfolios/" + portfolio.model,
        )

    return inner
