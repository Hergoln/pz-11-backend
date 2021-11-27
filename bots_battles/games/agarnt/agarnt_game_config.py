from bots_battles.game_engine.config_options import StringOption
from bots_battles.game_engine.real_time_game_config import RealtimeGameConfig

class AgarntGameConfig(RealtimeGameConfig):
    '''Defines Agarnt config. Here should store all settings of game (for example speed of game)'''
    def __init__(self):
        super().__init__()
