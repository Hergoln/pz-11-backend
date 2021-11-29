from __future__ import annotations
import abc
from typing import Dict
from uuid import UUID

import orjson

from .communication_handler import CommunicationHandler
from .game_config import GameConfig
from .game_logic import GameLogic
from .player import Player

class Game(metaclass=abc.ABCMeta):
    '''Abstrac class which defines the game.'''

    def __init__(self, game_logic: GameLogic, game_config: GameConfig, communication_handler: CommunicationHandler):
        '''Create instance of game.
        Parameters:
        game_logic: Defines game logic. New class derivered from GameLogic abstract class should be passed here. 
        communication_handler: Handles communication between game and outside enviromment (for example a website or standalone application).
        '''
        self._players: Dict[UUID, Player] = dict()
        self._communication_handler = communication_handler
        self._is_terminated = False

        self._game_logic = game_logic
        self._game_config = game_config

    @abc.abstractmethod
    async def run(self):
        '''Starts a main loop of game. It's user task to create a loop and define their form 
        (for example, should it be a loop with a constant game step or a turn-based game)'''
        pass

    @abc.abstractmethod
    def add_player(self, player_uuid: UUID, player_name: str):
        '''
        Add player to game.
        Parameters:
        player_uuid: Player identificator.
        player_name: Player name.
        '''

        pass

    def remove_player(self, player_uuid: UUID):
        '''
        Remove player from game.
        '''

        self._players.pop(player_uuid, None)

    async def update_game_state(self, delta: float):
        '''
        Helper method which can be used to get all players states and pass them to communication handler.
        '''

        states: Dict[UUID, str] = dict()
        for player_uuid in self._players.keys():
            player_state = self.get_state_for_player(player_uuid)
            player_state['delta'] = delta
            states[player_uuid] = orjson.dumps(player_state).decode("utf-8")
        await self._communication_handler.handle_game_state(states)

    @abc.abstractmethod
    def get_state_for_player(self, player_uuid: UUID):
        '''Returns actual state of game for player with given UUID'''
        pass

    @abc.abstractmethod
    def _cleanup(self):
        ''''Cleanup all resources after close the game.'''
        pass
    
    def terminate(self):
        ''''Terminates main loop game'''
        self._is_terminated = True

    @property
    def game_config(self):
        return self._game_config
    
    def is_full(self):
        return self._game_config['max_player_number'] <= len(self._players) 

