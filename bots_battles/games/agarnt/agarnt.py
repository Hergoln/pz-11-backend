from __future__ import annotations
import asyncio
import logging
import json
from typing import Dict
from uuid import UUID
from .agarnt_game_logic import AgarntGameLogic
from .agarnt_game_config import AgarntGameConfig
from .player import Player
from .board import Board
from bots_battles.game_engine import Game, Clock, CommunicationHandler

class AgarntGame(Game):
    instance_counter = 0

    def __init__(self, game_config: AgarntGameConfig, communication_handler: CommunicationHandler):
        self.__board = Board(50, (200, 200))
        self.__players: Dict[UUID, Player] = dict()

        super().__init__(AgarntGameLogic(self.__board, self.__players), game_config, communication_handler)

        AgarntGame.instance_counter = AgarntGame.instance_counter + 1
        self.object_counter = AgarntGame.instance_counter
        self.clock = Clock()

        logging.info(f'create Agarnt game {self.object_counter}')
        

    async def run(self):
        while not self._is_end():
            self._communication_handler.handle_incomming_messages(lambda msg: self._game_logic.process_input(msg))

            await self.clock.tick(self._game_config.game_speed)
            await self._communication_handler.handle_game_state(self.get_state())
            
        self._cleanup()

    
    def add_player(self, player_uuid: UUID, player_name: str):
        self.__players[player_uuid] = Player(player_name, player_uuid)
    
    def remove_player(self, player_uuid: UUID):
        del self.__players[player_uuid]

    def get_state(self):
        state = dict()
        # state['players'] = [{'uuid': uuid, 'x': player.x, 'y': player.y, 'mass': player.mass} for uuid, player in self.__players.items()]
        state['board'] = self.__board.max_size
        # state['food'] = self.__board.foods

        # TODO convert dict to json
        return (state)

    def _is_end(self):
        '''Check if game should end.'''
        return False or self._is_terminated

    def _cleanup(self):
        pass
            