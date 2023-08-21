from typing import Tuple

import torch
from imblearn.over_sampling import SMOTE
from torch.utils.data import DataLoader, TensorDataset

from mlc.dataloaders.dataloader import BaseDataLoader


class SMOTEDataLoader(BaseDataLoader):
    def __init__(self, num_workers: int = 4, random_state: int = 42, smote_params: dict = {},
                 filter_constraints: bool = False) -> None:
        self.num_workers = num_workers
        self.filter_constraints = filter_constraints
        self.smote = SMOTE(random_state=random_state, **smote_params)

    def get_dataloader(
            self, x: torch.Tensor, y: torch.Tensor, train: bool, batch_size: int, augment: bool = True
    ) -> DataLoader[Tuple[torch.Tensor, ...]]:

        # Create dataset
        x_aug, y_aug = self.smote.fit_resample(x.cpu().detach().numpy(), y.cpu().detach().numpy())
        x_aug, y_aug = torch.Tensor(x_aug).type(x), torch.Tensor(y_aug).type(y)
        if augment:
            dataset = TensorDataset(torch.cat((x, x_aug)), torch.cat((y, y_aug)))
        else:
            dataset = TensorDataset(x_aug, y_aug)

        # Create dataloader
        if train:

            return DataLoader(
                dataset=dataset,
                batch_size=batch_size,
                shuffle=True,
                num_workers=self.num_workers,
            )

        else:
            return DataLoader(
                dataset=dataset,
                batch_size=batch_size,
                shuffle=False,
                num_workers=self.num_workers,
            )
