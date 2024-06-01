from dataclasses import dataclass

@dataclass
class QuickLinkerConfig:
    """
    QuickLinker 的配置数据类
    """


    enable: bool
    """
    是否启用重命名
    """

    name: str
    """
    节目的名字
    """

    season: int
    """
    节目所属的季数
    """

    meta: str
    """
    剧集的元信息
    """

    mute: list[str]
    """
    在剧集集数抽取时忽略的字符串。
    例如： 
    'Urusei Yatsura 2022 [01].mkv' --mute('2022')--> 'Urusei Yatsura [01].mkv'
    """

    exclude: list[str]
    """
    在剧集集数抽取时，忽略不需要的文件
    """

    format: str
    """
    重命名格式，默认为 `{name} - S{season}E{episode} - {meta}`
    """
