import logging
from functools import wraps

# 配置日志记录
logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s  %(levelname)s --- [%(threadName)s (%(thread)d)] %(name)s : %(message)s',
    handlers = [
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)


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