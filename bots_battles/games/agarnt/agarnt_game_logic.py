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
    PLAYER_RADIUS_RATIO = 0.8

    def __init__(self, board: Board):
        self.__board = board
        self.__players = None

    def set_players(self, players: Dict[UUID, AgarntPlayer]):
        self.__players = players

    def process_input(self, player_uuid: str, message: Dict[str, str], delta: float):
        '''
        Process player inputs using game rules.
        '''

        player = self.__players.get(player_uuid, None)
        if player is None:
            return
        player.update_position(message['directions'], self.__board.max_size, delta)
        

        other_players = [other_uuid for other_uuid in self.__players if other_uuid != player_uuid] 
        is_collision, first_player = self.is_collision_with_other_players(player, other_players)
        if is_collision:
            player.is_defeated = True
            first_player.eat_other_players([player])
            return

        self.update_eaten_other_players(player, other_players)
        self.update_eaten_foods(player)

    def update_eaten_foods(self, player):
        '''
        Method to check if current player eaten foods
        and game logic adds to player more points and increases the radius.
        '''
        try:
            foods_to_remove = [f for f in self.__board.foods if euclidean_distance(f[0], player.x, f[1], player.y) <= player.get_radius()] 
            player.eat_food(len(foods_to_remove))
            for f in foods_to_remove:
                self.__board.foods.remove(f)
        except Exception as e:
            print("FOOD ERROR: ", repr(e))

    def update_eaten_other_players(self, player, other_players):
        '''
        Method to check if player find other smaller players
        and game logic adds to player points and increases the radius.
        '''
        try:
            players_to_remove = [self.__players[uuid] for uuid in other_players if self.__players[uuid].radius/player.radius < AgarntGameLogic.PLAYER_RADIUS_RATIO
                                                and euclidean_distance(self.__players[uuid].x, player.x, self.__players[uuid].y, player.y) <= player.radius]

            player.eat_other_players(players_to_remove)
            for p in players_to_remove:
                p.is_defeated = True # set flag to true if eaten, then use it to send proper state message
        except Exception as e:
            print("OTHER PLAYER ERROR: ", repr(e))

    def is_collision_with_other_players(self, player, other_players):
        '''
        Method to check if player collides with other bigger players.
        If yes - game logic marks current player as defeated and returns.
        If no - game logic continues.
        '''
        try:
            result = [self.__players[uuid] for uuid in other_players if player.radius/self.__players[uuid].radius < AgarntGameLogic.PLAYER_RADIUS_RATIO
                        and euclidean_distance(self.__players[uuid].x, player.x, self.__players[uuid].y, player.y) <= player.radius]
            first_player = result[0] if len(result) > 0 else None
            return any(result), first_player

        except Exception as e:
            print("PLAYER COLLISION ERROR: ", repr(e))