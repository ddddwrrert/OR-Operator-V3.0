from execution.code_integrator import executable, integrate
from unittest import TestCase


class CodeTest(TestCase):
    def test_preserves_outer_program(self):
        base = "import math\n#EVOLVE_START\na = 1\n#EVOLVE_END\nprint(a)\n"
        changed = integrate(base, "a = 2")
        self.assertIn("import math", changed)
        self.assertIn("print(a)", changed)
        self.assertNotIn("EVOLVE_", executable(changed))
        with self.assertRaises(ValueError):
            integrate(base, "#EVOLVE_END")
