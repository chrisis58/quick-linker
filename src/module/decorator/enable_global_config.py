from dataclasses import asdict, is_dataclass
from typing import Type


from .global_config_strategy import GlobalConfigStrategy

def EnableGlobalConfig(strategy: GlobalConfigStrategy = GlobalConfigStrategy.OVERRIDE):
    def decorator(cls: Type):
        print(f"Decorating class: {cls.__name__}")

        def wrapper_in(*args, **kwargs):
            from src.module.bean import GlobalConfig

            global_config = GlobalConfig()
            if not is_dataclass(global_config):
                raise TypeError("global_config must be a dataclass instance")

            if strategy == GlobalConfigStrategy.OVERRIDE:
                combined_kwargs = {**asdict(global_config), **kwargs}
                return cls(*args, **combined_kwargs)

            elif strategy == GlobalConfigStrategy.EXTEND:
                combined_kwargs = {**kwargs, **asdict(global_config)}
                return cls(*args, **combined_kwargs)

            else:
                raise RuntimeError("strategy not supported!")

        return wrapper_in

    return decorator
