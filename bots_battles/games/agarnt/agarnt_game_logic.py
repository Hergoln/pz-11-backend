import logging
import numpy as np
from typing import Dict
from uuid import UUID
from bots_battles.game_engine.game_logic import GameLogic
from .board import Board
from .agarnt_player import AgarntPlayer
from util.math import euclidean_distance

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
        
        try:
            foods_to_remove = [f for f in self.__board.foods if euclidean_distance(f[0], player.x, f[1], player.y) <= player.get_radius()] 
            player.eat_food(len(foods_to_remove))
            for f in foods_to_remove:
                self.__board.foods.remove(f)
        except Exception as e:
            print("FOOD ERROR: ", repr(e))