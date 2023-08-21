from typing import Any, Dict, List, Optional, Tuple, Type, Union

import numpy as np
import optuna
import pandas as pd
import torch
import torch.nn as nn
from mlc.dataloaders.fast_dataloader import FastTensorDataLoader

from mlc.models.model import Model
from mlc.models.torch_models import BaseModelTorch
from mlc.transformers.tab_scaler import TabScaler
from mlc.utils import to_torch_number

from .deepfm_lib.inputs import DenseFeat, SparseFeat
from .deepfm_lib.models.deepfm import DeepFM as DeepFMModel

"""
    DeepFM: A Factorization-Machine based Neural Network for CTR Prediction
     (https://www.ijcai.org/proceedings/2017/0239.pdf)

    Code adapted from: https://github.com/shenweichen/DeepCTR-Torch
"""


class BalancedBCELoss(torch.nn.BCEWithLogitsLoss):
    def __init__(self, y: torch.Tensor, **args: Any):
        self.weights = None
        y = np.array(y)
        y_class, y_occ = np.unique(y, return_counts=True)
        self.weights = dict(zip(y_class, y_occ / len(y)))
        super(BalancedBCELoss, self).__init__(**args)

    def forward(
        self, input: torch.Tensor, target: torch.Tensor, reduction: Any = None
    ) -> torch.Tensor:

        if self.weights is None:
            return super(BalancedBCELoss, self).forward(input, target)

        negative_inputs_mask = target == 0
        positive_inputs_mask = target == 1

        positive_inputs, positive_targets = (
            input[positive_inputs_mask],
            input[positive_inputs_mask],
        )
        positive_loss = super(BalancedBCELoss, self).forward(
            positive_inputs, positive_targets
        )
        negative_inputs, negative_targets = (
            input[negative_inputs_mask],
            input[negative_inputs_mask],
        )
        negative_loss = super(BalancedBCELoss, self).forward(
            negative_inputs, negative_targets
        )

        return positive_loss / self.weights.get(
            1
        ) + negative_loss / self.weights.get(0)


def get_fixlen_feature_columns(
    cat_idx: List[int],
    cat_dims: List[int],
    num_features: int,
    num_dense_features: int = None,
) -> List[Union[DenseFeat, SparseFeat]]:
    if cat_idx:
        if (
            num_dense_features
            and num_dense_features > 0
            and num_dense_features + len(cat_idx) < num_features
        ):
            # i.e. we have one hot encoded the features, using binary sparse
            dense_features = list(
                range(
                    num_features - num_dense_features,
                    num_features,
                )
            )
            binary_featues = list(range(0, num_dense_features))
            fixlen_feature_columns = [
                SparseFeat(str(feat), 2) for feat in binary_featues
            ] + [
                DenseFeat(
                    str(feat),
                    1,
                )
                for feat in dense_features
            ]
        else:
            dense_features = list(set(range(num_features)) - set(cat_idx))
            fixlen_feature_columns = [
                SparseFeat(str(feat), cat_dims[idx])
                for idx, feat in enumerate(cat_idx)
            ] + [
                DenseFeat(
                    str(feat),
                    1,
                )
                for feat in dense_features
            ]

    else:
        # Add dummy sparse feature, otherwise it will crash...
        fixlen_feature_columns = [SparseFeat("dummy", 1)] + [
            DenseFeat(
                str(feat),
                1,
            )
            for feat in range(num_features)
        ]

    return fixlen_feature_columns


class DeepFMWrapper(nn.Module):
    def __init__(self, num_features, cat_idx, feature_index) -> None:

        self.num_features = num_features
        self.cat_idx = cat_idx
        self.feature_index = feature_index
        super().__init__()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        X_dict = {str(name): x[:, name] for name in range(self.num_features)}

        # Adding dummy spare feature
        if not self.cat_idx:
            X_dict["dummy"] = torch.zeros(x.shape[0])

        x_stacked = [X_dict[feature] for feature in self.feature_index]
        for i in range(len(x_stacked)):
            if len(x_stacked[i].shape) == 1:
                x_stacked[i] = x_stacked[i].unsqueeze(-1).to(x.device)

        x = torch.column_stack(x_stacked)
        return x


class DeepFMOutputLayer(nn.Module):
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.column_stack([1 - x, x])


