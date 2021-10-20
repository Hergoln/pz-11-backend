from .agarnt_game_logic import AgarntGameLogic
from game_engine import Game

class AgarntGame(Game):
    def __init__(self, game_config, communication_handler):
        super().__init__(AgarntGameLogic(), game_config, communication_handler)
        print("Create Agarnt game")

    def run(self):
        print("run agarnt")
        
        while self._is_end():
            self._event_handler.handle_incoming_messages()
            self._event_handler.update_game_state()

    def _is_end(self):
        '''Check if game should end.'''
        return False
            