import numpy as np


def get_custom_dataloader(custom_dataloader: str, dataset, model, scaler, custom_args, verbose: int,
                          x: np.ndarray, y: np.ndarray, train: bool, batch_size: int
                          ):
    from mlc.dataloaders.default import DefaultDataLoader
    from mlc.dataloaders.adversarial.madry import MadryATDataLoader
    DATALOADERS = {"madry": (MadryATDataLoader, {"verbose": verbose}), "subset": (DefaultDataLoader, {"subset": 0.1}),
                   "dist": (DefaultDataLoader, {})}

    dataloader = None
    dataloader_call, args = DATALOADERS.get(custom_dataloader, (None, {}))
    if dataloader_call is None:
        return None

    args = {**args, **custom_args, "dataset": dataset, "model": model, "scaler": scaler}
    dataloader = dataloader_call(**args).get_dataloader(x=x, y=y, train=train, batch_size=batch_size)
    return dataloader
