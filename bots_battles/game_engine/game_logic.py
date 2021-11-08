import abc
from typing import Dict
from websockets.typing import Data

class GameLogic(metaclass=abc.ABCMeta):
    '''Abstract class which defines a rules of game.'''

    @abc.abstractmethod
    def process_input(self, player_uuid: str, message: str):
        '''Abstract method where message will be parsed and all games rules will be check.'''
        pass

    @abc.abstractmethod
    def get_state(self):
        '''Returns actual state of game'''
        pass
