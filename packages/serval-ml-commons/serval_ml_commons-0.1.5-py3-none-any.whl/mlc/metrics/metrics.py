import numpy as np
import numpy.typing as npt
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    mean_squared_error,
    roc_auc_score,
)

from mlc.metrics.metric import Metric


def transaction_cost(
    y: npt.NDArray[np.int_], y_s: npt.NDArray[np.int_]
) -> float:
    (tn, fp, fn, tp) = confusion_matrix(y, y_s)
    return (((tp + fp) * 5.0) + (fn * 60.0) + (tn * 0)) / 60


str2pred_classification_metric = {
    "f1": f1_score,
    "mcc": matthews_corrcoef,
    "error_rate": lambda y, y_s: 1 - accuracy_score(y, y_s),
    "class_error": lambda y, y_s: 1 - (y == y_s).astype(int),
    "accuracy": lambda y, y_s: accuracy_score(y, y_s),
    "confusion_matrix": lambda y, y_s: confusion_matrix(y, y_s),
    "balanced_accuracy": lambda y, y_s: balanced_accuracy_score(y, y_s),
    "transaction_cost": transaction_cost,
}
str2proba_classification_metric = {
    "auc": lambda y, y_s: roc_auc_score(
        y,
        y_s,
    ),
    "proba_error": lambda y, y_s: 1 - y_s[np.arange(len(y)), y],
    "y_scores": lambda y, y_s: y_s,
}

str2regression_metric = {
    "rmse": lambda y, y_s: mean_squared_error(y, y_s, squared=True)
}


class RecordedMetric(object):
    def __init__(self):
        self.reset()

    def mean(self):
        return np.mean(self.values)

    def std(self):
        return np.std(self.values)

    def reset(self):
        self.values = []

    def last(self):
        return self.values[-1]


class PredClassificationMetric(Metric, RecordedMetric):
    def __init__(self, metric_name: str):
        self.metric_name = metric_name
        self.values = []

    def compute(
        self, y_true: npt.NDArray[np.generic], y_score: npt.NDArray[np.generic]
    ) -> npt.NDArray[np.generic]:
        val = str2pred_classification_metric[self.metric_name](y_true, y_score)

        self.values.append(val)
        return val


class ProbaClassificationMetric(Metric, RecordedMetric):
    def __init__(self, metric_name: str):
        self.metric_name = metric_name
        self.values = []

    def compute(
        self, y_true: npt.NDArray[np.generic], y_score: npt.NDArray[np.generic]
    ) -> npt.NDArray[np.generic]:

        val = str2proba_classification_metric[self.metric_name](
            y_true, y_score
        )

        self.values.append(val)
        return val


class RegressionMetric(Metric, RecordedMetric):
    def __init__(self, metric_name: str):
        self.metric_name = metric_name
        self.values = []

    def compute(
        self, y_true: npt.NDArray[np.generic], y_score: npt.NDArray[np.generic]
    ) -> npt.NDArray[np.generic]:
        val = str2regression_metric[self.metric_name](y_true, y_score)

        self.values.append(val)
        return val
