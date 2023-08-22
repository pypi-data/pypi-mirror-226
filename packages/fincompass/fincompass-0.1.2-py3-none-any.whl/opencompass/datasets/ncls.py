from datasets import DatasetDict, Dataset
from bs4 import BeautifulSoup
from opencompass.datasets import BaseDataset
from opencompass.registry import LOAD_DATASET
import random
random.seed(42)

@LOAD_DATASET.register_module()
class NCLSDataset(BaseDataset):

    @staticmethod
    def load(path: str):
        dataset = DatasetDict()
        with open(path, 'r') as f:
            # parse xml
            contents = f.read()
            soup = BeautifulSoup(contents, 'html.parser')
            docs = soup.find_all('doc')
            # save artical and ref
            data = []
            for doc in docs:
                en_refs = []
                zh_refs = []
                # 提取Article的内容
                article = doc.find("article").text.strip()

                # 提取EN-REF1的内容
                en_ref1 = doc.find("en-ref1").text.strip()
                en_refs.append(en_ref1)

                # 提取ZH-REF1的内容
                zh_ref1 = doc.find("zh-ref1-human-corrected").text.strip()
                zh_refs.append(zh_ref1)

                # 提取EN-REF2的内容
                en_ref2 = doc.find("en-ref2")
                if en_ref2 is not None:
                    en_ref2 = en_ref2.text.strip()
                    en_refs.append(en_ref2)

                # 提取ZH-REF2的内容
                zh_ref2 = doc.find("zh-ref2-human-corrected")
                if zh_ref2 is not None:
                    zh_ref2 = zh_ref2.text.strip()
                    zh_refs.append(zh_ref2)

                # 提取EN-REF3的内容
                en_ref3 = doc.find("en-ref3")
                if en_ref3 is not None:
                    en_ref3 = en_ref3.text.strip()
                    en_refs.append(en_ref3)

                # 提取ZH-REF3的内容
                zh_ref3 = doc.find("zh-ref3-human-corrected")
                if zh_ref3 is not None:
                    zh_ref3 = zh_ref3.text.strip()
                    zh_refs.append(zh_ref3)
                data.append({
                    "article": article,
                    "en_refs": en_refs,
                    "zh_refs": zh_refs
                })
        if len(data) > 100:
            # 随机抽取100条数据
            data = random.sample(data, 100)
        else:
            data = data
        dataset['test'] = Dataset.from_list(data)
        return dataset
