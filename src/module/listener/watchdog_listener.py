from typing import Callable

from src.module.listener.listener import Listener
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class WatchdogListener(Listener):

    def listen(self,
                path: str,
                callback: Callable[[], None]
    ) -> None:
        observer = Observer()
        observer.schedule(
            WatchdogListener.get_on_add_handler(callback),
            path = path,
            recursive = False
        )
        observer.start()
        try:
            while observer.is_alive():
                observer.join(1)
        finally:
            observer.join()

    @staticmethod
    def get_on_add_handler(on_add: Callable[[], None]) -> FileSystemEventHandler:
        """
        获取文件新增事件的处理器
        :param on_add: 触发文件新增事件的回调函数
        :return: 事件处理器
        """
        class OnAddHandler(FileSystemEventHandler):
            def on_created(self, event):
                if callable(on_add):
                    on_add()

        return OnAddHandler()