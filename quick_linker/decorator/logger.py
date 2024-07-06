import logging
from functools import wraps


def Logger(obj):
    logger_name = f'{obj.__module__}.{obj.__name__}'
    log = logging.getLogger(logger_name)

    if isinstance(obj, type):  # 装饰类
        original_init = obj.__init__

        @wraps(original_init)
        def new_init(self, *args, **kwargs):
            self.log = log
            original_init(self, *args, **kwargs)

        obj.__init__ = new_init
        return obj

    elif callable(obj):  # 装饰函数
        @wraps(obj)
        def wrapper(*args, **kwargs):
            return obj(*args, log=log, **kwargs)
        return wrapper

    else:
        raise TypeError("Logger decorator can only be used on classes or functions.")