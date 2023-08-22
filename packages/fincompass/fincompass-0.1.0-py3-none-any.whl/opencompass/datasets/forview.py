import json
import os
import csv
import random
random.seed(42)

import pandas as pd
from datasets import DatasetDict, Dataset

from opencompass.datasets import BaseDataset
from opencompass.registry import LOAD_DATASET

@LOAD_DATASET.register_module()
class ForViewDataset(BaseDataset):

    @staticmethod
    def load(path: str):
        dataset = DatasetDict()
        data = []
        selections = ["A", "B", "C"]
        df = pd.read_csv(path)
        for text, cls in zip(df['text'], df['class']):
            data.append({"text": text,
                         "class": selections[int(cls)],
                         "choiceA": "负面",
                         "choiceB": "正面",
                         "choiceC": "中立"
                         })
        if len(data) > 100:
            # 随机抽取100条数据
            data = random.sample(data, 100)
        else:
            data = data
        dataset['test'] = Dataset.from_list(data)
        return dataset