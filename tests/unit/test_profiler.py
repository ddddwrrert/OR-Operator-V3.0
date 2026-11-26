from tests.support import WithWorkspace


class Profiler(WithWorkspace):
    def test_profiles_inline_and_function_regions(self):
        output = self.profile()
        self.assertIn("<inline>", output["graph"])
        self.assertIn("zip", output["graph"]["predict"])
        self.assertTrue(any(item["kind"] == "iterative-state-update" for item in output["operators"]))
