from enum import Enum
from typing import Callable, TypeVar

V = TypeVar("V")

class GlobalConfigStrategy(Enum):
    """
    子配置项的全局配置策略， 值为对应的冲突解决方法
    """


    OVERRIDE: Callable[[V, V], V] = lambda _, i: i
    """
    忽略旧值，总是使用新值
    """

    EXTEND: Callable[[V, V], V] = lambda a, b: a + b if isinstance(a, list) else b
    """
    检查值是否为列表，如果是，就将它们合并；如果不是列表，就使用新值
    """