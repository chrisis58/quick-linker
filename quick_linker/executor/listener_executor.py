from typing import Callable

from quick_linker.executor.executor import Executor
from quick_linker.listener.watchdog_listener import WatchdogListener


class ListenerExecutor(Executor):
    def __init__(self, job: Callable[[], None], path: str):
        super().__init__()
        self.setDaemon(False)
        self._job = job
        self._path = path
        self._listener = WatchdogListener()

    def execute(self):
        self.start()

    def start(self):
        super().start()
        self._listener.listen(self._path, self._job)

