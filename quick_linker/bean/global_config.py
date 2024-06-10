from dataclasses import dataclass, field

from quick_linker.decorator import Singleton

@Singleton
@dataclass
class GlobalConfig:
    """
    全局配置项
    """

    mute: list[str] = field(default_factory=list)
    """
    解析文件名时忽略的子串
    
    >> 'abc' --mute('b')--> 'ac'
    """

    exclude: list[str] = field(default_factory=list)
    """
    文件名包含此项的文件不参与解析
    """

    format: str = ""
    """
    最终重命名文件的格式，默认为 '{name} - S{season}E{episode} - {meta}'
    """
