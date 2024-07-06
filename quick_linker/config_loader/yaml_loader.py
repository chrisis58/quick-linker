
import yaml

from .loader import ConfigLoader

from quick_linker.decorator import Logger

@Logger
class YamlLoader(ConfigLoader):

    def __init__(self):
        self._config = {}

    def load(self, path: str) -> ConfigLoader:
        self.log.info(f'load config from {path}')
        try:
            with open(path, encoding='utf-8', mode='r') as yml:
                self._config = yaml.load(yml, Loader=yaml.FullLoader)
            self.log.debug(f'config: {self._config}')
        except FileNotFoundError as e:
            self.log.error("config file cannot be found!")
            raise e
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

