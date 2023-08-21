import torch

from mlc.datasets.dataset_factory import load_dataset
from mlc.metrics.compute import compute_metrics
from mlc.metrics.metric_factory import create_metric
from mlc.models.model_factory import load_model
from mlc.transformers.tab_scaler import TabScaler


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
    "saint": {},
    "vime": {},
}


def run(
    dataset_name: str = "lcld_v2_time",
    model_name: str = "deepfm",
) -> None:

    dataset = load_dataset(dataset_name)
    metadata = dataset.get_metadata(only_x=True)
    common_model_params = {
        "x_metadata": metadata,
        "objective": "classification",
        "use_gpu": True,
        "batch_size": 64,
        "num_classes": 2,
        "epochs": 1,
        "early_stopping_rounds": 5,
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
    x_val = x_val[:1000]
    y_val = y_val[:1000]

    # x_train = x.iloc[:350000]
    # y_train = y[:350000]
    # x_test = x.iloc[400000:]
    # y_test = y[400000:]
    # x_val = x.iloc[350000:400000]
    # y_val = y[350000:400000]

    model_class = load_model(model_name)

    scaler = TabScaler(num_scaler="min_max", one_hot_encode=True)
    scaler.fit(
        torch.tensor(x.values, dtype=torch.float32), x_type=metadata["type"]
    )

    model_params = {
        **models_params[model_name],
        **common_model_params,
    }
    model = model_class(**model_params, scaler=scaler)

    save_path = f"./data/models/{dataset_name}_{model_name}.model"

    model.fit(x_train.values, y_train, x_val.values, y_val)

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
    for e in ["tabtransformer", "deepfm", "torchrln", "saint", "vime"]:
        run(model_name=e)
