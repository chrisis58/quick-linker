import unittest

from quick_linker.config_loader import YamlLoader
from quick_linker.config import GlobalConfig, LoggerConfig
from quick_linker.utils import logger_util


class MyTestCase(unittest.TestCase):
    def test_something(self):
        config = YamlLoader().load('D:\Documents\pypyppy\quick-linker\config.yml')

        # 初始化全局配置和日志配置
        GlobalConfig(**config.get("config.global"))
        print('loading logger config in test')
        LoggerConfig(**config.get("config.logger"))
        
        logger_util.init_logger() 
        
        assert LoggerConfig().level.upper() == 'INFO' 


if __name__ == '__main__':
    unittest.main()


