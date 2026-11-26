import time


class RuntimeTracker:
    def __init__(self, previous=0):
        self.started = time.monotonic()
        self.previous = previous

    def elapsed(self):
        return self.previous + time.monotonic() - self.started
