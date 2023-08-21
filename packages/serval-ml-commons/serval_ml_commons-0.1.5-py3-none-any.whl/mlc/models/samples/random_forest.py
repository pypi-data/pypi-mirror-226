from math import sqrt
from typing import Any, List, Optional, Tuple, Type, Dict
from joblib import parallel_backend
import optuna
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from mlc.models.model import Model
from mlc.models.sk_models import SkModel
from mlc.transformers.tab_scaler import TabScaler
from mlc.typing import NDFloat, NDNumber


class Rf(SkModel):
    def __init__(
        self,
        name: str = "random_forest",
        objective: str = "classification",
        x_metadata: Optional[pd.DataFrame] = None,
        scaler: Optional[TabScaler] = None,
        n_jobs: int = -1,
        **kwargs: Any,
    ):
        super().__init__(
            name=name,
            objective=objective,
            x_metadata=x_metadata,
            scaler=scaler,
            n_jobs=n_jobs,
            **kwargs,
        )
        self.x_metadata = x_metadata
        self.scaler = scaler

        if self.scaler is not None:
            n_scaler = TabScaler(num_scaler="min_max", one_hot_encode=True)
            n_scaler.fit_scaler_data(self.scaler.get_scaler_data())
            self.scaler = n_scaler

        rf_parameters = {
            "class_weight": "balanced",
            **kwargs,
        }

        # Filter out parameters that are not in the model
        rf_parameters = {
            e: kwargs[e]
            for e in rf_parameters
            if e in RandomForestClassifier().get_params()
        }

        rf_parameters = {
            **rf_parameters,
            "n_jobs": n_jobs,
            "verbose": 1,
        }

        self.model = RandomForestClassifier(
            **rf_parameters,
        )

    @staticmethod
    def define_trial_parameters(
        trial: optuna.Trial, trial_params: Dict[str, Any]
    ) -> Dict[str, Any]:

        len_x = len(trial_params["x_metadata"])
        max_features = 1.0
        if len_x > 200:
            max_features = sqrt(len_x) / len_x

        params = {
            "n_estimators": trial.suggest_int("n_estimators", 10, 1000),
            "max_depth": trial.suggest_int("max_depth", 4, 50),
            "min_samples_split": trial.suggest_int(
                "min_samples_split", 2, 150
            ),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 60),
            "max_features": trial.suggest_float(
                "max_features", 0, max_features
            ),
        }

        return params

    @staticmethod
    def get_default_params(trial_params: Dict[str, Any]) -> Dict[str, Any]:
        params = {
            "n_estimators": 100,
            "max_depth": 50,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "max_features": (
                sqrt(trial_params["n_features"]) / trial_params["n_features"]
            ),
        }

        return params

    def predict(self, x: NDFloat) -> NDNumber:
        """
        Returns the regression value or the concrete classes of binary /
        multi-class-classification tasks.
        (Save predictions to self.predictions)

        :param x: test data
        :return: predicted values / classes of test data (Shape N x 1)
        """
        if self.scaler is not None:
            x = self.scaler.transform(x)
        return super().predict(x)

    def predict_proba(self, x: NDFloat) -> NDFloat:
        """
        Only implemented for binary / multi-class-classification tasks.
        Returns the probability distribution over the classes C.
        (Save probabilities to self.prediction_probabilities)

        :param x: test data
        :return: probabilities for the classes (Shape N x C)
        """
        if self.scaler is not None:
            x = self.scaler.transform(x)
        return super().predict_proba(x)

    def fit(
        self,
        x: NDFloat,
        y: NDNumber,
        x_val: Optional[NDFloat] = None,
        y_val: Optional[NDNumber] = None,
    ) -> None:
        x = self.scaler.transform(x)
        if x_val is not None:
            x_val = self.scaler.transform(x_val)

        super().fit(
            x,
            y,
            x_val,
            y_val,
        )

    def set_experiment(self, experiment: Any) -> None:
        pass

    @staticmethod
    def load_class(self, path: str, **kwargs) -> None:
        model = Rf(**kwargs)
        model.load(path)
        return model


models: List[Tuple[str, Type[Model]]] = [("random_forest", Rf)]
