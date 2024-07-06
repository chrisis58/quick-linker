import logging

def get_logger_level(name: str) -> int:
    """
    获取日志级别

    :param name: 日志级别名称
    :return: 日志级别
    """
    return getattr(logging, name.upper())


def init_logger():
    """
    配置日志

    :param logger: 日志对象
    :param level: 日志级别
    :param filename: 日志文件名
    """
    from quick_linker.config import LoggerConfig

    # 配置日志记录
    handler = [logging.StreamHandler()]
    if LoggerConfig().filename:
        handler.append(logging.FileHandler(LoggerConfig().filename))

    logging.basicConfig(
        level = get_logger_level(LoggerConfig().level),
        format = '%(asctime)s  %(levelname)s --- [%(threadName)s (%(thread)d)] %(name)s : %(message)s',
        handlers = handler
    )
