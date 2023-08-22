import json
import os
import csv
from datasets import DatasetDict, Dataset

from opencompass.datasets import BaseDataset
from opencompass.registry import LOAD_DATASET
import random
random.seed(42)

@LOAD_DATASET.register_module()
class KdConvDataset(BaseDataset):

    @staticmethod
    def load(path: str):
        dataset = DatasetDict()
        data = []
        with open(path, 'r') as f:
            for line in f:
                line = json.loads(line)
                item = {
                    'name': line['name'],
                    'kg': line['kg'],
                    'history': line['history'],
                    'response': line['response']
                }
                data.append(item)
        if len(data) > 100:
            # 随机抽取100条数据
            data = random.sample(data, 100)
        else:
            data = data
        dataset['test'] = Dataset.from_list(data)
        return dataset


# @LOAD_DATASET.register_module()
# class KdConvDataset_v2(BaseDataset):
#     @staticmethod
#     def load(**kwargs):
#         dataset = load_dataset(**kwargs)

#         def preprocess(example):
#             example['label'] = ' ABC'[int(example['label'])]
#             return example

#         dataset = dataset.map(preprocess)
#         return dataset