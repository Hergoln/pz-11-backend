import logging
from bots_battles.game_engine.game_logic import GameLogic

class AgarntGameLogic(GameLogic):
    def process_input(self, message:str):
        logging.info(f'from agarnt game logic, {message}')

    def get_state(self):
        return ""