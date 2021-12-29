from __future__ import annotations
import asyncio
import logging
import orjson
from typing import Dict, Set
from uuid import UUID

from bots_battles.game_engine.player import Spectator

from .agarnt_game_logic import AgarntGameLogic
from .agarnt_game_config import AgarntGameConfig
from .agarnt_player import AgarntPlayer
from .board import Board
from bots_battles.game_engine import RealtimeGame, CommunicationHandler, communication_handler

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
        

    def add_player(self, player_uuid: UUID, player_name: str) -> str:
        self._players[player_uuid] = AgarntPlayer(player_name, player_uuid)
        
        components = set()
        components.add("position")
        components.add("food")
        components.add("board")
        components.add("score")
        state: Dict[UUID, str] = dict()
        player_state = self.get_state_for_player(components, player_uuid)
        player_state["delta"] = 0.0
        return orjson.dumps(player_state).decode("utf-8")
    

    def add_spectator(self, spectator_uuid: UUID, spectator_name: str) -> str:
        self._spectators[spectator_uuid] = Spectator(spectator_uuid, spectator_name)
                
        components = set()
        components.add("position")
        components.add("food")
        components.add("board")
        components.add("score")
        player_state = self.get_state_for_player(components, spectator_uuid)
        player_state["delta"] = 0.0
        return orjson.dumps(player_state).decode("utf-8")
        

    def __get_common_state_part(self, components_to_update: Set[str], n_digits: int):
        state = dict()
        if "board" in components_to_update:
            state['b'] = self.__board.max_size
        if "food" in components_to_update:
            state['f'] = self.__board.foods
        return state


    def get_state_for_player(self, components_to_update: Set[str], player_uuid: UUID):
        current_player = self._players[player_uuid]
        state = self.__get_common_state_part(components_to_update, self.__n_digits)
        if "position" in components_to_update:
            print('pos')
            state['p'] = {'x': round(current_player.x, self.__n_digits), 'y': round(current_player.y, self.__n_digits), 'r': round(current_player.radius, self.__n_digits)}
            state['ps'] = [{'n': player.player_name, 'x': round(player.x, self.__n_digits), 'y': round(player.y, self.__n_digits), 'r': round(player.radius, self.__n_digits)} for uuid, player in self._players.items() if uuid is not player_uuid]
            state['d'] = 1 if current_player.is_defeated else 0
        if "score" in components_to_update:
            state['s'] = current_player.score
        
        return state

    def get_state_for_spectator(self, components_to_update: Set[str]):
        state = self.__get_common_state_part(components_to_update, self.__n_digits)
        if "position" in components_to_update:
            state['ps'] = [{'n': player.player_name, 'x': round(player.x, self.__n_digits), 'y': round(player.y, self.__n_digits), 'r': round(player.radius, self.__n_digits)} for uuid, player in self._players.items()]
        return state

    def _is_end(self):
        '''Check if game should end.'''
        return False or self._is_terminated

    def _cleanup(self):
        pass
            