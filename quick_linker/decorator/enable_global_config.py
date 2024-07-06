from dataclasses import asdict, is_dataclass
from typing import Type

from quick_linker.utils import combine_dicts

from .global_config_strategy import GlobalConfigStrategy

def EnableGlobalConfig(strategy: GlobalConfigStrategy = GlobalConfigStrategy.OVERRIDE):
    def decorator(cls: Type):
        def wrapper_in(*args, **kwargs):
            from quick_linker.config import GlobalConfig

            global_config = GlobalConfig()
            if not is_dataclass(global_config):
                raise TypeError("global_config must be a dataclass instance")

            try:
                combined_dict = combine_dicts(
                    asdict(global_config), kwargs,
                    conflict_handler = strategy
                )
                return cls(*args, **combined_dict)
            except:
                raise RuntimeError("strategy not supported!")

        return wrapper_in

    return decorator
