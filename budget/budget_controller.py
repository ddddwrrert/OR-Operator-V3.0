from .budget_allocator import allows
from .evaluation_budget import remaining
from .runtime_tracker import RuntimeTracker


class BudgetError(RuntimeError):
    pass


class Budget:
    def __init__(self, limits, state, save):
        self.limits = limits
        self.state = state
        self.save = save
        self.counts = state.setdefault("budget", {})
        if any(not isinstance(value, (int, float)) or value < 0 for value in limits.values()):
            raise ValueError("Budget limits must be nonnegative numbers")
        self.clock = RuntimeTracker(state.get("runtime_seconds", 0))

    def reserve(self, key, amount=1):
        self.check_time()
        if not allows(self.limits, self.counts, key, amount):
            raise BudgetError(f"{key} budget exhausted")
        self.counts[key] = self.counts.get(key, 0) + amount
        self.checkpoint()

    def check_time(self):
        if self.clock.elapsed() >= self.limits["runtime_seconds"]:
            raise BudgetError("Runtime budget exhausted")

    def remaining_evaluations(self):
        return remaining(self.counts, self.limits)

    def checkpoint(self):
        self.state["runtime_seconds"] = self.clock.elapsed()
        self.save()
