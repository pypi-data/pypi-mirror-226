# The SAINT model.
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple, Type

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from einops import rearrange
from torch import einsum
from torch.utils.data import DataLoader, TensorDataset

from mlc.load_do_save import load_json, save_json
from mlc.models.model import Model
from mlc.models.tabsurvey.saint_lib.augmentations import embed_data_mask
from mlc.models.tabsurvey.saint_lib.data_openml import DataSetCatCon
from mlc.models.tabsurvey.saint_lib.models.pretrainmodel import (
    SAINT as SAINTModel,
)
from mlc.models.torch_models import BaseModelTorch
from mlc.transformers.tab_scaler import TabScaler
from mlc.utils import parent_exists, to_torch_number

"""
    SAINT: Improved Neural Networks for Tabular Data via
    Row Attention and Contrastive Pre-Training
    (https://arxiv.org/abs/2106.01342)

    Code adapted from: https://github.com/somepago/saint
"""
import optuna


class SAINTWrapper(nn.Module):
    def __init__(self, cat_idx, num_idx, task, model, device) -> None:
        super().__init__()
        self.cat_idx = cat_idx
        self.num_idx = num_idx
        self.task = task
        self.model = model
        self.device = device

    def forward(self, X: torch.Tensor) -> torch.Tensor:

        device = self.device
        Y = torch.ones((X.shape[0], 1))
        X_mask = torch.ones_like(X)

        X = torch.clone(X)

        self.X1 = (
            X[:, self.cat_idx].clone().type(torch.int64)
        )  # categorical columns
        self.X2 = (
            X[:, self.num_idx].clone().type(torch.float32)
        )  # numerical columns
        self.X1_mask = (
            X_mask[:, self.cat_idx].clone().type(torch.int64)
        )  # categorical columns
        self.X2_mask = (
            X_mask[:, self.num_idx].clone().type(torch.int64)
        )  # numerical columns
        if self.task == "regression":
            self.y = Y.astype(np.float32)
        else:
            self.y = Y  # .astype(np.float32)
        self.cls = torch.zeros_like(self.y, dtype=int)
        self.cls_mask = torch.ones_like(self.y, dtype=int)

        x_categ, x_cont, cat_mask, con_mask = (
            torch.concat((self.cls, self.X1), dim=1),
            self.X2,
            torch.concat((self.cls_mask, self.X1_mask), dim=1),
            self.X2_mask,
        )

        x_categ, x_cont, cat_mask, con_mask = (
            x_categ.to(device),
            x_cont.to(device),
            cat_mask.to(device),
            con_mask.to(device),
        )

        _, x_categ_enc, x_cont_enc = embed_data_mask(
            x_categ, x_cont, cat_mask, con_mask, self.model
        )
        reps = self.model.transformer(x_categ_enc, x_cont_enc)
        y_reps = reps[:, 0, :]
        y_outs = self.model.mlpfory(y_reps)

        return y_outs


