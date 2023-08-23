from abc import ABC, abstractmethod
from typing import Any

import jijmodeling as jm
import numpy as np
from dimod import (
    BinaryQuadraticModel,
    ConstrainedQuadraticModel,
    DiscreteQuadraticModel,
)

from strangeworks_optimization_models.problem_models import StrangeworksModelType


class StrangeworksConverter(ABC):
    model: Any
    model_type: StrangeworksModelType
    model_options: dict | None = None
    strangeworks_parameters: dict | None = None

    @staticmethod
    @abstractmethod
    def convert(
        model: Any,
    ) -> (
        BinaryQuadraticModel | ConstrainedQuadraticModel | DiscreteQuadraticModel | jm.Problem | np.ndarray | dict | str
    ):
        ...


class StrangeworksBinaryQuadraticModel_JiJProblem(StrangeworksConverter):
    def __init__(self, model: BinaryQuadraticModel):
        self.model = model
        self.model_type = StrangeworksModelType.BinaryQuadraticModel

    def convert(self) -> jm.Problem:
        Q = jm.Placeholder("Q", ndim=2)  # Define variable d
        Q.len_at(0, latex="N")  # Set latex expression of the length of d
        x = jm.BinaryVar("x", shape=(Q.shape[0],))  # Define binary variable
        i = jm.Element("i", belong_to=(0, Q.shape[0]))  # Define dummy index in summation
        j = jm.Element("j", belong_to=(0, Q.shape[1]))  # Define dummy index in summation
        problem = jm.Problem("simple QUBO problem")  # Create problem instance
        problem += jm.sum(i, jm.sum(j, Q[i, j] * x[i] * x[j]))  # Add objective function

        qubo = self.model.to_qubo()

        Qmat = np.zeros((self.model.num_variables, self.model.num_variables))
        for k, v in qubo[0].items():
            Qmat[k[0] - 1, k[1] - 1] = v

        feed_dict = {"Q": Qmat}
        return problem, feed_dict


class StrangeworksConverterFactory:
    @staticmethod
    def from_model(model_from: Any, model_to: Any) -> StrangeworksConverter:
        if isinstance(model_from, BinaryQuadraticModel) and model_to == jm.Problem:
            return StrangeworksBinaryQuadraticModel_JiJProblem(model=model_from)
        elif isinstance(model_from, jm.Problem) and model_to == BinaryQuadraticModel:
            # TODO: Implement
            pass
        else:
            raise ValueError("Unsupported model type")
