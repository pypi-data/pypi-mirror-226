import json
import os

from datasets import DatasetDict, Dataset

from opencompass.datasets import BaseDataset
from opencompass.registry import LOAD_DATASET

import random
random.seed(42)

@LOAD_DATASET.register_module()
class DuIEDataset(BaseDataset):

    @staticmethod
    def load(path: str):
        dataset = DatasetDict()
        relations_path = os.path.join(path, 'duie_schema.json')
        with open(relations_path, 'r') as f:
            relations = []
            subject_types = []
            object_types = []
            for line in f:
                line = json.loads(line)
                relations.append(line['predicate'])
                subject_types.append(line['subject_type'])
                object_types.append(line['object_type']['@value'])
        # remove duplicate elements
        relations = list(set(relations))
        subject_types = list(set(subject_types))
        object_types = list(set(object_types))
        data = []
        datas_path = os.path.join(path, 'duie_dev.json')
        with open(datas_path, 'r') as f:
            for line in f:
                line = json.loads(line)
                content = line['text']
                # extract word1, word2, relation
                wwr = []
                for item in line['spo_list']:
                    relation = item['predicate']
                    word1 = item['subject']
                    word2 = item['object']['@value']
                    wwr.append((word1, word2, relation))
                result = {'content': content, "subject_types": subject_types, "object_types": object_types,
                          "relations": relations, 'wwr': wwr}
                data.append(result)
        if len(data) > 100:
            # 随机抽取100条数据
            data = random.sample(data, 100)
        else:
            data = data
        dataset['test'] = Dataset.from_list(data)
        return dataset