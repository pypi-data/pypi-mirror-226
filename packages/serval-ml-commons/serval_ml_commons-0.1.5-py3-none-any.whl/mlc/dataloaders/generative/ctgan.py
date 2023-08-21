from typing import Tuple

import torch
from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer
from torch.utils.data import DataLoader, TensorDataset

from mlc.dataloaders.sdv import SDVDataLoader
from mlc.datasets.dataset import Dataset


class CTGANDataLoader(SDVDataLoader):
    def __init__(self, num_workers: int = 4, original_dataset: Dataset = None, scaler=None, generator_epochs: int = 500,
                 filter_constraints: bool = False, pretrained_path: str = None, save_path: str = None
                 , train_batch_size: int = 32, verbose: bool = False, subset: int = 0) -> None:
        self.dataset = original_dataset
        self.scaler = scaler
        self.filter_constraints = filter_constraints

        metadata = SingleTableMetadata()
        self.data = self.dataset.get_data()
        if subset > 0:
            self.data = self.data[:subset]
        metadata.detect_from_dataframe(data=self.data)

        self.generator = CTGANSynthesizer(metadata, epochs=generator_epochs, batch_size=train_batch_size,
                                          verbose=verbose)

        super().__init__(num_workers, pretrained_path, save_path)

    def get_dataloader(
            self, x: torch.Tensor, y: torch.Tensor, train: bool, batch_size: int, augment: bool = True
    ) -> DataLoader[Tuple[torch.Tensor, ...]]:

        # Create dataset
        synthetic_data = self.generator.sample(num_rows=len(y))
        self.dataset.set_data(synthetic_data, filter_constraints=self.filter_constraints)
        x_aug, y_aug = self.dataset.get_x_y()
        x_aug = self.scaler.transform(x_aug.values)

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
