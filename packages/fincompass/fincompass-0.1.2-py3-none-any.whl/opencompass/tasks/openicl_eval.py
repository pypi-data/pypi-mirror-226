import argparse
import os.path as osp
import time
from typing import Optional

import mmengine
from mmengine.config import Config, ConfigDict
from mmengine.utils import mkdir_or_exist

from opencompass.registry import (ICL_EVALUATORS, MODELS, TASKS,
                                  TEXT_POSTPROCESSORS)
from opencompass.tasks.base import BaseTask
from opencompass.utils import (build_dataset_from_cfg, get_infer_output_path,
                               get_logger, task_abbr_from_cfg)


@TASKS.register_module(force=(__name__ == '__main__'))  # A hack for script run
class OpenICLEvalTask(BaseTask):
    """OpenICL Evaluation Task.

    This task is used to evaluate the metric between predictions and
    references.
    """

    name_prefix = 'OpenICLEval'
    log_subdir = 'logs/eval'
    output_subdir = 'results'

    def __init__(self, cfg: ConfigDict):
        super().__init__(cfg)
        self.num_gpus = 0
        self.logger = get_logger()

    def get_command(self, cfg_path, template):
        script_path = __file__
        command = f'python3 {script_path} {cfg_path}'
        return template.format(task_cmd=command)

    def run(self):
        for model_cfg, dataset_cfgs in zip(self.model_cfgs, self.dataset_cfgs):
            for dataset_cfg in dataset_cfgs:
                self.model_cfg = model_cfg
                self.dataset_cfg = dataset_cfg

                # Load Dataset
                self.eval_cfg = self.dataset_cfg.get('eval_cfg')
                self.output_column = dataset_cfg['reader_cfg']['output_column']

                out_path = get_infer_output_path(
                    self.model_cfg, self.dataset_cfg,
                    osp.join(self.work_dir, 'results'))
                if osp.exists(out_path):
                    continue
                self._score()

    def _score(self):
        test_set = build_dataset_from_cfg(self.dataset_cfg).test
        # Postprocess dataset if necessary
        if 'dataset_postprocessor' in self.eval_cfg:
            TEXT_POSTPROCESSORS.get(
                self.eval_cfg['dataset_postprocessor']['type'])

            def postprocess(sample):
                s = sample[self.output_column]
                proc = TEXT_POSTPROCESSORS.get(
                    self.eval_cfg['dataset_postprocessor']['type'])
                sample[self.output_column] = proc(s)
                return sample

            test_set = test_set.map(postprocess)

        # Load predictions
        filename = get_infer_output_path(
            self.model_cfg, self.dataset_cfg,
            osp.join(self.work_dir, 'predictions'))
        # in case the prediction is partial
        root, ext = osp.splitext(filename)
        partial_filename = root + '_0' + ext

        if not osp.exists(osp.realpath(filename)) and not osp.exists(
                osp.realpath(partial_filename)):
            result = {'error': 'No predictions found.'}
        else:
            if osp.exists(osp.realpath(filename)):
                preds = mmengine.load(filename)
                pred_strs = [
                    preds[str(i)]['prediction'] for i in range(len(preds))
                ]
                # TODO: get "origin_prompt" from json file
                prompt_strs = [
                    preds[str(i)]['origin_prompt'] for i in range(len(preds))
                ]

            else:
                filename = partial_filename
                pred_strs = []
                prompt_strs = []
                i = 1
                while osp.exists(osp.realpath(filename)):
                    preds = mmengine.load(filename)
                    filename = root + f'_{i}' + ext
                    i += 1
                    pred_strs += [
                        preds[str(i)]['prediction'] for i in range(len(preds))
                    ]
                    prompt_strs += [
                        preds[str(i)]['origin_prompt'] for i in range(len(preds))
                    ]

            if ('pred_role' in self.eval_cfg
                    and 'meta_template' in self.model_cfg
                    and not MODELS.get(self.model_cfg['type']).is_api):
                # Create a prompt template for role config parsing
                from opencompass.models.base import LMTemplateParser
                parser = LMTemplateParser(self.model_cfg['meta_template'])
                role = parser.roles[self.eval_cfg['pred_role']]
                pred_strs = [
                    self._extract_role_pred(pred, role.get('begin', None),
                                            role.get('end', None))
                    for pred in pred_strs
                ]

            # Postprocess predictions if necessary
            if 'pred_postprocessor' in self.eval_cfg:
                proc = TEXT_POSTPROCESSORS.get(
                    self.eval_cfg['pred_postprocessor']['type'])
                pred_strs = [proc(s) for s in pred_strs]

            # get evaluate method
            try:
                eval_method = self.eval_cfg['method']
            except:
                eval_method = None

            # human evaluation
            if eval_method == 'human':
                icl_evaluator = ICL_EVALUATORS.build(self.eval_cfg['evaluator'])
                result = icl_evaluator.score(
                    predictions=pred_strs, references=test_set[self.output_column], prompts=prompt_strs)
            # gpt evaluation
            elif eval_method == 'gpt':
                icl_evaluator = ICL_EVALUATORS.build(self.eval_cfg['evaluator'])
                result = icl_evaluator.score(
                    predictions=pred_strs, references=test_set[self.output_column], prompts=prompt_strs)
            # logp evaluation
            else:
                icl_evaluator = ICL_EVALUATORS.build(self.eval_cfg['evaluator'])
                result = icl_evaluator.score(
                    predictions=pred_strs, references=test_set[self.output_column])


        if 'error' in result:
            self.logger.error(
                f'Task {task_abbr_from_cfg(self.cfg)}: {result["error"]}')
            return

        # Save result
        out_path = get_infer_output_path(self.model_cfg, self.dataset_cfg,
                                         osp.join(self.work_dir, 'results'))
        mkdir_or_exist(osp.split(out_path)[0])
        mmengine.dump(result, out_path)

    def _extract_role_pred(self, s: str, begin_str: Optional[str],
                           end_str: Optional[str]) -> str:
        """Extract the role prediction from the full prediction string. The
        role prediction may be the substring between the begin and end string.

        Args:
            s (str): Full prediction string.
            begin_str (str): The beginning string of the role
            end_str (str): The ending string of the role.

        Returns:
            str: The extracted role prediction.
        """
        start = 0
        end = len(s)

        if begin_str:
            begin_idx = s.find(begin_str)
            if begin_idx != -1:
                start = begin_idx + len(begin_str)

        if end_str:
            # TODO: Support calling tokenizer for the accurate eos token
            # and avoid such hardcode
            end_idx = s.find(end_str[:1], start)
            if end_idx != -1:
                end = end_idx

        return s[start:end]


def parse_args():
    parser = argparse.ArgumentParser(description='Score Calculator')
    parser.add_argument('config', help='Config file path')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    cfg = Config.fromfile(args.config)
    start_time = time.time()
    inferencer = OpenICLEvalTask(cfg)
    inferencer.run()
    end_time = time.time()
    get_logger().info(f'time elapsed: {end_time - start_time:.2f}s')
