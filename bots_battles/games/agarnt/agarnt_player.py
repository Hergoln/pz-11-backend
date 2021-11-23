from __future__ import annotations
from bots_battles.game_engine import Player
from uuid import UUID 
from typing import Dict, List
import numpy as np

class AgarntPlayer(Player):
    MAX_VELOCITY = 20

    def velocity(cls, radius):
        log_value = np.log(radius) + 1
        return cls.MAX_VELOCITY - max(0, min(log_value, cls.MAX_VELOCITY - 1)) # clamp

    def __init__(self, player_name: str, uuid: UUID):
        super().__init__(uuid)
        self.player_name = player_name
        self.radius = 1
        self.x = 0.0
        self.y = 0.0
        self.color = None

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
        self.radius += number_of_eaten_food

    def eat_other_player(self, other_players: List[AgarntPlayer]):
        self.radius += sum(p.radius for p in other_players)

        