from typing import Dict

from botocore.client import BaseClient

from investment_lambda.repository.questionnaire_repo import (
    get_questions_for_model,
    put_questions,
)
from investment_lambda.types.questionnaire import (
    RiskOption,
    RiskQuestion,
    Questionnaire,
)


def serialise_questions(questions):
    return questions


def get_questions_handler(s3Client: BaseClient):
    def inner(model: str):
        return serialise_questions(get_questions_for_model(s3Client)(model))

    return inner


def validate_questionnaire(questionnaire: Dict):
    questionnaire["questions"] = list(
        map(validate_question, questionnaire["questions"])
    )
    return Questionnaire(**questionnaire)


def validate_question(question: Dict):
    question["options"] = list(map(lambda x: RiskOption(**x), question["options"]))
    return RiskQuestion(**question)


def add_questions(s3Client: BaseClient):
    def inner(questionnaire: Dict):
        valid_questionnaire = validate_questionnaire(questionnaire)
        return put_questions(s3Client)(valid_questionnaire)

    return inner
