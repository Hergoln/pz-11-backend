import abc
from typing import Any
import orjson
from .config_options import *


class GameConfig(metaclass=abc.ABCMeta):
    '''Abstract class, used to define the game config.
    To add new option, method _add_option should be used. 
    GameConfig acts like dict, but with possibility to add new options outside constructor of game config class.
    '''

    def __init__(self):
        '''Constructor of game config class.'''
        self._options = dict()
        self._configurable_options = []

        self._add_option('max_player_number', IntOption('Maximum number of players', 10, 2), True)

    def _add_option(self, name: str, config_option: Option, configurable: bool) ->None:
        '''
        Method used to add option to config.

        Parameters:
        name: Option name, which will be used to get option from config.
        config_option: Instance of Option class.
        configurable: If this flag is set to True, option will be apper in json.
        '''
        self._options[name] = config_option
        if configurable:
            self._configurable_options.append(name)

    def __getitem__(self, property_name: str) ->Any:
        return self._options[property_name].value
    
    def __setitem__(self, property_name: str, value: Any) -> None:
        self._options[property_name].value = value

    def __contains__(self, item: str):
        return item in self._options
        
    def to_json(self) -> str:
        '''Convert config to json'''
        json = dict()
        json['variables'] = dict()

        for name in self._configurable_options:
            json['variables'][name] = self._options[name].to_json()
        return orjson.dumps(json)

    def load_json(self, json: Dict[str, Any]) -> None:
        '''
        Read json dict and update options. 
        Throws RuntimeError when type of option doesn't match or value is invalid
        '''
        for name, prop in json['variables'].items():
            print(prop)
            if name not in self._configurable_options or prop['type'] != self._options[name].type:
                raise RuntimeError("Json config contains invalid option!")
            
            self._options[name].load_json(prop)

