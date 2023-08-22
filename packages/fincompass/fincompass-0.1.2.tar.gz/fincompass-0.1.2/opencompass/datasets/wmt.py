import json
import os
import csv
from datasets import DatasetDict, Dataset

from opencompass.datasets import BaseDataset
from opencompass.registry import LOAD_DATASET
import random
random.seed(42)

@LOAD_DATASET.register_module()
class WMTDataset(BaseDataset):

    @staticmethod
    def load(path: str):
        dataset = DatasetDict()
        data = []
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for num in range(1, len(lines)):
                if lines[num].strip() == '':
                    continue
                line = lines[num].strip().split(',')
                data.append({'zh_text': line[0], 'en_text': line[1]})
        if len(data) > 100:
            # 随机抽取100条数据
            data = random.sample(data, 100)
        else:
            data = data
        dataset['test'] = Dataset.from_list(data)
        return dataset