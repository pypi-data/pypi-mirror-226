import random
random.seed(42)

from datasets import DatasetDict, Dataset

from opencompass.datasets import BaseDataset
from opencompass.registry import LOAD_DATASET

@LOAD_DATASET.register_module()
class NLPCCDataset(BaseDataset):

    @staticmethod
    def load(path: str):
        dataset = DatasetDict()
        with open(path, 'r') as f:
            contents = f.readlines()
            print(len(contents))
            data = []
            for num in range(0, len(contents) // 4):
                if contents[num].strip() == '':
                    continue
                question = contents[num * 4].strip().split('\t')[1]
                triple = contents[num * 4 + 1].strip().split('\t')[1]
                answer = contents[num * 4 + 2].strip().split('\t')[1]
                data.append({'question': question, 'triple': triple, 'answer': answer})
        if len(data) > 100:
            # 随机抽取100条数据
            data = random.sample(data, 100)
        else:
            data = data
        dataset['test'] = Dataset.from_list(data)
        return dataset