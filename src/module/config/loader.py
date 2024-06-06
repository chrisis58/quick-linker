from abc import ABC, abstractmethod

class ConfigLoader(ABC):

    @abstractmethod
    def load(self, path: str) -> dict[str, any]:
        """
        从外部文件中加载配置项

        :param path: 配置文件的路径
        :return: 配置项字典
        """
        pass

    @abstractmethod
    def get(self, identifier: str, default: any = None) -> any:
        """
        从配置项字典中获取需要的配置

        :param identifier: 配置项标识符
        :param default: 如果没有找到的候补
        :return: 对应的配置项
        """
        pass

