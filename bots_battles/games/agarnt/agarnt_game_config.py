from bots_battles.game_engine.config_options import IntOption, StringOption
from bots_battles.game_engine.real_time_game_config import RealtimeGameConfig

class AgarntGameConfig(RealtimeGameConfig):
    '''Defines Agarnt config. Here should store all settings of game (for example speed of game)'''
    def __init__(self):
        super().__init__()
        self._add_option('food_number', IntOption("Number of food to eat", 50, 1), True)
        self._add_option('board_size', IntOption("Board size", 200, 10), True)
        self._add_option('waiting_time', IntOption("After this time without player, session will be closed (in s)", 300, 30, 1500), True)
