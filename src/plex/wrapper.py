from typing import Callable


class CallWrapper:
    def __init__(self, func: Callable | str, priority: int = 0):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        if callable(func):
            self.func = wrapper
        else:
            self.func = lambda x: func + ": " + x
        self.priority = priority

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
