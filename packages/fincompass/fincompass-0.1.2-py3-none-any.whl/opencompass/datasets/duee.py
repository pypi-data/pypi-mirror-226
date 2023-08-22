import json
import os

from datasets import DatasetDict, Dataset

from opencompass.datasets import BaseDataset
from opencompass.registry import LOAD_DATASET

import random
random.seed(42)


def get_schema(path: str):
    """
    get schema for duee, mainly event_type and role_list
    Args:
        path: path of duee
    Returns: event_type and role_list

    """
    schema_path = os.path.join(path, 'duee_event_schema.json')
    # save event_type and role_list
    event_type_and_role_list = {}
    with open(schema_path, 'r') as f:
        for line in f:
            schema = json.loads(line)
            # extract role_list
            role_list = []
            for role in schema['role_list']:
                role_list.append(role['role'])
            # extract event_type
            if "/" not in schema['event_type']:
                event_type_and_role_list[schema['event_type']] = role_list
            else:
                before, after = schema['event_type'].split('-')
                if "/" in before:
                    before_list = before.split('/')
                else:
                    before_list = [before]
                if "/" in after:
                    after_list = after.split('/')
                else:
                    after_list = [after]
                # contact before and after
                for b in before_list:
                    for a in after_list:
                        event_type = b + '-' + a
                        event_type_and_role_list[event_type] = role_list
    return event_type_and_role_list

@LOAD_DATASET.register_module()
class DuEEDataset(BaseDataset):

    @staticmethod
    def load(path: str):
        dataset = DatasetDict()
        # get event_type and role_list
        event_type_and_role_list = get_schema(path)
        # get event_type and role_list
        event_types = list(event_type_and_role_list.keys())
        role_lists = list(event_type_and_role_list.values())
        template = "事件类型 ‘{event_type}’ 对应的论元角色列表是 {arguments} ;"
        types_and_roles = []
        for i in range(len(event_types)):
            # 实现代码：将事件类型和事件角色列表拼接成字符串，存储到字典中
            types_and_roles.append(template.format(event_type=event_types[i], arguments=role_lists[i]))
        # get data
        data = []
        datas_path = os.path.join(path, 'duee_dev.json')
        with open(datas_path, 'r') as f:
            for line in f:
                line = json.loads(line)
                content = line['text']
                # extract event_type and arguments
                arguments = []
                for item in line['event_list']:
                    event_type = item['event_type']
                    for role in item['arguments']:
                        event_role = role['role']
                        event_argument = role['argument']
                        arguments.append({'role': event_role, 'argument': event_argument})
                result = {'content': content, "types_and_roles": "".join(types_and_roles),
                          "event_type_and_arguments": {"event_type": event_type, "arguments": arguments}}
                data.append(result)
        if len(data) > 100:
            # 随机抽取100条数据
            data = random.sample(data, 100)
        else:
            data = data
        dataset['test'] = Dataset.from_list(data)
        return dataset