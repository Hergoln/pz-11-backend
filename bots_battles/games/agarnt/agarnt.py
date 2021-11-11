from __future__ import annotations
import asyncio
import logging
import orjson
from typing import Dict
from uuid import UUID

from .agarnt_game_logic import AgarntGameLogic
from .agarnt_game_config import AgarntGameConfig
from .agarnt_player import AgarntPlayer
from .board import Board
from bots_battles.game_engine import Game, Clock, CommunicationHandler

class AgarntGame(Game):
    instance_counter = 0

    def __init__(self, game_config: AgarntGameConfig, communication_handler: CommunicationHandler):
        self.__board = Board(50, (200, 200))

        super().__init__(AgarntGameLogic(self.__board), game_config, communication_handler)
        self._game_logic.set_players(self._players)

        AgarntGame.instance_counter = AgarntGame.instance_counter + 1
        self.object_counter = AgarntGame.instance_counter
        self.clock = Clock()

        logging.info(f'create Agarnt game {self.object_counter}')
        

    async def run(self):
        while not self._is_end():
            self._communication_handler.handle_incomming_messages(lambda msg: self._game_logic.process_input(msg))

            await self.clock.tick(self._game_config.game_speed)
            await self.update_game_state()
            
        self._cleanup()


    def add_player(self, player_uuid: UUID, player_name: str):
        self._players[player_uuid] = AgarntPlayer(player_name, player_uuid)
    
    def remove_player(self, player_uuid: UUID):
        del self._players[player_uuid]

    def get_state_for_player(self, player_uuid: UUID):
        current_player = self._players[player_uuid]
        state = dict()
        state['player'] = {'x': current_player.x, 'y': current_player.y, 'mass': current_player.mass}
        state['players'] = [{'name': player.name, 'x': player.x, 'y': player.y, 'mass': player.mass} for uuid, player in self._players.items() if uuid is not player_uuid]
        state['board'] = self.__board.max_size
        state['food'] = self.__board.foods
        
        return orjson.dumps(state).decode("utf-8")

    def _is_end(self):
        '''Check if game should end.'''
        return False or self._is_terminated

    def _cleanup(self):
        pass
            