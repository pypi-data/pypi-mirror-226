## Adapted from https://github.com/yandex-research/tab-ddpm/
from typing import Tuple

import torch
from torch.utils.data import DataLoader, TensorDataset

from mlc.dataloaders.dataloader import BaseDataLoader
from mlc.dataloaders.generative.tab_ddpm.lib.data import Dataset
from mlc.dataloaders.generative.tab_ddpm.lib.util import TaskType
from mlc.dataloaders.generative.tab_ddpm.sample import sample
from mlc.dataloaders.generative.tab_ddpm.train import train, get_model
from mlc.datasets.dataset import Dataset as MLC_Dataset


class DDPMDataLoader(BaseDataLoader):
    def __init__(self, num_workers: int = 2, original_dataset: MLC_Dataset = None, ddpm_params: dict = {},
                 pretrained_path: str = None, save_path: str = None, nb_classes: int = 2,
                 task_type: str = TaskType.MULTICLASS, train_batch_size: int = 32) -> None:

        self.num_workers = num_workers
        task = TaskType.BINCLASS if nb_classes == 2 else task_type
        if pretrained_path is None:

            x, y = original_dataset.get_x_y()
            metadata = original_dataset.get_metadata(only_x=True)
            transformations = original_dataset.get_ddpm_transformations()
            num_index = [k for (k, v) in enumerate(metadata.type.values) if v != "cat"]
            cat_index = [k for (k, v) in enumerate(metadata.type.values) if v == "cat"]
            dataset = Dataset({"train": x.values[:, num_index]}, {"train": x.values[:, cat_index]}, {"train": y}, {},
                              task,
                              nb_classes)

            self.generator = train("../", dataset=dataset, T_dict=transformations, batch_size=train_batch_size,
                                   **ddpm_params)
        else:
            self.generator = get_model(
                ddpm_params.get("model_type"),
                ddpm_params.get("model_params"),
                ddpm_params.get("num_numerical_features_"),
                category_sizes=dataset.get_category_sizes('train')
            )

            self.generator.load_state_dict(
                torch.load(pretrained_path, map_location="cpu")
            )

        if save_path is not None:
            self.save(save_path)

    def load(self, pretrained_path: str):
        self.generator._model.load(pretrained_path)

    def save(self, save_path: str):
        self.generator._model.save(save_path)

    def get_dataloader(
            self, x: torch.Tensor, y: torch.Tensor, train: bool, batch_size: int, augment: bool = True
    ) -> DataLoader[Tuple[torch.Tensor, ...]]:

        # Create dataset
        x_aug, y_aug = sample("../", model=self.generator, num_samples=len(y), batch_size=batch_size)

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
