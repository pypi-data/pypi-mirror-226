from typing import List, Optional, Union

import numpy as np
import torch

from mlc.constraints.constraints_backend_executor import ConstraintsExecutor
from mlc.constraints.pytorch_backend import PytorchBackend
from mlc.constraints.relation_constraint import (
    BaseRelationConstraint,
    EqualConstraint,
    Feature,
)
from mlc.constraints.utils import get_feature_index
from mlc.typing import NDFloat
from mlc.utils import to_numpy_number, to_torch_number


class ConstraintsFixer:
    def __init__(
        self,
        guard_constraints: List[BaseRelationConstraint],
        fix_constraints: List[EqualConstraint],
        feature_names: Optional[List[str]] = None,
    ):
        self.guard_constraints = guard_constraints
        self.fix_constraints = fix_constraints
        self.feature_names = feature_names
        for c in self.fix_constraints:
            if not isinstance(c, EqualConstraint):
                raise ValueError("Fix constraints must be an EqualConstraint.")
            else:
                if not isinstance(c.left_operand, Feature):
                    raise ValueError(
                        "Left operand of fix constraints must be a Feature."
                    )

    def fix(
        self, x: Union[torch.Tensor, NDFloat]
    ) -> Union[torch.Tensor, NDFloat]:

        if isinstance(x, np.ndarray):
            return to_numpy_number(self.fix(to_torch_number(x)))

        x = x.clone()

        for i in range(len(self.fix_constraints)):
            guard_c = self.guard_constraints[i]
            fix_c = self.fix_constraints[i]

            if not isinstance(fix_c.left_operand, Feature):
                raise ValueError(
                    "Left operand of fix constraints must be a Feature."
                )

            # Index of inputs that shall be updated
            # according the guard constraints,
            # if none then update all.
            if guard_c is not None:
                executor = ConstraintsExecutor(
                    guard_c, PytorchBackend(), self.feature_names
                )
                to_update = executor.execute(x) > 0
            else:
                to_update = torch.ones(x.shape[0], dtype=torch.bool)

            # Index of the feature to update.
            # Ignore warning, this is checked in the constructor.
            index = get_feature_index(
                self.feature_names, fix_c.left_operand.feature_id
            )

            # Value to be update.
            # Known warning, not supposed to evaluate without constraint.
            executor = ConstraintsExecutor(
                fix_c.right_operand, PytorchBackend(), self.feature_names
            )
            new_value = executor.execute(x[to_update])

            x[to_update, index] = new_value

        return x
