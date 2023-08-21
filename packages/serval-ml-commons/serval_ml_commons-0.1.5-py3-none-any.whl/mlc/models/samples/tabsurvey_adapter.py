from typing import Any, Dict

from tabsurvey.models import str2model

from mlc.models.model import Model
from mlc.utils import dict2obj


class TabsurveyAdapter(Model):
    def __init__(
        self, tabsurvey_model_name: str, **kwargs: Dict[str, Any]
    ) -> None:

        self.name = tabsurvey_model_name
        self.objective = kwargs["objective"]
        self.constructor_kwargs = kwargs
        args = dict2obj(kwargs)
        params = kwargs

        super().__init__(
            name=self.name, tabsurvey_model_name=tabsurvey_model_name, **kwargs
        )

        self.model = str2model(tabsurvey_model_name)(args=args, params=params)

    def save(self, path: str) -> None:
        pass

    def load(self, path: str) -> None:
        pass


models = [
    ("tabsurvey_adapter", TabsurveyAdapter),
]
