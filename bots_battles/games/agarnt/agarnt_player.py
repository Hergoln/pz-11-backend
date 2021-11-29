from __future__ import annotations
from bots_battles.game_engine import Player
from uuid import UUID 
from typing import Dict, List
import numpy as np

class AgarntPlayer(Player):
    MAX_VELOCITY = 20

    @classmethod
    def velocity(cls, radius):
        log_value = np.log(radius) + 1
        # conversion to Python's float is necessary because np.log returns np.float64 object which is non-serializable
        return float(cls.MAX_VELOCITY - max(0, min(log_value, cls.MAX_VELOCITY - 1))) # clamp

    @classmethod
    def radius_func(cls, value):
        # same deal here
        return float(np.sqrt(value))

    def __init__(self, player_name: str, uuid: UUID):
        super().__init__(uuid)
        self.player_name = player_name
        self.radius = 1
        self.x = 0.0
        self.y = 0.0
        self.color = None
        self.score = 0

    def update_position(self, directions: Dict[str, bool], delta: float):        
        if directions['U']: #UP
            self.y += AgarntPlayer.velocity(self.radius) * delta
        if directions['D']: #DOWN
            self.y -= AgarntPlayer.velocity(self.radius) * delta
        if directions['L']: #LEFT
            self.x -= AgarntPlayer.velocity(self.radius) * delta
        if directions['R']: #RIGHT
            self.x += AgarntPlayer.velocity(self.radius) * delta
    
    def get_radius(self) -> int:
        return self.radius

    def eat_food(self, number_of_eaten_food: int):
        self.radius += AgarntPlayer.radius_func(number_of_eaten_food)
        self.score += number_of_eaten_food

    def eat_other_players(self, other_players: List[AgarntPlayer]):
        players_total_size = sum(p.radius for p in other_players)
        self.radius += AgarntPlayer.radius_func(players_total_size)
        self.score += int(players_total_size)

        