class SAINT(BaseModelTorch):
    def __init__(
        self,
        objective: str,
        x_metadata: pd.DataFrame,
        batch_size: int,
        epochs: int,
        early_stopping_rounds: int,
        num_classes: int,
        dim: int = 64,
        depth: int = 6,
        heads: int = 8,
        dropout: float = 0.1,
        val_batch_size: int = 100000,
        name="saint",
        scaler: Optional[TabScaler] = None,
        **kwargs,
    ):

        # Thibault: this should be handled somewhere else
        # Decreasing some hyperparameter to cope with memory issues
        # dim = self.params["dim"] if args.num_features < 20000 else 8
        # self.batch_size = self.args.batch_size
        # depth = self.params["depth"] if args.num_features < 20000 else 3
        # heads = self.params["heads"] if args.num_features < 20000 else 4
        # print("Using dim %d and batch size %d" % (dim, self.batch_size))

        self.objective = objective
        self.x_metadata = x_metadata
        self.batch_size = batch_size
        self.epochs = epochs
        self.early_stopping_rounds = early_stopping_rounds
        self.num_classes = num_classes

        self.dim = dim
        self.depth = depth
        self.heads = heads
        self.dropout = dropout
        self.val_batch_size = val_batch_size

        if scaler is not None:
            self.scaler = TabScaler(num_scaler="min_max", one_hot_encode=False)
            self.scaler.fit_scaler_data(scaler.get_scaler_data())

        # Generate super call
        super().__init__(
            objective=objective,
            x_metadata=x_metadata,
            batch_size=batch_size,
            epochs=epochs,
            early_stopping_rounds=early_stopping_rounds,
            num_classes=num_classes,
            dim=dim,
            depth=depth,
            heads=heads,
            dropout=dropout,
            val_batch_size=val_batch_size,
            name=name,
            scaler=scaler,
            **kwargs,
        )

        # Generated

        self.cat_idx = np.where(x_metadata["type"] == "cat")[0].tolist()
        self.num_features = x_metadata.shape[0]
        self.cat_idx = np.where(x_metadata["type"] == "cat")[0].tolist()
        self.num_idx = list(set(range(self.num_features)) - set(self.cat_idx))
        self.cat_dims = [
            (int(x_metadata.iloc[i]["max"]) + 1) for i in self.cat_idx
        ]

        self.model = SAINTModel(
            categories=tuple(
                np.append(np.array([1]), np.array(self.cat_dims)).astype(int)
            ),
            num_continuous=len(self.num_idx),
            dim=dim,
            dim_out=1,
            depth=depth,  # 6
            heads=heads,  # 8
            attn_dropout=self.dropout,  # 0.1
            ff_dropout=self.dropout,  # 0.1
            mlp_hidden_mults=(4, 2),
            cont_embeddings="MLP",
            attentiontype="colrow",
            final_mlp_style="sep",
            y_dim=self.num_classes,
        )

        # if self.args.data_parallel:
        #     self.model.transformer = nn.DataParallel(
        #         self.model.transformer, device_ids=self.args.gpu_ids
        #     )
        #     self.model.mlpfory = nn.DataParallel(
        #         self.model.mlpfory, device_ids=self.args.gpu_ids
        #     )

        self.wrapper_model = SAINTWrapper(
            self.cat_idx, self.num_idx, self.objective, self.model, self.device
        )

        if hasattr(self, "scaler") and (self.scaler is not None):
            self.wrapper_model = nn.Sequential(
                self.scaler.get_transorm_nn(), self.wrapper_model
            )

        self.experiment = None

    def fit(self, X, y, X_val=None, y_val=None):

        if self.scaler is not None:
            X = self.scaler.transform(X)
            X_val = self.scaler.transform(X_val)
        self.set_loss_y(to_torch_number(y))
        criterion = self.loss_func

        # if (y.ndim == 1) or (y.shape[1] == 1):
        #     y = np.column_stack((1 - y, y))
        # if (y_val.ndim == 1) or (y_val.shape[1] == 1):
        #     y_val = np.column_stack((1 - y_val, y_val))

        optimizer = optim.AdamW(self.model.parameters(), lr=0.00003)

        self.model.to(self.device)

        # SAINT wants it like this...
        X = {"data": X, "mask": np.ones_like(X)}
        y = {"data": y.reshape(-1, 1)}
        X_val = {"data": X_val, "mask": np.ones_like(X_val)}
        y_val = {"data": y_val.reshape(-1, 1)}

        train_ds = DataSetCatCon(X, y, self.cat_idx, self.objective)
        trainloader = DataLoader(
            train_ds, batch_size=self.batch_size, shuffle=True, num_workers=4
        )

        val_ds = DataSetCatCon(X_val, y_val, self.cat_idx, self.objective)
        valloader = DataLoader(
            val_ds,
            batch_size=self.val_batch_size,
            shuffle=True,
            num_workers=4,
        )

        min_val_loss = float("inf")
        min_val_loss_idx = 0

        loss_history = []
        val_loss_history = []

        for epoch in range(self.epochs):
            self.model.train()

            for i, data in enumerate(trainloader, 0):
                print(
                    f"Epoch: {epoch} / {self.epochs}, "
                    f"Batch: {i} / {len(trainloader)}"
                )

                optimizer.zero_grad()

                # x_categ is the the categorical data,
                # x_cont has continuous data,
                # y_gts has ground truth ys.
                # cat_mask is an array of ones same shape as
                # x_categ and an additional column(corresponding to CLS
                # token) set to 0s.
                # con_mask is an array of ones same shape as x_cont.
                x_categ, x_cont, y_gts, cat_mask, con_mask = data

                x_categ, x_cont = x_categ.to(self.device), x_cont.to(
                    self.device
                )
                cat_mask, con_mask = cat_mask.to(self.device), con_mask.to(
                    self.device
                )

                # We are converting the data to embeddings in the next step
                _, x_categ_enc, x_cont_enc = embed_data_mask(
                    x_categ, x_cont, cat_mask, con_mask, self.model
                )

                reps = self.model.transformer(x_categ_enc, x_cont_enc)

                # select only the representations corresponding to CLS token
                # and apply mlp on it in the next step to get the predictions.
                y_reps = reps[:, 0, :]

                y_outs = self.model.mlpfory(y_reps)

                if self.objective == "regression":
                    y_gts = y_gts.to(self.device)
                elif self.objective == "classification":
                    y_gts = y_gts.to(self.device).squeeze()
                else:
                    y_gts = y_gts.to(self.device).float()

                loss = criterion(y_outs, y_gts)
                loss.backward()
                optimizer.step()

                loss_history.append(loss.item())
                if self.experiment is not None:
                    self.experiment.log_metric("train_loss", loss.item())

                print("Loss", loss.item())

            # Early Stopping
            val_loss = 0.0
            val_dim = 0
            self.model.eval()
            with torch.no_grad():
                for data in valloader:
                    x_categ, x_cont, y_gts, cat_mask, con_mask = data

                    x_categ, x_cont = x_categ.to(self.device), x_cont.to(
                        self.device
                    )
                    cat_mask, con_mask = cat_mask.to(self.device), con_mask.to(
                        self.device
                    )

                    _, x_categ_enc, x_cont_enc = embed_data_mask(
                        x_categ, x_cont, cat_mask, con_mask, self.model
                    )
                    reps = self.model.transformer(x_categ_enc, x_cont_enc)
                    y_reps = reps[:, 0, :]
                    y_outs = self.model.mlpfory(y_reps)

                    if self.objective == "regression":
                        y_gts = y_gts.to(self.device)
                    elif self.objective == "classification":
                        y_gts = y_gts.to(self.device).squeeze()
                    else:
                        y_gts = y_gts.to(self.device).float()

                    val_loss += criterion(y_outs, y_gts).item()
                    val_dim += 1
            val_loss /= val_dim

            val_loss_history.append(val_loss)
            if self.experiment is not None:
                self.experiment.log_metric("validation_loss", val_loss)

            print("Epoch", epoch, "loss", val_loss)

            if val_loss < min_val_loss:
                min_val_loss = val_loss
                min_val_loss_idx = epoch

                # Save the currently best model
                self.save_best_weights()
                # self.save_model(filename_extension="best", directory="tmp")

            if min_val_loss_idx + self.early_stopping_rounds < epoch:
                print(
                    "Validation loss has not improved for %d steps!"
                    % self.early_stopping_rounds
                )
                print("Early stopping applies.")
                break

        self.load_best_weights()
        return loss_history, val_loss_history

    def get_logits(self, x: torch.Tensor, with_grad: bool) -> torch.Tensor:
        if not with_grad:
            with torch.no_grad():
                # with_grad = True to avoid recursion
                return self.get_logits(x, with_grad=True)

        # Warning: use wrapper model
        preds = self.wrapper_model(x)
        if self.objective == "binary":
            preds = torch.sigmoid(preds)
        elif self.objective == "classification":
            preds = F.softmax(preds, dim=1)
        return preds

    def predict_helper(self, x, keep_grad=False):
        self.model.eval()

        x = np.array(x, dtype=float)
        x = torch.tensor(x).float()

        test_dataset = TensorDataset(x)
        test_loader = DataLoader(
            dataset=test_dataset,
            batch_size=self.val_batch_size,
            shuffle=False,
            num_workers=2,
        )

        predictions = []
        for batch_x in test_loader:
            preds = self.get_logits(batch_x[0], with_grad=keep_grad)
            predictions.append(preds.cpu())

        return np.concatenate(predictions)

    def save(self, path: str) -> None:
        kwargs_save = deepcopy(self.constructor_kwargs)
        if "x_metadata" in kwargs_save:
            kwargs_save.pop("x_metadata")

        args_path = f"{path}/args.json"
        save_json(kwargs_save, parent_exists(args_path))

        weigths_path = f"{path}/weights.pt"
        torch.save(self.model.state_dict(), parent_exists(weigths_path))

    @classmethod
    def load_class(cls, path: str, **kwargs: Dict[str, Any]) -> BaseModelTorch:

        args_path = f"{path}/args.json"
        weigths_path = f"{path}/weights.pt"

        load_kwargs = load_json(args_path)
        model = cls(**load_kwargs, **kwargs)
        model.model.load_state_dict(torch.load(weigths_path))
        model.model.to(model.device)

        return model

    def attribute(self, X, y, strategy=""):
        """Generate feature attributions for the model input.
        Two strategies are supported: default ("") or "diag".
        The default strategie takes the sum
        over a column of the attention map, while "diag"
        returns only the diagonal (feature attention to itself)
        of the attention map.
        return array with the same shape as X.
        """
        global my_attention
        # self.load_model(filename_extension="best", directory="tmp")

        X = {"data": X, "mask": np.ones_like(X)}
        y = {"data": np.ones((X["data"].shape[0], 1))}

        test_ds = DataSetCatCon(X, y, self.cat_idx, self.objective)
        testloader = DataLoader(
            test_ds,
            batch_size=self.val_batch_size,
            shuffle=False,
            num_workers=4,
        )

        self.model.eval()
        # print(self.model)
        # Apply hook.
        my_attention = torch.zeros(0)

        def sample_attribution(layer, minput, output):
            global my_attention
            # print(minput)
            """ an hook to extract the attention maps. """
            h = layer.heads
            q, k, v = layer.to_qkv(minput[0]).chunk(3, dim=-1)
            q, k, v = map(
                lambda t: rearrange(t, "b n (h d) -> b h n d", h=h), (q, k, v)
            )
            sim = einsum("b h i d, b h j d -> b h i j", q, k) * layer.scale
            my_attention = sim.softmax(dim=-1)

        # print(type(self.model.transformer.layers[0][0].fn.fn))
        self.model.transformer.layers[0][0].fn.fn.register_forward_hook(
            sample_attribution
        )
        attributions = []
        with torch.no_grad():
            for data in testloader:
                x_categ, x_cont, y_gts, cat_mask, con_mask = data

                x_categ, x_cont = x_categ.to(self.device), x_cont.to(
                    self.device
                )
                cat_mask, con_mask = cat_mask.to(self.device), con_mask.to(
                    self.device
                )
                # print(x_categ.shape, x_cont.shape)
                _, x_categ_enc, x_cont_enc = embed_data_mask(
                    x_categ, x_cont, cat_mask, con_mask, self.model
                )
                reps = self.model.transformer(x_categ_enc, x_cont_enc)
                # y_reps = reps[:, 0, :]
                # y_outs = self.model.mlpfory(y_reps)
                if strategy == "diag":
                    attributions.append(
                        my_attention.sum(dim=1)[:, 1:, 1:].diagonal(0, 1, 2)
                    )
                else:
                    attributions.append(
                        my_attention.sum(dim=1)[:, 1:, 1:].sum(dim=1)
                    )

        attributions = np.concatenate(attributions)
        return attributions

    @staticmethod
    def define_trial_parameters(trial: optuna.Trial, trial_params: Dict[str, Any]):
        params = {
            "dim": trial.suggest_categorical("dim", [32, 64, 128, 256]),
            "depth": trial.suggest_categorical("depth", [1, 2, 3, 6, 12]),
            "heads": trial.suggest_categorical("heads", [2, 4, 8]),
            "dropout": trial.suggest_categorical(
                "dropout", [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
            ),
        }
        return params


models: List[Tuple[str, Type[Model]]] = [("saint", SAINT)]
