from .agarnt_game_logic import AgarntGameLogic
from game_engine import Game

class AgarntGame(Game):
    def __init__(self, game_config, communication_handler):
        Game.__init__(self, AgarntGameLogic(), game_config, communication_handler)
        print("Create Agarnt game")

    def run(self):
        print("run agarnt")
        
        while self._isEnd():
            self._event_handler.handleIncomingMessages()
            self._event_handler.updateGameState()

    def _isEnd(self):
        '''Check if game should end.'''
        return False
            