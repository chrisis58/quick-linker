from quick_linker.config import YamlLoader
from quick_linker.linker import QuickLinker
from quick_linker.bean import QuickLinkerConfig, GlobalConfig
from quick_linker.executor import ExecutorFactory

if __name__ == "__main__":

    config = YamlLoader().load("../config.yml")

    GlobalConfig(**config.get("config.global"))

    linker = QuickLinker(QuickLinkerConfig(**config.get("tasks.mushoku.rename")))
    src = config.get("tasks.mushoku.src")
    dest = config.get("tasks.mushoku.dest")

    executor = ExecutorFactory.create_executor(
        ExecutorFactory.ExecutorType.LISTENER,
        lambda: linker.ln(src, dest),
        path = src
    )
    
    try:
        executor.execute()
        executor.join()
    except InterruptedError:
        print("process terminalted")




