import abc

from websockets.typing import Data

class GameLogic(metaclass=abc.ABCMeta):
    '''Abstract class which defines a rules of game.'''

    @abc.abstractmethod
    def process_input(self, message: Data):
        '''Abstract method where message will be parsed and all games rules will be check.'''
        pass

    @abc.abstractmethod
    def get_state(self):
        '''Returns actual state of game'''
        pass
