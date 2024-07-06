import argparse

import logging

from quick_linker.config import GlobalConfig, LoggerConfig
from quick_linker.utils.logger_util import init_logger
from quick_linker.executor import ExecutorFactory
from quick_linker.config_loader import YamlLoader
from quick_linker.linker import QuickLinker
from quick_linker.bean import QuickLinkerConfig


# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser(description="Quick Linker Script")
# 添加 -c/--config 参数
parser.add_argument("-c", "--config", help="Specify the path to the configuration file", required=True)
# 解析命令行参数
args = parser.parse_args()

try:
    # 加载配置文件
    config = YamlLoader().load(args.config)

    # 初始化全局配置和日志配置
    GlobalConfig(**config.get("config.global"))
    LoggerConfig(**config.get("config.logger"))

    init_logger()    
    
except Exception as e:
    print(e)
    print("script exiting")
    exit(1)

log = logging.getLogger(f'{__name__}')

log.info("script started")

tasks = config.get("tasks")
if tasks is None:
    print("no tasks found")
    exit(1)


src = config.get("tasks.mushoku.src")
dest = config.get("tasks.mushoku.dest")
linker = QuickLinker(QuickLinkerConfig(**config.get("tasks.mushoku.rename")))

executor = ExecutorFactory.create_executor(
    ExecutorFactory.ExecutorType.DISPOSABLE,
    lambda: linker.ln(src, dest),
    path = src
)

try:
    executor.execute()
    executor.join()
except InterruptedError:
    print("process terminalted")




