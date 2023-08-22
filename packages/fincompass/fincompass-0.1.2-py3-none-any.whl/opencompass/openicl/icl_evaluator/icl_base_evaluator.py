"""Base Evaluator."""
from typing import List


class BaseEvaluator:
    def __init__(self) -> None:
        pass

    def score(self):
        raise NotImplementedError("Normal score method hasn't been implemented yet")

    def get_score_by_gpt(self):
        raise NotImplementedError("GPT score method hasn't been implemented yet")
