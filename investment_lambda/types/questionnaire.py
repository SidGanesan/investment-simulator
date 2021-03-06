from dataclasses import dataclass
from typing import List


@dataclass()
class RiskOption:
    text: str
    score: int


@dataclass()
class RiskQuestion:
    title: str
    question: str
    options: List[RiskOption]


@dataclass
class Questionnaire:
    model: str
    questions: List[RiskQuestion]
