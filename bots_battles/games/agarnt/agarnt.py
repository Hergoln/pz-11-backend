from __future__ import annotations
import asyncio
import logging
import orjson
from typing import Dict
from uuid import UUID
import random

from .agarnt_game_logic import AgarntGameLogic
from .agarnt_game_config import AgarntGameConfig
from .agarnt_player import AgarntPlayer
from .board import Board
from bots_battles.game_engine import RealtimeGame, CommunicationHandler
from util.math import euclidean_distance

class AgarntGame(RealtimeGame):
    instance_counter = 0

    def __init__(self, game_config: AgarntGameConfig, communication_handler: CommunicationHandler):
        self.__n_digits = 3

        self.__board = Board(game_config['food_number'], (game_config['board_size'], game_config['board_size']))
        super().__init__(AgarntGameLogic(self.__board), game_config, communication_handler)
        self._game_logic.set_players(self._players)

        AgarntGame.instance_counter = AgarntGame.instance_counter + 1
        self.object_counter = AgarntGame.instance_counter

        logging.info(f'create Agarnt game {self.object_counter}')
        

    def add_player(self, player_uuid: UUID, player_name: str):
        x, y = self.__generate_random_position()
        self._players[player_uuid] = AgarntPlayer(player_name, player_uuid, (x, y))
    
    def __get_common_state_part(self, n_digits):
        state = dict()
        state['b'] = self.__board.max_size
        state['f'] = self.__board.foods
        return state


    def get_state_for_player(self, player_uuid: UUID):
        current_player = self._players[player_uuid]
        state = self.__get_common_state_part(self.__n_digits)

        state['p'] = {'x': round(current_player.x, self.__n_digits), 'y': round(current_player.y, self.__n_digits), 'r': round(current_player.radius, self.__n_digits)}
        state['ps'] = [{'n': player.player_name, 'x': round(player.x, self.__n_digits), 'y': round(player.y, self.__n_digits), 'r': round(player.radius, self.__n_digits)} for uuid, player in self._players.items() if uuid is not player_uuid]
        state['d'] = 1 if current_player.is_defeated else 0
        state['s'] = current_player.score
        
        return state

    def get_state_for_spectator(self):
        state = self.__get_common_state_part(self.__n_digits)
        state['ps'] = [{'n': player.player_name, 'x': round(player.x, self.__n_digits), 'y': round(player.y, self.__n_digits), 'r': round(player.radius, self.__n_digits)} for uuid, player in self._players.items()]
        return state

    def _is_end(self):
        '''Check if game should end.'''
        return False or self._is_terminated

    def _cleanup(self):
        pass

    def __generate_random_position(self):
        wrong_position = True
        while wrong_position:
            x, y = random.uniform(0, self.__board.max_size[0]), random.uniform(0, self.__board.max_size[1])  
            wrong_position = False
            for player in self._players.values():
                if euclidean_distance(x, player.x, y, player.y) <= player.radius:
                    wrong_position = True
                    break
        return x, y




            