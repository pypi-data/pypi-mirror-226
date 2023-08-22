import json
import os
import csv
from datasets import DatasetDict, Dataset

from opencompass.datasets import BaseDataset
from opencompass.registry import LOAD_DATASET
import random
random.seed(42)

@LOAD_DATASET.register_module()
class DoubanDataset(BaseDataset):

    @staticmethod
    def load(path: str):
        dataset = DatasetDict()
        data = []
        with open(path, 'r') as f:
            for line in f:
                line = json.loads(line)
                item = {
                    'history': "".join((", ".join(line['history'])).split(" ")),
                    'response': line['response'],
                }
                data.append(item)
        if len(data) > 100:
            # 随机抽取100条数据
            data = random.sample(data, 100)
        else:
            data = data
        dataset['test'] = Dataset.from_list(data)
        return dataset