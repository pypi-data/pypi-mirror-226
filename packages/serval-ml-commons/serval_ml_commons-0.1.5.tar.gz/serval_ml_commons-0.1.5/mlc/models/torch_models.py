from __future__ import annotations

import logging
from copy import deepcopy
from typing import Any, Dict, Optional, Union
from uuid import uuid4

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

from mlc.dataloaders.default import DefaultDataLoader
from mlc.load_do_save import load_json, save_json
from mlc.models.model import Model
from mlc.typing import NDFloat, NDNumber
from mlc.utils import parent_exists

logger = logging.getLogger(__name__)
from mlc.dataloaders.fast_dataloader import FastTensorDataLoader


class BaseModelTorch(Model):
    def __init__(
        self,
        name: str,
        objective: str,
        batch_size: int,
        epochs: int,
        early_stopping_rounds: int,
        learning_rate: float = 0.001,
        val_batch_size: int = 100000,
        class_weight: Union[str, Dict[int, str]] = None,
        force_device: str = None,
        is_text: bool = False,
        weight_decay=0,
        use_gpu: bool = False,
        gpu_ids: Optional[str] = None,
        data_parallel=False,
        **kwargs: Any,
    ) -> None:

        # Generate super call with all the parameters
        super().__init__(
            name=name,
            objective=objective,
            batch_size=batch_size,
            epochs=epochs,
            early_stopping_rounds=early_stopping_rounds,
            learning_rate=learning_rate,
            val_batch_size=val_batch_size,
            class_weight=class_weight,
            weight_decay=weight_decay,
            force_device=force_device,
            is_text=is_text,
            **kwargs,
        )

        self.force_device = force_device
        self.device = self.get_device()
        self.objective = objective
        self.batch_size = batch_size
        self.epochs = epochs
        self.early_stopping_rounds = early_stopping_rounds
        self.learning_rate = learning_rate
        self.force_train = False
        self.val_batch_size = val_batch_size
        self.class_weight = class_weight
        self.is_text = is_text
        self.weight_decay = weight_decay

        # Computed

        self.gpus = (
            gpu_ids
            if use_gpu and torch.cuda.is_available() and data_parallel
            else None
        )

        self.data_loader = DefaultDataLoader()

        if self.objective == "regression":
            self.set_loss(nn.MSELoss())
        elif self.objective == "classification":
            self.set_loss(nn.CrossEntropyLoss())
        else:
            self.set_loss(nn.BCEWithLogitsLoss())

        self.uuid = str(uuid4())

    def to_device(self, device=None) -> None:
        self.device = device if device is not None else self.device
        logger.debug(f"On Device: {self.device}")
        self.model.to(self.device)
        self.data_loader.device = self.device

    def get_device(self):
        if self.force_device is not None:
            device = self.force_device
        else:
            if torch.cuda.is_available():
                device = "cuda"
            else:
                device = "cpu"
        return torch.device(device)

    def eval(self) -> None:
        self.force_train = False

    def train(self) -> None:
        self.force_train = True

    def set_loss_y(self, y: NDNumber, **kwargs: Any) -> None:
        class_weight = self.class_weight
        if class_weight is not None:
            if self.class_weight == "balanced":
                y_w = y
                if y.ndim == 2:
                    y_w = y.argmax(1)
                class_weight = torch.Tensor(
                    1 - torch.unique(y_w, return_counts=True)[1] / len(y)
                )

            else:
                class_weight = torch.Tensor(self.class_weight)

        class_weight = class_weight.to(self.device)
        if self.objective == "regression":
            loss_func = nn.MSELoss(**kwargs)
        elif self.objective == "classification":
            loss_func = nn.CrossEntropyLoss(weight=class_weight, **kwargs)
        else:
            if hasattr(self, "num_classes") and (self.num_classes == 1):
                class_weight = torch.Tensor(class_weight[1] / class_weight[0])
            loss_func = nn.BCEWithLogitsLoss(pos_weight=class_weight, **kwargs)

        self.set_loss(loss_func)

    def fit(
        self,
        x: NDFloat,
        y: NDNumber,
        x_val: Optional[NDFloat] = None,
        y_val: Optional[NDNumber] = None,
        custom_train_dataloader=None,
        custom_val_dataloader=None,
        scaler=None
    ):
        # if reset_weight:
        #     self.reset_all_weights()

        optimizer = optim.AdamW(
            filter(lambda p: p.requires_grad, self.model.parameters()),
            lr=self.learning_rate,
            weight_decay=self.weight_decay,
        )

        if x_val is None:
            (
                _,
                count_idx,
                count,
            ) = np.unique(y, return_counts=True, return_index=True)
            if np.sum(count == 1) > 0:
                to_delete = count_idx[np.where(count == 1)[0]]
                x = np.delete(x, to_delete, axis=0)
                y = np.delete(y, to_delete, axis=0)

            x, x_val, y, y_val = train_test_split(
                x, y, test_size=0.2, random_state=42, stratify=y
            )

        if self.is_text:
            x = torch.tensor(x).int()
            x_val = torch.tensor(x_val).int()
        else:
            if isinstance(x, pd.DataFrame):
                x = x.values
            if isinstance(x_val, pd.DataFrame):
                x_val = x_val.values
            x = torch.tensor(x).float()
            x_val = torch.tensor(x_val).float()

        y = torch.tensor(y)
        y_val = torch.tensor(y_val)

        if (y.ndim == 1) or (y.shape[1] == 1):
            y_train = torch.column_stack((1 - y, y))
        if (y_val.ndim == 1) or (y_val.shape[1] == 1):
            y_val = torch.column_stack((1 - y_val, y_val))

        self.set_loss_y(y_train)
        loss_func = self.loss_func

        y_train = y_train.float()
        y_val = y_val.float()

        # train_loader = self.data_loader.get_dataloader(
        #     x, y, True, self.batch_size
        # )

        if custom_train_dataloader:
            if hasattr(custom_train_dataloader,"dataset"):
                custom_train_dataloader.dataset.tensors = x.to(self.device), y_train.to(self.device)
            else:
                custom_train_dataloader.tensors = x.to(self.device), y_train.to(self.device)
            train_loader = custom_train_dataloader
            train_loader.scaler = scaler
            train_loader.transform_y = True
        else:
            train_loader = FastTensorDataLoader(
                x.to(self.device),
                y_train.to(self.device),
                batch_size=self.batch_size,
                shuffle=True,
            )

        if custom_val_dataloader:
            custom_val_dataloader.dataset.tensors = x_val.to(self.device),
            y_val.to(self.device)
            val_loader = custom_val_dataloader
            train_loader.scaler = scaler
        else:
            val_loader = FastTensorDataLoader(
                x_val.to(self.device),
                y_val.to(self.device),
                batch_size=self.val_batch_size,
                shuffle=False,
            )

        min_val_loss = float("inf")
        min_val_loss_idx = 0

        loss_history = []
        val_loss_history = []

        for epoch in range(self.epochs):
            for i, (batch_x, batch_y) in enumerate(train_loader):

                out = self.model(batch_x.to(self.device))

                if (
                    self.objective == "regression"
                    or self.objective == "binary"
                ):
                    out = out.squeeze()

                loss = loss_func(out, batch_y.to(self.device))
                loss_history.append(loss.item())
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                logger.debug(f"Batch {i}")

            # Early Stopping
            if self.early_stopping_rounds > 0:
                val_loss = 0.0
                val_dim = 0
                with torch.no_grad():
                    for val_i, (batch_val_x, batch_val_y) in enumerate(
                        val_loader
                    ):
                        out = self.model(batch_val_x.to(self.device))

                        if (
                            self.objective == "regression"
                            or self.objective == "binary"
                        ):
                            out = out.squeeze()

                        val_loss += loss_func(
                            out, batch_val_y.to(self.device)
                        ).item()
                        val_dim += 1

                val_loss /= val_dim
                val_loss_history.append(val_loss)

                # logger.debug("Epoch %d, Val Loss: %.5f" % (epoch, val_loss))
                print("Epoch %d, Val Loss: %.5f" % (epoch, val_loss))

                if val_loss < min_val_loss:
                    min_val_loss = val_loss
                    min_val_loss_idx = epoch

                    # Save the currently best model
                    self.save_best_weights()

                if min_val_loss_idx + self.early_stopping_rounds < epoch:
                    logger.debug(
                        "Validation loss has not improved for %d steps!"
                        % self.early_stopping_rounds
                    )
                    logger.debug("Early stopping applies.")
                    break

        self.model.__hash__()
        # Load best model
        if self.early_stopping_rounds > 0:
            self.load_best_weights()
        return loss_history, val_loss_history

    def predict(self, x):
        if self.objective == "regression":
            self.predictions = self.predict_helper(x)
        else:
            self.predict_proba(x)
            self.predictions = np.argmax(self.prediction_probabilities, axis=1)

        return self.predictions

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        probas = self.predict_helper(x)

        # If binary task returns only probability for the true class,
        # adapt it to return (N x 2)
        if probas.shape[1] == 1:
            probas = np.concatenate((1 - probas, probas), 1)

        self.prediction_probabilities = probas
        return self.prediction_probabilities

    def get_logits(self, x: torch.Tensor, with_grad: bool) -> torch.Tensor:
        if not with_grad:
            with torch.no_grad():
                # with_grad = True to avoid recursion
                return self.get_logits(x, with_grad=True)

        preds = self.model(x)
        if self.objective == "binary":
            preds = torch.sigmoid(preds)
        return preds

    def predict_helper(
        self,
        x: Union[NDFloat, torch.Tensor, pd.DataFrame],
        load_all_gpu: bool = False,
    ) -> NDFloat:
        if self.force_train:
            self.model.train()
        else:
            self.model.eval()

        if isinstance(x, pd.DataFrame):
            x = x.values

        if self.is_text:
            x = torch.tensor(x).int()
        else:
            x = torch.tensor(x).float()

        if load_all_gpu:
            x = x.to(self.device)

        # test_dataset = TensorDataset(x)
        # test_loader = DataLoader(
        #     dataset=test_dataset,
        #     batch_size=self.val_batch_size,
        #     shuffle=False,
        #     num_workers=0,
        # )

        test_loader = FastTensorDataLoader(
            x.to(self.device), batch_size=self.val_batch_size, shuffle=False
        )
        predictions = []
        with torch.no_grad():
            for batch_x in test_loader:
                if load_all_gpu:
                    preds = self.model(batch_x[0])
                else:
                    preds = self.model(batch_x[0].to(self.device))

                if self.objective == "binary":
                    preds = torch.sigmoid(preds)
                if self.device == "cuda":
                    torch.cuda.synchronize()
                predictions.append(preds.detach().cpu().numpy())
        return np.concatenate(predictions)

    def save(self, path: str) -> None:
        kwargs_save = deepcopy(self.constructor_kwargs)
        if "x_metadata" in kwargs_save:
            kwargs_save.pop("x_metadata")

        if "scaler" in kwargs_save:
            kwargs_save.pop("scaler")

        args_path = f"{path}/args.json"
        save_json(kwargs_save, parent_exists(args_path))

        weigths_path = f"{path}/weights.pt"
        torch.save(self.model.state_dict(), parent_exists(weigths_path))

    @classmethod
    def load_class(cls, path: str, **kwargs: Dict[str, Any]) -> BaseModelTorch:

        args_path = f"{path}/args.json"
        weigths_path = f"{path}/weights.pt"

        load_kwargs = load_json(args_path)
        args = {**load_kwargs, **kwargs}
        model = cls(**args)
        model.model.load_state_dict(torch.load(weigths_path))

        return model

    def save_best_weights(self) -> None:
        filename = parent_exists(f"./tmp/{self.uuid}_best.pt")
        torch.save(self.model.state_dict(), filename)

    def load_best_weights(self) -> None:
        filename = f"./tmp/{self.uuid}_best.pt"
        state_dict = torch.load(filename)
        self.model.load_state_dict(state_dict)

    def load(self, path: str) -> None:
        state_dict = torch.load(f"{path}/weights.pt")
        if self.scaler is None:
            model = self.model
        else:
            model = self.model[1]
        model.load_state_dict(state_dict)

    def get_model_size(self) -> int:
        model_size = sum(
            t.numel() for t in self.model.parameters() if t.requires_grad
        )
        return model_size

    def reset_all_weights(self) -> None:
        """
        refs:
            - https://discuss.pytorch.org/t/how-to-re-set-alll-parameters-in
            -a-network/20819/6
            - https://stackoverflow.com/questions/63627997/reset-parameters
            -of-a-neural-network-in-pytorch
            - https://pytorch.org/docs/stable/generated/torch.nn.Module.html
        """

        @torch.no_grad()
        def weight_reset(m: nn.Module) -> None:
            # - check if the current module has reset_parameters & if it's
            # callabed called it on m
            reset_parameters = getattr(m, "reset_parameters", None)
            if callable(reset_parameters):
                m.reset_parameters()

        # Applies fn recursively to every submodule see:
        # https://pytorch.org/docs/stable/generated/torch.nn.Module.html
        self.model.apply(fn=weight_reset)

    def set_dataloader(self, dataloader) -> None:
        self.data_loader = dataloader

    def set_loss(self, loss) -> None:
        self.loss_func = loss

    def set_experiment(self, experiment):
        self.experiment = experiment
