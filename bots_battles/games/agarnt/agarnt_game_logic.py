import logging
from game_engine.game_logic import GameLogic


class AgarntGameLogic(GameLogic):
    def process_input(self, message):
        logging.info(f'from agarnt game logic, {message}')

    def get_state(self):
        return ""