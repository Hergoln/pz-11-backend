import logging
import numpy as np
from typing import Dict
from uuid import UUID
from bots_battles.game_engine.game_logic import GameLogic
from .board import Board
from .agarnt_player import AgarntPlayer

class AgarntGameLogic(GameLogic):
    '''
    Defines the logic for Agarnt game.
    '''

    def __init__(self, board: Board):
        self.__board = board
        self.__players = None

    def set_players(self, players: Dict[UUID, AgarntPlayer]):
        self.__players = players

    def process_input(self, player_uuid: str, message: Dict[str, str], delta: float):
        '''
        Process player inputs using game rules.
        '''

        player = self.__players[player_uuid]
        player.update_position(message['directions'], delta)
        
        # foods_to_remove = [f for f in self.__board.foods if np.isclose(f, (player.x, player.y), (player.get_radius(), player.get_radius()))]
        # player.eat_food(len(foods_to_remove))
        # self.__board.foods.remove(foods_to_remove)