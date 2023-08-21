from abc import ABC

import joblib

from mlc.models.model import Model


class SkModel(Model, ABC):
    def load(self, path: str) -> None:
        n_jobs = self.model.get_params().get("n_jobs")
        self.model = joblib.load(path)
        self.model.set_params(n_jobs=n_jobs)

    def save(self, path: str) -> None:
        joblib.dump(self.model, path, compress=3)
