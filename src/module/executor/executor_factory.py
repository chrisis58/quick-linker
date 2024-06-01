from enum import Enum
from typing import Callable

from .executor import Executor
from .listener_executor import ListenerExecutor
from .disposable_executor import DisposableExecutor


class ExecutorFactory:
    """"
    Executor 工厂类，用于创建 Executor 实例
    """
    def __init__(self):
        pass

    class ExecutorType(Enum):
        DISPOSABLE = 1
        LISTENER = 2

    @staticmethod
    def create_executor(
        executor_type: ExecutorType,
        job: Callable[[], None],
        **kwargs
    ) -> Executor:
        """
        获取 Executor 实例

        :param executor_type:
        :param job: 交由 Executor 办的任务
        :param kwargs: 具体实现类的额外配置
        :return: Executor 实例
        """
        if executor_type == ExecutorFactory.ExecutorType.DISPOSABLE:
            return DisposableExecutor(job)
        elif executor_type == ExecutorFactory.ExecutorType.LISTENER:
            return ListenerExecutor(job, **kwargs)