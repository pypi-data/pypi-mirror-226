import json
import os

from datasets import DatasetDict, Dataset

from opencompass.datasets import BaseDataset
from opencompass.registry import LOAD_DATASET
import random
random.seed(42)

@LOAD_DATASET.register_module()
class BaseLoaderDataset(BaseDataset):

    @staticmethod
    def load(path: str, sample_size: int):
        dataset = DatasetDict()
        with open(path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        data = random.sample(data, min(sample_size, len(data)))
        dataset['test'] = Dataset.from_list(data)
        print(dataset['test'])
        return dataset