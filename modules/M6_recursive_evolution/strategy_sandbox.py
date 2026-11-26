from types import MappingProxyType
from .strategy_compiler import compile_strategy


def sandbox(policy, config):
    # Only validated scalars reach the fixed strategy interpreter.
    return MappingProxyType(compile_strategy(policy, config))
