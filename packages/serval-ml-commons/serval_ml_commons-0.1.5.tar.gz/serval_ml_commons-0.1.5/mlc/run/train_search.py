import os
import sys

sys.path.append(".")
from mlc.logging import XP

import torch
import optuna
from optuna.trial import TrialState
from optuna._callbacks import MaxTrialsCallback
from mlc.datasets.dataset_factory import load_dataset
from mlc.models.model_factory import load_model
from mlc.utils import cross_validation
from mlc.load_do_save import save_json
from mlc.utils import parent_exists
from argparse import Namespace, ArgumentParser
from mlc.transformers.tab_scaler import TabScaler
from mlc.metrics.compute import compute_metric
from mlc.metrics.metric_factory import create_metric
from mlc.dataloaders import get_custom_dataloader

# Torch config to avoid crash on HPC
torch.multiprocessing.set_sharing_strategy('file_system')



class Objective(object):
    def __init__(self, args, model_class, scaler, X, y):
        # Save the model that will be trained
        self.model_class = model_class

        # Save the trainings data
        self.X = X
        self.y = y
        self.scaler = scaler

        self.args = args

    def __call__(self, trial):
        # Define hyperparameters to optimize
        trial_params = self.model_class.define_trial_parameters(trial, self.args)

        # Create model
        args = {**self.args, **trial_params, "task": "HP train", "trial": trial.number}

        model = self.model_class(**args, scaler=self.scaler)
        args = Namespace(**args)

        # Cross validate the chosen hyperparameters
        metric = args.metrics[0]
        metrics, time = cross_validation(model, self.X, self.y, metric, args)

        experiment = XP(vars(args))
        save_path = f"./tmp/models/{args.dataset}_{args.model_name}.model"
        model.save(save_path)
        experiment.log_model(f"{args.dataset}_{args.model_name}.model", save_path)
        experiment.log_metric(metric, metrics.mean())
        experiment.end()

        return metrics.mean()


def run(dataset_name: str = "lcld_v2_iid", model_name: str = "tabtransformer", n_trials: int = 100, subset: int = 1000,
        train_batch_size: int = 256, val_batch_size: int = 1024, save_best_model: int = 0, epochs: int = 100,
        custom_dataloader:str="") -> None:
    print("Train hyperparameter optimization for {} on {}".format(model_name, dataset_name))
    dataset = load_dataset(dataset_name)
    metadata = dataset.get_metadata(only_x=True)
    common_model_params = {
        "x_metadata": metadata,
        "objective": "classification",
        "use_gpu": True,
        "batch_size": train_batch_size,
        "num_classes": 2,
        "early_stopping_rounds": 5,
        "val_batch_size": val_batch_size,
        "class_weight": "balanced",
        "custom_dataloader":custom_dataloader
    }

    x, y = dataset.get_x_y()
    splits = dataset.get_splits()

    x_train = x.iloc[splits["train"]]
    y_train = y[splits["train"]]

    if subset > 0:
        x_train = x_train[:subset]
        y_train = y_train[:subset]

    model_class = load_model(model_name)
    args = {
        **common_model_params,
        "depth": 12,
        "heads": 2,  # 4,
        "weight_decay": -3,  # -2,
        "learning_rate": -3,  # -2,
        "dropout": 0.5,  # 0.3,
        "data_parallel": False,
        "epochs": epochs,
        "model_name": model_name,
        "dataset": dataset_name,
        "early_stopping_rounds": 5,
        "num_splits": 5,
        "seed": 42,
        "shuffle": True,
        "metrics": ["auc"]
    }
    if model_name == "torchrln":
        args["weight_decay"] = 0

    study_name = model_name + "_" + dataset_name
    storage_name = "sqlite:///{}.db".format(study_name)

    study = optuna.create_study(direction="maximize",
                                study_name=study_name,
                                storage=storage_name,
                                load_if_exists=True)

    n_completed = len(study.get_trials(states=(TrialState.COMPLETE,)))
    n_to_finish = n_trials
    print(f"{n_completed}/{n_trials} already completed")

    scaler = TabScaler(num_scaler="min_max", one_hot_encode=True)
    scaler.fit(
        torch.tensor(x.values, dtype=torch.float32), x_type=metadata["type"]
    )

    if n_completed < n_to_finish:
        study.optimize(
            Objective(args, model_class, scaler, x_train.to_numpy(), y_train),
            n_trials=None,
            callbacks=[
                MaxTrialsCallback(
                    n_to_finish,
                    states=(TrialState.COMPLETE,),
                ),
            ],
        )

    save_path = os.path.join(".", "data", "models", "{}.model".format(model_name), "best_args.json")
    best_args = {**args, **study.best_trial.params, "task": "HP train", "trial": "best"}
    best_args["x_metadata"] = None
    experiment = XP(best_args)
    experiment.log_metrics({"best_{}".format(args.get("metrics")[0]): study.best_value})

    save_json(best_args, parent_exists(save_path))
    print(f"Best parameters: {best_args} with best performance: {study.best_value}")

    if save_best_model:
        best_trial = sorted(study.trials,key=lambda d: d.value if d.values is not None else -1)[-1]
        print(f"Best trial parameters: {best_trial.params} with best performance: {best_trial.value}")
        model = model_class(**{**args,**best_trial.params, "early_stopping_rounds":args["epochs"]}, scaler=scaler)
        x_test = x.iloc[splits["test"]]
        y_test = y[splits["test"]]

        custom_train_dataloader = get_custom_dataloader(custom_dataloader, dataset,model, scaler,{},
                                                        x=x_train.values,y=y_train, train=True, batch_size=train_batch_size)
        model.fit(x_train,y_train,x_test,y_test, custom_train_dataloader=custom_train_dataloader)

        sc = create_metric("auc")
        metric_val = compute_metric(model, sc, x_test, y_test)
        print(metric_val)
        experiment.log_metric("test_{}".format(sc.metric_name), metric_val)

        save_path = os.path.join(".", "data", "models", "best_{}_{}_{}.model".format(model_name,dataset_name,
                                                                                     custom_dataloader))
        model.save(save_path)
        experiment.log_model("best_{}_{}_{}.model".format(model_name,dataset_name,custom_dataloader),save_path)

if __name__ == "__main__":
    parser = ArgumentParser(
        description="Training with Hyper-parameter optimization"
    )
    parser.add_argument("--dataset_name", type=str, default="lcld_v2_iid",
                        )
    parser.add_argument("--model_name", type=str, default="tabtransformer",
                        )
    parser.add_argument("--n_trials", type=int, default=100)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--subset", type=int, default=0)
    parser.add_argument("--train_batch_size", type=int, default=1024)
    parser.add_argument("--val_batch_size", type=int, default=2048)
    parser.add_argument("--save_best_model", type=int, default=1)
    parser.add_argument("--custom_dataloader", type=str, default="")

    args = parser.parse_args()

    run(dataset_name=args.dataset_name, model_name=args.model_name, n_trials=args.n_trials, subset=args.subset,
        train_batch_size=args.train_batch_size, val_batch_size=args.val_batch_size,
        save_best_model=args.save_best_model,
        epochs=args.epochs,custom_dataloader=args.custom_dataloader)
