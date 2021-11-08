import logging
import numpy as np
from typing import Dict
from uuid import UUID
from bots_battles.game_engine.game_logic import GameLogic
from .board import Board
from .player import Player

class AgarntGameLogic(GameLogic):
    def __init__(self, board: Board, players: Dict[UUID, Player]):
        self.__board = board
        self.__players = players

    def process_input(self, player_uuid: str, message: Dict[str, str]):
        player = self.__players[player_uuid]
        player.update_position(message['dir'])
        
        foods_to_remove = [f for f in self.__board if np.isclose(f, (player.x, player.y), (player.get_radius(), player.get_radius()))]
        player.eated_food(len(foods_to_remove))
        self.__board.foods.remove(foods_to_remove)
        

        logging.info(f'from agarnt game logic, {message}')