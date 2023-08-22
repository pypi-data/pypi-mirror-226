# -*- coding: UTF-8 -*-
# @Date     : 2023/8/15 上午11:12 
# @Author   : Jiwei Qin
# @Project  : opencompass_v2 
# @Filename : icl_f1_evaluator.py
# @Software : PyCharm


from opencompass.registry import ICL_EVALUATORS
from opencompass.utils.text_postprocessors import general_postprocess

from .icl_base_evaluator import BaseEvaluator

def get_f1_score(y_true_entities: set, y_pred_entities: set) -> float:
    """
    get f1 score
    Args:
        y_true_entities: true label
        y_pred_entities: predict label

    Returns:

    """
    num_correct = len(y_true_entities & y_pred_entities)
    num_pred = len(y_pred_entities)
    num_true = len(y_true_entities)

    if num_pred == 0 or num_true == 0 or num_correct == 0:
        return 0.0
    precision = num_correct / num_pred
    recall = num_correct / num_true
    f1 = 2 * precision * recall / (precision + recall)
    return f1


@ICL_EVALUATORS.register_module()
class F1Evaluator(BaseEvaluator):
    """
    F1 evaluator.
    """

    def __init__(self) -> None:
        super().__init__()

    def score(self, predictions, references):
        if len(predictions) != len(references):
            return {
                'error': 'predictions and references have different '
                'length'
            }
        score_list = []
        print("predictions: ", predictions)
        print("references: ", references)
        # get f1 score
        for i in range(len(references)):
            if predictions[i] == "NO RESPONSE":
                score_list.append(0)
                continue

            try:
                current_reference = references[i].split("\n\n")[0].strip()
                current_prediction = predictions[i].split("\n\n")[0].strip()
                current_f1_score = get_f1_score(set(eval(current_reference)),set(eval(current_prediction)))
            except:
                current_f1_score = 0
            score_list.append(current_f1_score)

        score = sum(score_list)/len(score_list)
        return {'F1': score * 100}
