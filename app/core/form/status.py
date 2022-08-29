from enum import Enum


class AnswerStatus(Enum):
    WAIT = "WAIT"
    CHECK = "CHECK"
    REFUSAL = "REFUSAL"
    ACCEPTED = "ACCEPTED"

