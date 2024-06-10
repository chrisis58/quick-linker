from abc import ABC, abstractmethod
from threading import Thread


class Executor(ABC, Thread):

    @abstractmethod
    def execute(self) -> None:
        """
        执行交由 Executor 执行的任务
        """
        pass






