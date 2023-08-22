import json
import os

from datasets import DatasetDict, Dataset

from opencompass.datasets import BaseDataset
from opencompass.registry import LOAD_DATASET

import random
random.seed(42)
@LOAD_DATASET.register_module()
class MSRADataset(BaseDataset):

    @staticmethod
    def load(path: str):
        dataset = DatasetDict()
        content_path = os.path.join(path, 'test1.txt')
        with open(content_path, 'r') as f:
            contents = f.readlines()
        labels_path = os.path.join(path, 'testright1.txt')

        entity_types = {"nr": "人名", "ns": "地名", "nt": "机构名"}
        with open(labels_path, 'r') as f:
            labels_datas = f.readlines()
            data = []
            for num in range(len(labels_datas)):
                wt = []
                line = labels_datas[num].strip().split(" ")
                for item in line:
                    word, type = item.split("/")
                    if type in ["nt", "nr", "ns"]:
                        wt.append((word, entity_types[type]))
                    else:
                        continue
                result = {"content": contents[num].strip(), "entity_type": ",".join(list(entity_types.values())), "labels": str(wt)}
                data.append(result)
        if len(data) > 100:
            # 随机抽取100条数据
            data = random.sample(data, 100)
        else:
            data = data
        dataset['test'] = Dataset.from_list(data)
        return dataset