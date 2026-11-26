from modules.M1_operator_profiler.ast_analyzer import analyze
from modules.M1_operator_profiler.source_parser import parse_source
from unittest import TestCase


class AstTest(TestCase):
    def test_function_calls_do_not_leak_into_module(self):
        src = "#EVOLVE_START\ndef choose(a):\n    return max(a)\nchoose([1])\n#EVOLVE_END\n"
        module, function = analyze(parse_source(src, "solution.py"))
        self.assertEqual(module["calls"], ["choose"])
        self.assertEqual(function["calls"], ["max"])
