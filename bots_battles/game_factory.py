from __future__ import annotations
from typing import Dict, Optional, Tuple, Type
from .game_engine import Game, GameConfig, CommunicationHandler


class GameFactory:
    '''
    Game factory class.
    Can create all available games and return list with names of that games.
    '''
    def __init__(self, games_dict: Dict[str, Tuple[Type[Game], Type[GameConfig]]]):
        '''
        Constructor of GameFactory class.
        To self.__games should be added all available games.
        '''
        self.__games = games_dict

    def get_all_games(self):
        '''
        Returns names of all available games.
        '''

        return self.__games.keys()

    def create_game(self, game_type: str, communication_handler: CommunicationHandler, config: Optional[GameConfig] =None):
        '''
        Creates and returns created game instance.
        If game_type is not recognized, runtime error will be raised.

        Parameters:
        game_type: Name of game. List of available games can be fetched using get_all_games
        method
        communication_handler: CommunicationHandler object.
        config: Game config object. If set to None, default one will be used.
        
        Returns created game instance.
        '''

        if game_type not in self.__games:
            raise RuntimeError("game_type is not recognized")

        config = config if config != None else self.__games[game_type][1]()
        return self.__games[game_type][0](config, communication_handler)

    def get_game_config_class(self, game_type):
        if game_type not in self.__games:
            raise RuntimeError("game_type is not recognized")

        return self.__games[game_type][1]
