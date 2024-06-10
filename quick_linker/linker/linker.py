from abc import abstractmethod, ABC

class Linker(ABC):

    @abstractmethod
    def ln(
        self,
        src: str,
        dest: str
    ) -> None:
        """
        根据传入的源路径与目标路径进行硬链接

        :param src: 等待进行链接的路径
        :param dest: 链接的目标路径
        """
        pass



