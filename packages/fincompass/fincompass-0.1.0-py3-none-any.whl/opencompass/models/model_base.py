# -*- coding: UTF-8 -*-
# @Date     : 2023/8/18 上午11:18 
# @Author   : Jiwei Qin
# @Project  : opencompass_v2 
# @Filename : model_base.py
# @Software : PyCharm


from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Union

from opencompass.registry import MODELS
from opencompass.utils.prompt import PromptList

from .base_api import BaseAPIModel
import json



PromptType = Union[PromptList, str]

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry



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

@MODELS.register_module()
class ModelBaseAPI(BaseAPIModel):
    """Model wrapper around BaseModel's models.

    Args:
        path (str): The name of OpenAI's model.
        max_seq_len (int): The maximum allowed sequence length of a model.
            Note that the length of prompt + generated tokens shall not exceed
            this value. Defaults to 2048.
        query_per_second (int): The maximum queries allowed per second
            between two consecutive calls of the API. Defaults to 1.
        retry (int): Number of retires if the API call fails. Defaults to 2.
        key (str): OpenAI key. In particular, when it is set to "ENV", the key
            will be fetched from the environment variable $OPENAI_API_KEY, as
            how openai defaults to be. Defaults to 'ENV'
        meta_template (Dict, optional): The model's meta prompt
            template if needed, in case the requirement of injecting or
            wrapping of any meta instructions.
        openai_api_base (str): The base url of OpenAI's API. Defaults to
            'https://api.openai.com/v1'.
    """

    is_api: bool = True

    def __init__(self,
                 path: str,
                 max_seq_len: int = 2048,
                 query_per_second: int = 1,
                 retry: int = 3,
                 key: str = 'ENV',
                 meta_template: Optional[Dict] = None,
                 data_json: json = None,
                 generateURL: str = None,
                 tokenizeURL: str = None,
                 ):
                 # generateURL: str = 'https://deepqopenai.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-03-15-preview',
                 # tokenizeURL: str = 'http://192.168.11.37:8015/cpmbee/tokenizer'):
        super().__init__(path=path,
                         max_seq_len=max_seq_len,
                         meta_template=meta_template,
                         query_per_second=query_per_second,
                         retry=retry)
        self.generateURL = generateURL
        # self.tokenizeURL = tokenizeURL
        self.data_json = data_json
        self.max_seq_len = max_seq_len
        self.key = key

    def get_response(self, input_data):
        self.data_json["data"]['question'] = input_data
        print(self.data_json)
        if self.key != "ENV":
            headers = {"api-key": self.key}
        else:
            headers = {"Content-Type": "application/json"}
        try:
            current_response = post_request(url=self.generateURL, data=json.dumps(self.data_json), headers=headers, timeout=10)
            content = current_response.json()["data"]["prediction"]
            return content
        except requests.exceptions.RequestException as e:
            print("get_response error: ", end="")
            print(e)
            return "NO RESPONSE"

    def generate(
            self,
            inputs: List[str or PromptList],
            max_out_len: int = 512,
            temperature: float = 0.01,
    ) -> List[str]:
        """Generate results given a list of inputs.

        Args:
            inputs (List[str or PromptList]): A list of strings or PromptDicts.
                The PromptDict should be organized in OpenCompass'
                API format.
            max_out_len (int): The maximum length of the output.
            temperature (float): What sampling temperature to use,
                between 0 and 2. Higher values like 0.8 will make the output
                more random, while lower values like 0.2 will make it more
                focused and deterministic. Defaults to 0.7.

        Returns:
            List[str]: A list of generated strings.
        """
        with ThreadPoolExecutor() as executor:
            results = list(
                executor.map(self._generate, inputs,
                             [max_out_len] * len(inputs),
                             [temperature] * len(inputs)))
        return results

    def _generate(self, input: str or PromptList, max_out_len: int,
                  temperature: float) -> str:
        """Generate results given a list of inputs.

        Args:
            inputs (str or PromptList): A string or PromptDict.
                The PromptDict should be organized in OpenCompass'
                API format.
            max_out_len (int): The maximum length of the output.
            temperature (float): What sampling temperature to use,
                between 0 and 2. Higher values like 0.8 will make the output
                more random, while lower values like 0.2 will make it more
                focused and deterministic.

        Returns:
            str: The generated string.
        """
        assert isinstance(input, (str, PromptList))

        # max num token for gpt-3.5-turbo is 4097
        max_out_len = min(max_out_len, 4000 - self.get_token_len(str(input)))

        messages = input

        max_num_retries = 0
        while max_num_retries < self.retry:
            self.wait()
            response = self.get_response(messages)
            if response == "NO RESPONSE" and max_num_retries < self.retry:
                max_num_retries += 1
            else:
                return response
        return response
        # raise RuntimeError(
        #     f"API call failed after {self.retry} retries. Please check your "
        #     f"internet connection")

    def get_token_len(self, prompt: str) -> int:
        """Get lengths of the tokenized string. Only English and Chinese
        characters are counted for now. Users are encouraged to override this
        method if more accurate length is needed.

        Args:
            prompt (str): Input string.

        Returns:
            int: Length of the input tokens
        """
        return len(prompt)