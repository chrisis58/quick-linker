from src.module.decorator import Singleton
from src.module.bean.quick_linker_config import QuickLinkerConfig

@Singleton
class GlobalConfigurer:
    """
    singleton configurer
    """

    def __init__(self):
        self._global_config = {}

    def set_global_config(self, **kwargs):
        self._global_config = kwargs

    def get_config_instance(self, cls, **kwargs):
        return cls(**{**self._global_config, **kwargs})



