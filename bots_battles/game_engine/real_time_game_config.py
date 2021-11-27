from .config_options import IntOption
from .game_config import GameConfig

class RealtimeGameConfig(GameConfig):
    '''Defines real time game config.'''
    def __init__(self):
        super().__init__()
        self._add_option('fps', IntOption("", 30), False)
    