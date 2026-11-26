from execution.compiler import check


class CppSolverAdapter:
    def __init__(self, compiler, timeout, sandbox_prefix):
        self.compiler = compiler
        self.timeout = timeout
        self.sandbox_prefix = sandbox_prefix

    def check(self, source):
        check(source, compiler=self.compiler, timeout=self.timeout, prefix=self.sandbox_prefix)
