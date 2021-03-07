from typing import Dict

from botocore.client import BaseClient

from investment_lambda import env


def list_from_s3(s3Client: BaseClient):
    def inner(prefix):
        return s3Client.list_objects(Bucket=env.BUCKET, Prefix=prefix)["Contents"]

    return inner


def get_from_s3(s3Client: BaseClient):
    def inner(key: str):
        result = s3Client.get_object(Bucket=env.BUCKET, Key=key)
        return result["Body"].read()

    return inner


def put_into_s3(s3Client: BaseClient):
    def inner(obj: Dict, key: str):
        return s3Client.put_object(
            Body=obj,
            Bucket=env.BUCKET,
            Key=key,
        )

    return inner
