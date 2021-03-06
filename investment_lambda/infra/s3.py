from typing import Dict

from botocore.client import BaseClient

bucket = "model.portfolio.jarden.io"


def list_from_s3(s3Client: BaseClient):
    def inner(prefix):
        return s3Client.list_objects(Bucket=bucket, Prefix=prefix)["Contents"]

    return inner


def get_from_s3(s3Client: BaseClient):
    def inner(key: str):
        result = s3Client.get_object(Bucket=bucket, Key=key)
        return result["Body"].read()

    return inner


def put_into_s3(s3Client: BaseClient):
    def inner(obj: Dict, key: str):
        return s3Client.put_object(
            Body=obj,
            Bucket=bucket,
            Key=key,
        )

    return inner
