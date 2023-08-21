from typing import List, Union

import numpy as np
import numpy.typing as npt
from sklearn.preprocessing import OneHotEncoder

from mlc.metrics.metric import Metric
from mlc.metrics.metrics import PredClassificationMetric
from mlc.models.model import Model
from mlc.typing import NDInt, NDNumber


def default_model_prediction(
    model: Model, x: npt.NDArray[np.float_]
) -> Union[npt.NDArray[np.int_], npt.NDArray[np.float_]]:
    if model.objective in ["regression"]:
        return model.predict(x)
    if model.objective in ["binary", "classification"]:
        return model.predict_proba(x)
    raise NotImplementedError


def compute_metric(
    model: Model,
    metric: Metric,
    x: npt.NDArray[np.float_],
    y: npt.NDArray[Union[np.float_, np.int_]],
) -> npt.NDArray[np.generic]:
    return compute_metrics(model, metric, x, y)


def compute_metrics(
    model: Model,
    metrics: Union[Metric, List[Metric]],
    x: NDNumber,
    y: NDInt,
) -> npt.NDArray[np.generic]:

    if isinstance(metrics, Metric):
        return compute_metrics(model, [metrics], x, y)[0]

    y_score = default_model_prediction(model, x)

    return compute_metrics_from_scores(metrics, y, y_score)


def compute_metrics_from_scores(
    metrics: Union[Metric, List[Metric]],
    y: npt.NDArray[Union[np.float_, np.int_]],
    y_score: npt.NDArray[np.float_],
) -> npt.NDArray[np.generic]:

    if isinstance(metrics, Metric):
        return compute_metrics_from_scores([metrics], y, y_score)[0]

    y_2d = OneHotEncoder(sparse=False).fit_transform(y[:, None])

    y_pred = np.argmax(y_score, axis=1)
    out = []
    for metric in metrics:
        if isinstance(metric, PredClassificationMetric):
            out.append(metric.compute(y, y_pred))
        else:
            out.append(metric.compute(y_2d, y_score))

    return np.array(out)
