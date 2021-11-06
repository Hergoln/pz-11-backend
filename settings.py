from typing import Dict, Tuple, Type
from bots_battles import Game, GameConfig, AgarntGame, AgarntGameConfig
"""This module is a container for every gmae-related settings

    All configurable stuffs should be stored in, e.g., appropriate dictionaries
"""
GAMES: Dict[str, Tuple[Type[Game], Type[GameConfig]]] = {
            'agarnt': (AgarntGame, AgarntGameConfig),
            'placeholder #1': None,
            'placeholder #2': None
            }