**Welcome to FinCompass**!

**FinCompass**旨在面向金融NLPer，更便捷地对金融领域NLP模型的性能进行公平全面的评估。FinCompass在具备丰富的算法和功能的基础上，支持灵活的文件配置式评测，使得NLPer更高效地新增评测数据与模型。FinCompass 将不断致力于为NLPer提供准确、可靠的评估工具，以更好地理解和提升金融领域的NLP模型。

## 最新进展

- **\[2023.08.18\]** 新增面向模型训练者的框架部署流程，针对新增评测集和模型，只需修改`run.json`配置文件。
- **\[~2023.08.16\]** 基于官方框架新增10个中文评测数据集、11类金融领域评测任务以及6个模型评测接口；评测功能上，支持机器评估与人工评估两类评估方式；新增F1、GPT等评测基准。

## 评测流程

### 1. 运行环境配置
- python环境


```
$ conda create --name {deepai} python=3.10
```

```
$ conda activate {deepai}
```

- 安装依赖

```
$ unzip opencompass.zip
$ cd opencompass
$ pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 
```

- 安装opencompass库

```
$ pip install -e .
```

- 检测环境是否配置成功

```
$ python run.py configs/eval_demo.py -w outputs/demo --debug
```
如果一切正常，屏幕上会出现 “Starting inference process”

![debug](./imgs/debug.png)

### 2. 评测流程配置

如果运行环境配置完成，用户便可配置项目中的`run.json`文件，指定相关参数，即可对新增的数据集和模型进行评测。后续评测过程只需更改配置参数即可。

1. **修改`run.json`配置文件**

```json
{
  "dataset_name": "nlpcc",
  "dataset_path": "data/test/nlpcc_test.json",
  "prompt_key": ["question", "triple"],
  "answer_key": "answer",
  "prompt_template": "请根据知识库中的三元组知识回答问题,三元组知识为: {triple}\n请问答问题: {question}\n答案: ",
  "evaluator": "ROUGE",
  "model_name": "minimax",
  "generateURL": "http://ip:port/api/v1/eval/minimax",
  "request_data": {
    "data":{
      "question": ""
    },
    "times": 0
  },
  "recieve_data": {
    "data":{
      "prediction": ""
    }
  },
  "max_seq_len": 2048,
  "max_out_len": 512,
  "sample_size": 2
}
```

2. **执行评测指定**

```shell
python run.py configs/eval_base.py -w outputs/base
```

> Todo: 后面使用.sh文件

**json配置字段说明：**

- `dataset_name`：str，数据集名称，用于与其他数据集区分。
- `dataset_path`：str，数据集文件路径。

- `prompt_key`：list，构造prompt需要的字段。
- `answer_key`：str，标准答案字段。
- `prompt_template`：str，prompt样例，`{字段}`来源于`prompt_key`。
- `evaluator`：str，评估指标，目前可选项：`EM`、`ROUGE`。不支持自定义指标。
- `model_name`：str，模型名称，用于与其他模型区分。
- `generateURL`：str，模型接口链接。
- `request_data`：dict，请求字段设置。必须包含`data:{question:""}`字段，其他可自定义，比如模型的初始化参数。
- `recieve_data`：dict，接收字段设置。此处无需修改，用于告知用户返回字段必须包含`data:{prediction:""}`字段。
- `max_seq_len`：int，模型最大输入指定。也可在`request_data`字段中根据需求设定。
- `max_out_len`：int，模型最大输入指定。也可在`request_data`字段中根据需求设定。
- `sample_size`：int，指定个评估数据的样例个数，用于debug，选择方式为随机采样。

**!注意!**

当前版本，评测集必须为json格式数据，需要明确指定`prompt_key`字段和`answer_key`字段，且`prompt_key`需要在`prompt_template`字符串中出现。

## 性能榜单

**通用能力**

![image-20230818192047059](./imgs/bangdan.png)

**金融能力**

<img src="./imgs/fin.png" alt="image-20230818192620845" style="zoom: 33%;" />

## 数据集支持

<img src="./imgs/dataset.png" alt="image-20230818192317348" style="zoom: 33%;" />

## 模型支持

- 文心一言 ernie-bot
- 文心一言 ernie-bot-turbo（10B）
- gpt-3.5-turbo
- 面壁cpmbee-api
- minimax-api
- ChatGLM-6B
- ChatGLM2-6B
- llama-7b
- Baichuan-7B
- internlm_7b
- CPMBEE-10B
- ...