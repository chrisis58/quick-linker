
import yaml

from .loader import ConfigLoader

class YamlLoader(ConfigLoader):

    def __init__(self):
        self._config = dict()

    def load(self, path: str) -> ConfigLoader:
        try:
            with open(path, encoding='utf-8', mode='r') as yml:
                self._config = yaml.load(yml, Loader=yaml.FullLoader)
        except FileNotFoundError:
            print("config file cannot be find!")
        except Exception as e:
            print(e)
        return self

    def get(self, identifier: str, default: any = None) -> any:
        keys = identifier.split('.')
        value = self._config
        try:
            for key in keys:
                value = value.get(key, {})
            return value
        except (KeyError, TypeError):
            return None

