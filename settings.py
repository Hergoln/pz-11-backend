from pickle import DICT
from typing import Dict, List, Tuple, Type
from bots_battles import Game, GameConfig, AgarntGame, AgarntGameConfig
"""This module is a container for every game-related settings

    All configurable stuffs should be stored in, e.g., appropriate dictionaries
"""
GAMES: Dict[str, Tuple[Type[Game], Type[GameConfig]]] = {
            'agarnt': (AgarntGame, AgarntGameConfig),
            'placeholder #1': None,
            'placeholder #2': None
            }

"""
    In case new game type has been added to system, this dictionary
    should be updated with all aliases that the game could be 
    addressed with
"""
GAMES_NAMES_MAPPING: Dict[str, List[str]] = {'agarnt': ['agarnt', "agarn't"]}

PREFFERED_WS_PORT = 2137
