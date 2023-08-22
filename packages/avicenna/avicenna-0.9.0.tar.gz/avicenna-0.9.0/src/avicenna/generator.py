from typing import Set, Iterable
from abc import ABC, abstractmethod

from islearn.mutation import MutationFuzzer
from isla.fuzzer import GrammarFuzzer
from isla.language import DerivationTree
from isla.solver import ISLaSolver
from fuzzingbook.Grammars import Grammar
from fuzzingbook.GrammarFuzzer import GrammarFuzzer as FuzzingbookGrammarFuzzer

from avicenna.input import Input
from avicenna.helpers import map_to_bool
from avicenna.monads import Maybe, Just, Nothing


class Generator(ABC):
    def __init__(self, grammar: Grammar, **kwargs):
        self.grammar = grammar

    @abstractmethod
    def generate(self, **kwargs) -> Maybe[Input]:
        raise NotImplementedError


class FuzzingbookBasedGenerator(Generator):
    def __init__(self, grammar: Grammar, **kwargs):
        super().__init__(grammar)
        self.fuzzer = FuzzingbookGrammarFuzzer(grammar)

    def generate(self) -> Maybe[Input]:
        return Just(Input(DerivationTree.from_parse_tree(self.fuzzer.fuzz_tree())))


class ISLaGrammarBasedGenerator(Generator):
    def __init__(self, grammar: Grammar, **kwargs):
        super().__init__(grammar)
        self.fuzzer = GrammarFuzzer(grammar)

    def generate(self) -> Maybe[Input]:
        return Just(Input(tree=self.fuzzer.fuzz_tree()))


class ISLaSolverGenerator(Generator):
    def __init__(
        self, grammar: Grammar, constraint, enable_optimized_z3_queries=False, **kwargs
    ):
        super().__init__(grammar)
        self.solver = ISLaSolver(
            grammar,
            constraint,
            max_number_free_instantiations=10,
            max_number_smt_instantiations=10,
            enable_optimized_z3_queries=enable_optimized_z3_queries,
        )

    def generate(self, **kwargs) -> Maybe[Input]:
        try:
            tree = self.solver.solve()
            return Just(Input(tree=tree))
        except (StopIteration, RuntimeError):
            return Nothing()


class MutationBasedGenerator(Generator):
    def __init__(
        self,
        grammar: Grammar,
        oracle,
        seed: Set[Input],
        yield_negative: bool = False,
        **kwargs
    ):
        super().__init__(grammar)
        self.oracle = oracle
        self.seed = [inp.tree for inp in seed]
        self.fuzzer = AvicennaMutationFuzzer(grammar, self.seed, oracle).run(
            yield_negative=yield_negative
        )

    def generate(self, **kwargs) -> Maybe[Input]:
        try:
            return Just(Input(tree=next(self.fuzzer)))
        except StopIteration:
            return Nothing()


class AvicennaMutationFuzzer(MutationFuzzer):
    def __init__(self, grammar: Grammar, seed: Iterable[DerivationTree], oracle):
        super().__init__(grammar, seed)
        self.property = oracle

    def process_new_input(
        self, inp: DerivationTree, extend_fragments: bool = True
    ) -> bool:
        new_coverage = self.coverages_seen - self.coverages_of(inp)
        if (
            inp in self.population
            or not map_to_bool(self.property(inp))
            or not new_coverage
        ):
            return False

        self.coverages_seen.update(new_coverage)
        self.population.add(inp)
        if extend_fragments:
            self.update_fragments(inp)

        return True
