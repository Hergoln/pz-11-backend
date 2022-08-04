from __future__ import annotations

import logging
import random
from typing import Set
from uuid import UUID

import orjson

from bots_battles.game_engine import RealtimeGame, CommunicationHandler, JSONGame
from bots_battles.game_engine.player import Spectator
from util.math import euclidean_distance
from .agarnt_game_config import AgarntGameConfig
from .agarnt_game_logic import AgarntGameLogic
from .agarnt_player import AgarntPlayer
from .board import Board


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
        self.__empty_server_timer = 0.0
        self.__no_players = True

        # game_type will be also used for storage directory
        info = {'game_type': 'agarnt'}
        self.archive_record = JSONGame(info)

    async def run(self):
        delta = 0
        while not self._is_end():
            components_to_update = self._communication_handler.handle_incomming_messages(self._game_logic.process_input, delta)
            delta = await self._clock.tick(self._game_config['fps'])
            await self.update_game_state(components_to_update, round(delta, self.__n_digits))

            if self.__no_players:
                self.__empty_server_timer += delta
            else:
                self.__empty_server_timer = 0

            await self.send_ping(delta)

        self.archive_record.dump_to_archive()
        self._cleanup()

    def add_player(self, player_uuid: UUID, player_name: str) -> str:
        self.__no_players = False
        x, y = self.__generate_random_position()
        self._players[player_uuid] = AgarntPlayer(player_name, player_uuid, (x, y))

        components = set()
        components.add("position")
        components.add("food")
        components.add("board")
        components.add("score")

        player_state = self.get_state_for_player(components, player_uuid)
        player_state["delta"] = 0.0
        return orjson.dumps(player_state).decode("utf-8")

    def remove_player(self, player_uuid: UUID):
        super().remove_player(player_uuid)
        if len(self._players) == 0:
            self.__no_players = True

    def add_spectator(self, spectator_uuid: UUID, spectator_name: str) -> str:
        self._spectators[spectator_uuid] = Spectator(spectator_uuid, spectator_name)

        components = set()
        components.add("position")
        components.add("food")
        components.add("board")
        components.add("score")
        player_state = self.get_state_for_spectator(components)
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
        return self._is_terminated or self.__empty_server_timer >= self._game_config["waiting_time"]

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
