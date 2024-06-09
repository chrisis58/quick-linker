
import yaml

from .loader import ConfigLoader
from src.module.decorator import Logger

@Logger
class YamlLoader(ConfigLoader):

    def __init__(self):
        self._config = dict()

    def load(self, path: str) -> ConfigLoader:
        self.log.info(f'load config from {path}')
        try:
            with open(path, encoding='utf-8', mode='r') as yml:
                self._config = yaml.load(yml, Loader=yaml.FullLoader)
        except FileNotFoundError:
            self.log.warn("config file cannot be found!")
        except Exception as e:
            print(e)
        return self

    def get(self, identifier: str, default: any = None) -> any:
        keys = identifier.split('.')
        value = self._config
        try:
            for key in keys:
                value = value.get(key, {})
            self.log.debug(f'get {identifier}: {value}')
            return value
        except (KeyError, TypeError):
            return None