class DeepFM(BaseModelTorch):
    def __init__(
        self,
        objective: str,
        x_metadata: pd.DataFrame,
        batch_size: int,
        epochs: int,
        early_stopping_rounds: int,
        dnn_dropout: float,
        name: str = "deepfm",
        num_dense_features: Optional[int] = None,
        num_classes: int = 2,
        scaler: Optional[TabScaler] = None,
        **kwargs,
    ):
        # Parameters
        self.objective = objective
        self.x_metadata = x_metadata
        self.batch_size = batch_size
        self.epochs = epochs
        self.early_stopping_rounds = early_stopping_rounds
        self.dnn_dropout = dnn_dropout
        self.num_dense_features = num_dense_features
        self.num_classes = num_classes

        if scaler is not None:
            self.scaler = TabScaler(num_scaler="min_max", one_hot_encode=False)
            self.scaler.fit_scaler_data(scaler.get_scaler_data())

        super().__init__(
            objective=objective,
            x_metadata=x_metadata,
            batch_size=batch_size,
            epochs=epochs,
            early_stopping_rounds=early_stopping_rounds,
            dnn_dropout=dnn_dropout,
            name=name,
            num_dense_features=num_dense_features,
            num_classes=num_classes,
            scaler= scaler,
            **kwargs,
        )

        # Generated

        # Parameters check
        self.two_d_output = False
        if self.objective == "classification":
            if self.num_classes != 2:
                raise ValueError(
                    "DeepFM not yet implemented for classification"
                )
            else:
                self.objective = "binary"
                self.num_classes = 1
                self.two_d_output = True

        self.cat_idx = np.where(x_metadata["type"] == "cat")[0].tolist()
        self.num_features = x_metadata.shape[0]
        self.cat_idx = np.where(x_metadata["type"] == "cat")[0].tolist()
        self.num_idx = list(set(range(self.num_features)) - set(self.cat_idx))
        self.cat_dims = [
            (int(x_metadata.iloc[i]["max"]) + 1) for i in self.cat_idx
        ]

        # self.dataset = args.dataset

        fixlen_feature_columns = get_fixlen_feature_columns(
            self.cat_idx,
            self.cat_dims,
            self.num_features,
            num_dense_features=self.num_dense_features,
        )

        self.model: nn.Module = DeepFMModel(
            linear_feature_columns=fixlen_feature_columns,
            dnn_feature_columns=fixlen_feature_columns,
            task=self.objective,
            device=self.device,
            dnn_dropout=self.dnn_dropout,
            gpus=self.gpus,
        )

        self.wrapper_model = nn.Sequential(
            DeepFMWrapper(
                self.num_features, self.cat_idx, self.model.feature_index
            ),
            self.model,
            DeepFMOutputLayer(),
        )

        if scaler is not None:
            self.wrapper_model = nn.Sequential(
                self.scaler.get_transorm_nn(), self.wrapper_model
            )

        # For compatibility
        self.experiment = None

    def fit(self, X, y, X_val=None, y_val=None,
        custom_train_dataloader=None,
        custom_val_dataloader=None):

        if self.scaler is not None:
            X = self.scaler.transform(X)
            X_val = self.scaler.transform(X_val)

        X = np.array(X, dtype=float)
        X_dict = {str(name): X[:, name] for name in range(self.num_features)}

        X_val = np.array(X_val, dtype=float)
        X_val_dict = {
            str(name): X_val[:, name] for name in range(self.num_features)
        }

        if self.objective == "binary":
            self.set_loss_y(to_torch_number(y), reduction="sum")
            loss = lambda y, y2, reduction: self.loss_func(y, y2)
            metric = "binary_crossentropy"
            labels = [0, 1]
        elif self.objective == "regression":
            loss = "mse"
            metric = "mse"
            labels = None

        self.model.compile(
            optimizer=torch.optim.AdamW(self.model.parameters()),
            loss=loss,
            metrics=[metric],
        )

        # Adding dummy spare feature
        if not self.cat_idx:
            X_dict["dummy"] = np.zeros(X.shape[0])
            X_val_dict["dummy"] = np.zeros(X_val.shape[0])

        loss_history, val_loss_history = self.model.fit(
            X_dict,
            y,
            batch_size=self.batch_size,
            epochs=self.epochs,
            validation_data=(X_val_dict, y_val),
            labels=labels,
            early_stopping=True,
            patience=self.early_stopping_rounds,
            custom_train_dataloader = custom_train_dataloader,
            custom_val_dataloader=custom_val_dataloader,
            scaler = self.scaler

        )

        if self.experiment is not None:
            for lo in loss_history:
                self.experiment.log_metric("train_loss", lo)

            for lo in val_loss_history:
                self.experiment.log_metric("validation_loss", lo)

        return loss_history, val_loss_history

    def get_logits(self, x: torch.Tensor, with_grad: bool) -> torch.Tensor:
        self.model.eval()
        if not with_grad:
            with torch.no_grad():
                # with_grad = True to avoid recursion
                return self.get_logits(x, with_grad=True)

        # Warning: use wrapper model
        preds = self.wrapper_model(x.to(self.device))
        return preds

    def predict_helper(self, x, keep_grad=False):
        self.model.eval()

        x = np.array(x, dtype=float)
        x = torch.tensor(x).float().to(self.device)
        test_loader = FastTensorDataLoader(x, batch_size=self.val_batch_size, shuffle=False)

        predictions = []
        for batch_x in test_loader:
            preds = self.get_logits(batch_x[0], with_grad=keep_grad)
            predictions.append(preds.cpu())

        return np.concatenate(predictions)

    @staticmethod
    def define_trial_parameters(
        trial: optuna.Trial, trial_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        params = {
            "dnn_dropout": trial.suggest_float("dnn_dropout", 0, 0.9),
        }
        return params

        # dnn_dropout, l2_reg_linear, l2_reg_embedding,
        # l2_reg_dnn, dnn_hidden_units?


models: List[Tuple[str, Type[Model]]] = [("deepfm", DeepFM)]
