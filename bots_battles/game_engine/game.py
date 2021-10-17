import abc

from .event_handler import EventHandler

class Game(metaclass=abc.ABCMeta):

    def __init__(self, game_logic, communication_handler):
        self._game_logic = game_logic
        self._communication_handler = communication_handler
        self._event_handler = EventHandler(self._game_logic, self._communication_handler)

    @abc.abstractmethod
    def run(self):
        pass