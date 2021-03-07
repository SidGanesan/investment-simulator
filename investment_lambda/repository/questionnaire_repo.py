import jsonpickle as j
from botocore.client import BaseClient

from investment_lambda.infra.s3 import get_from_s3, put_into_s3
from investment_lambda.types.questionnaire import Questionnaire


def get_questions_for_model(s3Client: BaseClient):
    def inner(model: str):
        return get_from_s3(s3Client)(key="questionnaires/" + model)

    return inner


def put_questions(s3Client):
    def inner(questions: Questionnaire):
        return put_into_s3(s3Client)(
            j.encode(questions), "questionnaires/" + questions.model
        )

    return inner
