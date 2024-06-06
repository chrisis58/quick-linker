from src.module.decorator import Singleton
from typing import Type, TypeVar

T = TypeVar('T')

@Singleton
class GlobalConfigurer:
    """
    singleton global configurer
    """

    def __init__(self):
        self._global_config = {}

    def set_global_config(self, **kwargs):
        self._global_config = kwargs

    def get_config_instance(self, cls: Type[T], **kwargs) -> T:
        """
        获取配置数据类实例，缺省的项以全局为准

        :param cls: 要新建的配置数据类
        :param kwargs: 传入的配置项
        :return: 配置数据实例
        """
        return cls(**{**self._global_config, **kwargs})



