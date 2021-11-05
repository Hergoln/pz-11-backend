from typing import Dict, Tuple, Type
from bots_battles import Game, GameConfig, AgarntGame, AgarntGameConfig

GAMES: Dict[str, Tuple[Type[Game], Type[GameConfig]]] = {
            'agarnt': (AgarntGame, AgarntGameConfig),
            'placeholder #1': None,
            'placeholder #2': None
            }