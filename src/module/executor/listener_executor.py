from typing import Callable

from src.module.executor.executor import Executor
from src.module.listener.watchdog_listener import WatchdogListener


class ListenerExecutor(Executor):
    def __init__(self, path: str, todo: Callable[[], None]):
        self._todo = todo
        self._path = path
        self._listener = WatchdogListener()

    def execute(self):
        self._listener.listen(self._path, self._todo)