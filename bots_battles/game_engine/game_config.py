import abc
import orjson
from .config_options import *


class GameConfig(metaclass=abc.ABCMeta):
    '''Abstract class, used to define the game config.'''
    def __init__(self):
        self._options = dict()
        self._configurable_options = []

        self._add_option('max_player_number', IntOption('Maximum number of players', 10, 2), True)

    def _add_option(self, name: str, config_option: Option, configurable: bool):
        self._options[name] = config_option
        if configurable:
            self._configurable_options.append(name)

    def __getitem__(self, property_name: str):
        return self._options[property_name].value

    def to_json(self):
        json = dict()
        json['variables'] = dict()

        for name in self._configurable_options:
            json['variables'][name] = self._options[name].to_json()
        return orjson.dumps(json)

    def load_json(self, json: str):
        for name, prop in json['variables'].items():
            print(prop)
            if name not in self._configurable_options or prop['type'] != self._options[name].type:
                raise RuntimeError("Json config contains invalid option!")
            
            self._options[name].load_json(prop)

