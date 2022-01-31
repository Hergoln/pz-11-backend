from __future__ import annotations
import abc
from typing import Dict, Set
from uuid import UUID

import orjson

from .communication_handler import CommunicationHandler
from .game_config import GameConfig
from .game_logic import GameLogic
from .player import Player, Spectator

class Game(metaclass=abc.ABCMeta):
    '''Abstrac class which defines the game.'''

    def __init__(self, game_logic: GameLogic, game_config: GameConfig, communication_handler: CommunicationHandler):
        '''Create instance of game.
        Parameters:
        game_logic: Defines game logic. New class derivered from GameLogic abstract class should be passed here. 
        communication_handler: Handles communication between game and outside enviromment (for example a website or standalone application).
        '''
        self._players: Dict[UUID, Player] = dict()
        self._spectators: Dict[UUID, Spectator] = dict()
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
    def add_player(self, player_uuid: UUID, player_name: str) -> str:
        '''
        Add player to game.
        Parameters:
        player_uuid: Player identificator.
        player_name: Player name.
        '''

        pass

    def add_spectator(self, spectator_uuid: UUID, spectator_name: str) -> str:
        '''
        Add spectator to game.
        Parameters:
        spectator_uuid: Player identificator.
        spectator_name: Spectator name:
        '''
        pass
        

    def remove_player(self, player_uuid: UUID):
        '''
        Remove player from game.
        '''

        self._players.pop(player_uuid, None)

    def remove_spectator(self, spectator_uuid: UUID):
        '''
        Remove spectator from game.
        '''

        self._spectators.pop(spectator_uuid, None)

    @abc.abstractmethod
    def get_state_for_player(self, components_to_update: Set[str], player_uuid: UUID):
        '''Returns actual state of game for player with given UUID'''
        pass

    @abc.abstractmethod
    def get_state_for_spectator(self, components_to_update: Set[str]):
        '''Returns actual state of game for all spectators'''
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

    @abc.abstractmethod
    def _is_end(self):
        pass

    @property
    def player_names(self):
        return (player.player_name for player in self._players.values())
