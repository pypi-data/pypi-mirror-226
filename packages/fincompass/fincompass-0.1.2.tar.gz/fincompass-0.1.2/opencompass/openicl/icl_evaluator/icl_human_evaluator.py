import json
from typing import List
import numpy as np

from opencompass.registry import ICL_EVALUATORS
from opencompass.openicl.icl_evaluator import BaseEvaluator

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

HUMAN_EVAL_URL = "http://192.168.148.64:5001/api/v1/eval/human"

def requests_retry_session(retries=5, backoff_factor=1, session=None):
    session = session or requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get_request(url, **kwargs):
    with requests_retry_session() as session:
        r = session.get(url, **kwargs)
    r.raise_for_status()
    return r


def post_request(url, **kwargs):
    with requests_retry_session() as session:
        r = session.post(url, **kwargs)
    r.raise_for_status()
    return r


class HUMANRequest:
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers

    @staticmethod
    def create_request_body(prediction: str, reference: str, prompt: str) -> dict:
        """Create an API request body for a given text.
        params:
            question: question text
            answer: answer text
        Returns:
            dict: request body
        """
        return {
            "prediction": prediction,
            "reference": reference,
            "prompt": prompt
        }

    def get_human_score(self, prediction: str, reference: str, prompt: str) -> float:
        """
        Access the manual evaluation interface and return the manual evaluation score

        Args:
            prediction:  prediction text
            reference:  reference text
            prompt:  prompt text

        Returns:
            float: human evaluation score

        """
        data = self.create_request_body(prediction, reference, prompt)
        try:
            current_response = requests.post(url=self.url, data=json.dumps(data), headers=self.headers, timeout=300)
            score = float(current_response.json()["data"]["human_score"])
            return score
        except requests.exceptions.RequestException as e:
            print("get_response error: ", end="")
            print(e)
            return float(-1)


@ICL_EVALUATORS.register_module()
class APIEvaluator(BaseEvaluator):
    """Human evaluation for ICL.
    """  # noqa

    def __init__(self) -> None:
        super().__init__()
        self.client = HUMANRequest(url=HUMAN_EVAL_URL, headers={'Content-Type': 'application/json'})


    def score(self, predictions: List, references: List, prompts: list) -> dict:
        """get evaluation score by gpt.

        Args:
            predictions (List): List of predictions for each
                sample.
            references (List): List of target labels for each sample.
            prompts (list): List of prompts for each sample.

        Returns:
            dict: gpt evaluation scores.
        """
        if len(predictions) != len(references):
            return {
                'error': 'predictions and references have different length.'
            }
        if len(prompts) != len(references):
            return {
                'error': 'prompts and references have different length.'
            }
        # get gpt evaluation score for each sample
        for i in range(len(references)):
            predictions[i] = self.client.get_human_score(predictions[i], references[i], prompts[i])
        # calculate average human evaluation score
        human_score = np.mean(predictions)
        return dict(human_score=human_score * 100)
