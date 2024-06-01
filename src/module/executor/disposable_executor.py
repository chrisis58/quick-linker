from typing import Callable

from src.module.executor.executor import Executor

class DisposableExecutor(Executor):

    def __init__(self, todo: Callable[[], None]):
        self._todo = todo

    def execute(self):
        self._todo()
        del self