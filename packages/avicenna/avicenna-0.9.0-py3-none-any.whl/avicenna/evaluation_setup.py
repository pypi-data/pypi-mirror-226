from dataclasses import dataclass
from typing import List, Optional
from abc import ABC, abstractmethod

from isla.solver import ISLaSolver
from sklearn.metrics import confusion_matrix

from avicenna.generator import MutationBasedGenerator
from avicenna.oracle import OracleResult
from avicenna.input import Input


class EvaluationSubject(ABC):
    def __init__(self, grammar, oracle, initial_inputs):
        self.grammar = grammar
        self.oracle = oracle
        self.initial_inputs = initial_inputs

    @staticmethod
    def default_param():
        return {"max_iterations": 10, "timeout": 3600, "log": True}

    def get_evaluation_config(self):
        param = self.default_param().copy()
        param.update(
            {
                "grammar": self.grammar,
                "oracle": self.oracle,
                "initial_inputs": self.initial_inputs,
            }
        )
        return param


@dataclass
class EvaluationResult:
    def __init__(self, subject_name, formula):
        self.subject_name = subject_name
        self.formula = formula
        self.evaluation_data: Optional[List[Input]] = None
        self.precision: float = 0
        self.recall: float = 0


def evaluate_diagnosis(grammar, evaluation_result: EvaluationResult):
    assert evaluation_result.evaluation_data
    y_true = [
        1 if inp.oracle == OracleResult.BUG else 0
        for inp in evaluation_result.evaluation_data
    ]

    solver = ISLaSolver(grammar, formula=evaluation_result.formula)
    y_pred = list()
    for inp in evaluation_result.evaluation_data:
        y_pred.append(int(solver.check(inp.tree)))

    conf_matrix = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = conf_matrix.ravel()
    evaluation_result.precision = tp / (tp + fp)
    evaluation_result.recall = tp / (tp + fn)


def generate_evaluation_data_set(
    grammar, oracle, initial_inputs, targeted_size
) -> List:
    seed_inputs = set()
    for inp in initial_inputs:
        seed_inputs.add(Input.from_str(grammar, inp, None))

    positive_samples = set()
    negative_samples = set()

    i = 0
    while (
        not (
            len(positive_samples) > targeted_size
            and len(negative_samples) > targeted_size
        )
        and i < 200
    ):
        i += 1
        print(len(positive_samples), len(negative_samples))
        mutation_fuzzer = MutationBasedGenerator(
            grammar, oracle=oracle, seed=seed_inputs, yield_negative=True
        )
        result = mutation_fuzzer.generate()
        if result.is_just():
            inp = result.value()
            oracle_result = oracle(inp)
            if oracle_result == OracleResult.BUG:
                positive_samples.add(inp.update_oracle(OracleResult.BUG))
            elif oracle_result == OracleResult.NO_BUG:
                negative_samples.add(inp.update_oracle(OracleResult.NO_BUG))

    return (
        list(positive_samples)[:targeted_size] + list(negative_samples)[:targeted_size]
    )
