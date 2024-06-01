from typing import Callable

from src.module.executor.executor import Executor

class DisposableExecutor(Executor):

    def __init__(self, job: Callable[[], None]):
        super().__init__()
        self._job = job

    def execute(self):
        self.start()
        self._job()
        del self