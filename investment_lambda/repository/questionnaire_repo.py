from botocore.client import BaseClient
import jsonpickle as j

from investment_lambda.types.questionnaire import Questionnaire

bucket_name = "model.portfolio.jarden.io"


def get_questions_for_model(s3Client: BaseClient):
    def inner(model: str):
        result = s3Client.get_object(
            Bucket=bucket_name, Key="questionnaires/" + model + ".json"
        )
        result["Body"] = result["Body"].read()
        return

    return inner


def put_questions(s3Client):
    def inner(questions: Questionnaire):
        return s3Client.put_object(
            Body=j.encode(questions),
            Bucket=bucket_name,
            Key="questionnaires/" + questions.model,
        )

    return inner
