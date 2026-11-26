from evaluation.statistical_test import two_sided_sign_test
from modules.M4_operator_validation.static_checker import check_scope
from unittest import TestCase


class ValidationTest(TestCase):
    def test_rejects_outside_edit_and_reports_small_sample(self):
        source = "x = 1\n#EVOLVE_START\na = 1\n#EVOLVE_END\n"
        check_scope(source, source.replace("a = 1", "a = 2"))
        with self.assertRaises(ValueError):
            check_scope(source, source.replace("x = 1", "x = 2"))
        self.assertEqual(two_sided_sign_test([1, 1, 1]), 0.25)
