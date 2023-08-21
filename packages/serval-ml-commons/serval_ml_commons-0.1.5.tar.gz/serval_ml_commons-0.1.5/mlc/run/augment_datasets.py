import os
import sys

sys.path.append(".")
from mlc.logging import XP

import torch

from argparse import ArgumentParser, Namespace
from mlc.datasets.dataset_factory import load_dataset

from mlc.dataloaders.generative.ctgan import CTGANDataLoader
# from mlc.dataloaders.generative.ddpm import DDPMDataLoader
from mlc.transformers.tab_scaler import TabScaler

AUGMENTATIONS = {"ctgan": CTGANDataLoader}  # , "ddpm": DDPMDataLoader}


def run(augmentation_name, dataset_name, model_name, train_batch_size=32,train_generator_epochs=50, debug=0):
    dataset = load_dataset(dataset_name)
    metadata = dataset.get_metadata(only_x=True)
    x, y = dataset.get_x_y()

    scaler = TabScaler(num_scaler="min_max", one_hot_encode=True)
    scaler.fit(
        torch.tensor(x.values, dtype=torch.float32), x_type=metadata["type"]
    )
    filter_constraints = False
    path = "../models/mlc/data_augmentation"
    save_path = os.path.join(path, f"{dataset_name}_{augmentation_name}.pt")
    pretrained_path = save_path if os.path.exists(save_path) else None
    os.makedirs(path, exist_ok=True)

    experiment = XP(dict(dataset=dataset_name, model_name=model_name), project_name="DataAugment")
    augmentation = AUGMENTATIONS[augmentation_name](original_dataset=dataset, scaler=scaler,
                                                    pretrained_path=pretrained_path, save_path=save_path,
                                                    filter_constraints=filter_constraints,
                                                    train_batch_size=train_batch_size,
                                                    generator_epochs=train_generator_epochs,
                                                    verbose=debug, subset=10000 if debug else 0)

    augmented_loader = augmentation.get_dataloader(x, y, train=True, batch_size=train_batch_size, augment=False)
    experiment.log_parameters({"size_trainining": len(augmented_loader)})

    for batch in augmented_loader:
        print(batch)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Training with Hyper-parameter optimization"
    )
    parser.add_argument("--dataset_name", type=str, default="lcld_v2_iid",
                        )
    parser.add_argument("--augmentation_name", type=str, default="ctgan",
                        )
    parser.add_argument("--model_name", type=str, default="tabtransformer",
                        )

    parser.add_argument("--train_batch_size", type=int, default=1024)

    parser.add_argument("--train_generator_epochs", type=int, default=500)

    parser.add_argument("--debug", type=int, default=0)

    args = parser.parse_args()

    run(augmentation_name=args.augmentation_name, dataset_name=args.dataset_name, model_name=args.model_name,
        train_batch_size=args.train_batch_size,train_generator_epochs=args.train_generator_epochs, debug=args.debug)
