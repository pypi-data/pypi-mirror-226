import json
import os
import csv
from datasets import DatasetDict, Dataset

from opencompass.datasets import BaseDataset
from opencompass.registry import LOAD_DATASET
import random
random.seed(42)


@LOAD_DATASET.register_module()
class CCPMDataset(BaseDataset):

    @staticmethod
    def load(path: str):
        dataset = DatasetDict()
        data = []
        selections = ['A', 'B', 'C', 'D']
        with open(path, 'r') as f:
            for line in f:
                line = json.loads(line)
                item = {
                    'translation': line['translation'],
                    'choiceA': line['choices'][0],
                    'choiceB': line['choices'][1],
                    'choiceC': line['choices'][2],
                    'choiceD': line['choices'][3],
                    'answer': selections[int(line['answer'])]
                }
                data.append(item)
        if len(data) > 100:
            # 随机抽取100条数据
            data = random.sample(data, 100)
        else:
            data = data
        dataset['test'] = Dataset.from_list(data)
        return dataset