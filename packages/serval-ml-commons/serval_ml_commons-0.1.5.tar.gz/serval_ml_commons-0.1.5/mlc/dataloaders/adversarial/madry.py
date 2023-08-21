import sys

sys.path.append("../constrained-attacks")

from typing import Tuple
import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset

from mlc.models.torch_models import BaseModelTorch
from mlc.dataloaders.dataloader import BaseDataLoader
from constrained_attacks.attacks.cta.capgd import CAPGD
from mlc.datasets.dataset import Dataset

attacks = {
    "pgd": CAPGD, "c-pgd": CAPGD
}


def get_adversarial_collate(attack, augment, custom_loader):
    def custom_collate(batch):
        collated = torch.utils.data.dataloader.default_collate(batch)
        if attack is not None:
            x = collated[0].to(attack.device)
            y = collated[1].to(attack.device)
            y_adv = y if custom_loader.dataloader.transform_y is None else y[:, 1].long()
            adv_x = attack(x,
                           y_adv) if custom_loader.dataloader.scaler is None else custom_loader.dataloader.scaler.transform(
                attack(custom_loader.scaler.inverse_transform(x), y_adv))
        if augment == 2:
            return torch.cat([x, adv_x]), *[torch.cat([collated[k], collated[k]]) for k in range(1, len(collated))]
        elif augment == 1:
            return torch.cat([x[:len(x) // 2], adv_x[len(x) // 2:]]), *collated[1:]
        else:
            return adv_x, *collated[1:]

    return custom_collate


class MadryATDataLoader(BaseDataLoader):
    def __init__(self, dataset: Dataset = None, scaler=None, model: BaseModelTorch = None, attack="pgd",
                 attack_params={"eps": 0.3, "norm": "L2"}, move_all_to_model_device: bool = True,
                 filter_constraints: bool = False, augment: int = 1, verbose=False
                 ) -> None:
        self.num_workers = 0
        self.dataset = dataset
        self.device = model.device
        self.model = model.wrapper_model
        self.move_all_to_model_device = move_all_to_model_device
        self.custom_scaler = None

        constraints = dataset.get_constraints()
        fix_equality_constraints_end = True
        if not attack.startswith("c-"):
            constraints.relation_constraints = None
            fix_equality_constraints_end = False

        self.attack = attacks.get(attack, CAPGD)(constraints=constraints, scaler=scaler, model=self.model,
                                                 fix_equality_constraints_end=fix_equality_constraints_end,
                                                 fix_equality_constraints_iter=False,
                                                 model_objective=model.predict_proba, **attack_params,
                                                 verbose=verbose)
        self.filter_constraints = filter_constraints
        self.augment = augment
        self.scaler = scaler

    def set_tensors(self, tensors, scaler):
        self.dataset.tensors = tensors
        self.custom_scaler = scaler

    def get_dataloader(
            self, x: np.ndarray, y: np.ndarray, train: bool, batch_size: int) -> DataLoader[Tuple[torch.Tensor, ...]]:
        # Create dataset
        x_scaled = torch.Tensor(self.scaler.transform(x)).float()
        x = torch.Tensor(x).float()
        y = torch.Tensor(y).long()
        if self.move_all_to_model_device:
            x = x.to(self.device)
            y = y.to(self.device)

        self.dataset = TensorDataset(x, y)

        # Create dataloader
        if train:

            self.dataloader = DataLoader(
                dataset=self.dataset,
                batch_size=batch_size,
                shuffle=True,
                num_workers=self.num_workers,
                collate_fn=get_adversarial_collate(self.attack, self.augment, self)
            )

        else:
            self.dataloader = DataLoader(
                dataset=self.dataset,
                batch_size=batch_size,
                shuffle=False,
                num_workers=self.num_workers
            )
        self.dataloader.scaler = None
        self.dataloader.transform_y = None
        return self.dataloader
