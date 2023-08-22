import json
import os
import csv
from datasets import DatasetDict, Dataset

from opencompass.datasets import BaseDataset
from opencompass.registry import LOAD_DATASET
import openpyxl


CHINA2ENG = {"场景描述": "SceneDescription", "样例题目": "Question", "理想答案": "Answer"}
CAPACITY = "文本分类"

def read_excel(path):
    """
    读取excel文件,获取数据
    Args:
        path:

    Returns:

    """
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active

    keys = [cell.value for cell in sheet[1]] # get header values

    data = []
    for row in sheet.iter_rows(min_row=2):
        values = [cell.value for cell in row]
        data.append(dict(zip(keys, values)))
    return data


@LOAD_DATASET.register_module()
class FinClsDataset(BaseDataset):

    @staticmethod
    def load(path: str):
        dataset = DatasetDict()
        excel_data = read_excel(path)
        data = []
        # 读取特定字段数据
        for item in excel_data:
            dict_new = {}
            if item['能力类型'] == CAPACITY:
                for key, value in item.items():
                    if key in CHINA2ENG.keys():
                        dict_new[CHINA2ENG[key]] = str(value).replace('\n', '，')
                data.append(dict_new)

        print(data[0])
        dataset['test'] = Dataset.from_list(data)
        return dataset