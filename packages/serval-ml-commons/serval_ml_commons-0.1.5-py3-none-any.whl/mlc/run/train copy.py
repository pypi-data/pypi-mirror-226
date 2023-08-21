import os
import numpy as np

# from mlc.dataloaders.generative.ddpm import DDPMDataLoader

from mlc.datasets.dataset_factory import load_dataset
from mlc.metrics.compute import compute_metric, compute_metrics
from mlc.metrics.metric_factory import create_metric
from mlc.models.model_factory import load_model
from mlc.transformers.tab_scaler import TabScaler
import torch


models_params = {
    "tabtransformer": {
        "model_name": "TabTransformer",
        "dim": 8,
        "batch_size": 64,
        # "num_classes": 1,
        "depth": 6,
        "heads": 4,
        "weight_decay": -2,
        "learning_rate": -3,
        "dropout": 0.1,
        "data_parallel": False,
    },
    "deepfm": {
        "dnn_dropout": 0.3,
        "num_dense_features": None,
    },
    "torchrln": {
        "n_layers": 5,
        "theta": -12,
        "learning_rate": 0.0005588211696108453,
        "norm": 2,
        "hidden_dim": 78,
    },
}

other = {'depth': 3, 'dim': 32, 'dropout': 0.1, 'heads': 2, 'learning_rate': -3, 'weight_decay': -6}
# other = {'depth': 12, 'dim': 256, 'dropout': 0.3, 'heads': 4, 'learning_rate': -4, 'weight_decay': -2}

def run(
    dataset_name: str = "lcld_201317_ds_time",
    # dataset_name: str = "url",
    model_name: str = "tabtransformer",
) -> None:

    dataset = load_dataset(dataset_name)
    metadata = dataset.get_metadata(only_x=True)
    common_model_params = {
        "x_metadata": metadata,
        "objective": "binary",
        "use_gpu": True,
        "batch_size": 64,
        "num_classes": 2,
        "epochs": 1,
        "early_stopping_rounds": 1,
        "val_batch_size": 1024,
        "class_weight": "balanced",
    }

    x, y = dataset.get_x_y()
    splits = dataset.get_splits()

    x_train = x.iloc[splits["train"]]
    y_train = y[splits["train"]]
    x_test = x.iloc[splits["test"]]
    y_test = y[splits["test"]]
    x_val = x.iloc[splits["val"]]
    y_val = y[splits["val"]]

    x_train = x_train.iloc[:200000]
    y_train = y_train[:200000]
    x_test = x_test.iloc[:50000]
    y_test = y_test[:50000]
    x_val = x_val[:50000]
    y_val = y_val[:50000]
    
    # x_train = x.iloc[:350000]
    # y_train = y[:350000]
    # x_test = x.iloc[400000:]
    # y_test = y[400000:]
    # x_val = x.iloc[350000:400000]
    # y_val = y[350000:400000]

    # {'depth': 12, 'dim': 32, 'dropout': 0.5, 'heads': 2, 'learning_rate': -3, 'weight_decay': -3}
    model_class = load_model(model_name)
    model_params = {**models_params[model_name], **common_model_params}
    
    scaler = TabScaler(num_scaler="min_max", one_hot_encode=True)
    scaler.fit(
        torch.tensor(x.values, dtype=torch.float32), x_type=metadata["type"]
    )

    # model_params = {**models_params[model_name], **common_model_params, **other}
    model = model_class(**model_params, scaler = scaler)
    # scaler = TabScaler(num_scaler="min_max", one_hot_encode=False)
    # scaler.fit(x.values, x_type=metadata["type"])

    # model.set_dataloader(
    #     DDPMDataLoader(original_dataset=dataset)
    # )
    metadata = dataset.get_metadata(only_x=True)
    # {'depth': 12, 'dim': 32, 'dropout': 0.5, 'heads': 2, 'learning_rate': -3, 'weight_decay': -3}
    # model_class = load_model("tabtransformer")
    # model = model_class(
    #     x_metadata=metadata,
    #     objective="binary",
    #     use_gpu=True,
    #     dim=8,
    #     batch_size=64,
    #     num_classes=1,
    #     depth=6,
    #     heads=4,
    #     weight_decay=-2,
    #     learning_rate=-3,
    #     dropout=0.3,
    #     data_parallel=False,
    #     val_batch_size=64,
    #     epochs=5,
    #     model_name="TabTransformer",
    #     # dataset="lcld_v2_iid",
    #     early_stopping_rounds=1,
    # )

   
    # model_class = load_model("deepfm")

    # model = model_class(
    #     x_metadata=metadata,
    #     objective="binary",
    #     use_gpu=False,
    #     batch_size=64,
    #     epochs=1,
    #     early_stopping_rounds=1,
    #     dnn_dropout=0.3,
    #     num_dense_features=None,
    # )

    # model_class = load_model("torchrln")

    # model = model_class(
    #     x_metadata=metadata,
    #     objective="binary",
    #     use_gpu=False,
    #     batch_size=64,
    #     epochs=10,
    #     early_stopping_rounds=2,
    #     num_classes=2,
    #     n_layers=5,
    #     theta=-12,
    #     learning_rate=0.0005588211696108453,
    #     class_weight="balanced",
    #     norm=2,
    #     hidden_dim=78,
    #     scaler=scaler,
    # )

    # model_class = load_model("saint")
    # model = model_class(
    #     objective="binary",
    #     x_metadata=metadata,
    #     batch_size=64,
    #     epochs=1,
    #     early_stopping_rounds=1,
    #     num_classes=1,
    # )

    # model_class = load_model("vime")
    # model = model_class(
    #     objective="binary",
    #     x_metadata=metadata,
    #     batch_size=64,
    #     epochs=1,
    #     early_stopping_rounds=1,
    #     num_classes=1,
    #     device="cuda",
    # )

    # model.set_dataloader(
    #     SemiSupervisedDataLoader(take_amount=1000)
    # )

    # model.fit(
    #     x_train.values,
    #     y_train,
    #     x_val.values,
    #     y_val,
    # )

    # model.fit(
    #     scaler.transform(x_train.values),
    #     # y_train,
    #     np.array([1 - y_train, y_train]).T,
    #     scaler.transform(x_val.values),
    #     # y_val
    #     np.array([1 - y_val, y_val]).T,
    # )
    save_path = "./data/models/lcld_tabtransformer.model"

    model.fit(
        x_train.values,
        # scaler.transform(x_train.values),
        # y_train,
        np.array([1 - y_train, y_train]).T,
        x_val.values,
        # scaler.transform(x_val.values),
        # y_val
        np.array([1 - y_val, y_val]).T,
    )

    model.save(save_path)
    model = model_class.load_class(
        save_path, x_metadata=metadata, scaler=scaler
    )

    metrics = ["auc", "accuracy", "mcc"]
    metrics_obj = [create_metric(m) for m in metrics]
    res = compute_metrics(model, metrics_obj, x_test.values, y_test)

    for i, e in enumerate(metrics):
        print(f"Test {e}: {res[i]}")


if __name__ == "__main__":
    run()
