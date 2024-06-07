from src.module.config import YamlLoader
from src.module.linker import QuickLinker
from src.module.bean import QuickLinkerConfig, GlobalConfig
from src.module.executor import ExecutorFactory

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
    executor.execute()

    executor.join()




