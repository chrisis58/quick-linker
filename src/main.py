from src.module.linker import QuickLinker
from src.module.bean import QuickLinkerConfig
from src.module.executor import ListenerExecutor, DisposableExecutor

if __name__ == "__main__":
    config = QuickLinkerConfig(
        enable = True,
        exclude = [],
        format = '{name} - S{season}E{episode} - {meta}',
        meta = "[meta]",
        mute = ['.srt'],
        name = "mygo",
        season = 1
    )
    src = r"D:\Documents\temp\quick-linker-test\src\_mygo_sub_en"
    dest = r"D:\Documents\temp\quick-linker-test\dest\_mygo_sub_en"

    linker = QuickLinker(config)

    executor = DisposableExecutor(lambda : linker.ln(src, dest))
    executor.execute()




