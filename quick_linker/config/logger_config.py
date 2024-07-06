from dataclasses import dataclass

from quick_linker.decorator import Singleton

@Singleton
@dataclass
class LoggerConfig:
    """
    日志配置项
    """

    level: str = "DEBUG"
    """
    日志级别
    """

    filename: str = None
    """
    日志文件名，如果为空则不输出到文件
    """
