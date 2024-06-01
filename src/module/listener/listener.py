from abc import abstractmethod, ABC
from typing import Callable

class Listener(ABC):

    @abstractmethod
    def listen(
        self,
        path: str,
        callback: Callable[[None], None]
    ) -> None:
        """
        监听目标路径，如果目标路径有新增文件，则触发回调函数

        :param path: 监听的目标路径
        :param callback: 在目标路径有文件新增时触发的回调函数
        """
        pass



