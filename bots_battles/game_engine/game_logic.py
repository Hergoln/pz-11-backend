import abc
import json
from typing import Dict, Set
from websockets.typing import Data

class GameLogic(metaclass=abc.ABCMeta):
    '''Abstract class which defines a rules of game.'''

    @abc.abstractmethod
    def process_input(self, player_uuid: str, message: Dict[str, str], delta: float) -> Set[str]:
        '''Abstract method where message will be parsed and all games rules will be check.'''
        pass
