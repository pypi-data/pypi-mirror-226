import json
import os
import csv
from datasets import DatasetDict, Dataset

from opencompass.datasets import BaseDataset
from opencompass.registry import LOAD_DATASET

@LOAD_DATASET.register_module()
class ComAbbDataset(BaseDataset):

    @staticmethod
    def load(path: str):
        dataset = DatasetDict()
        data = []
        with open(path, 'r') as f:
            for line in f:
                line = json.loads(line)
                item = {
                    'question': line['question'],
                    'answer': line['answer'],
                }
                data.append(item)
        dataset['test'] = Dataset.from_list(data)
        return dataset