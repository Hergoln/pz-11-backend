import abc

from .event_handler import EventHandler

class Game(metaclass=abc.ABCMeta):
    '''Abstrac class which defines the game.'''

    def __init__(self, game_logic, game_config, communication_handler):
        '''Create instance of game.
        Parameters:
        game_logic: Defines game logic. New class derivered from GameLogic abstract class should be passed here. 
        communication_handler: Handles communication between game and outside enviromment (for example a website or standalone application).
        '''
        self._game_logic = game_logic
        self._game_config = game_config
        self._communication_handler = communication_handler
        self._event_handler = EventHandler(self._game_logic, self._communication_handler)

    @abc.abstractmethod
    def run(self):
        ''''Starts a main loop of game. It's user task to create a loop and define their form 
        (for example, should it be a loop with a constant game step or a turn-based game)'''
        pass