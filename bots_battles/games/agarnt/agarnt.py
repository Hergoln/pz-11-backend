from .agarnt_game_logic import AgarntGameLogic
from game_engine import Game

class AgarntGame(Game):
    def __init__(self, communication_handler):
        Game.__init__(self, AgarntGameLogic(), communication_handler)
        print("Create Agarnt game")

    def run(self):
        print("run agarnt")
        self._event_handler.handleIncomingMessages()