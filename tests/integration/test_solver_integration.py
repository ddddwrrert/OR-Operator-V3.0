import shutil
from execution.code_workspace import write_candidate
from execution.compiler import check
from tests.support import WithWorkspace


class SolverTest(WithWorkspace):
    def test_demo_runs_in_child_process(self):
        item = write_candidate(self.work, "000000", self.solver.program, self.solver.baseline)
        score = self.solver.evaluate(item, 11)
        self.assertTrue(score.valid)
        self.assertGreater(score.metrics["mse"], 0)

    def test_cpp_is_actually_compiled_and_rejects_errors(self):
        compiler = shutil.which("g++")
        if not compiler:
            self.skipTest("g++ is not installed")
        path = self.work / "solution.cpp"
        path.write_text("#EVOLVE_START\nint main(){return 0;}\n#EVOLVE_END\n", encoding="utf-8")
        check(path, compiler=compiler)
        path.write_text("#EVOLVE_START\nint main( {\n#EVOLVE_END\n", encoding="utf-8")
        with self.assertRaises(RuntimeError):
            check(path, compiler=compiler)
