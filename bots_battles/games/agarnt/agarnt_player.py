from bots_battles.game_engine import Player
from uuid import UUID 
from typing import Dict

class AgarntPlayer(Player):
    VELOCITY = 5

    def __init__(self, player_name: str, uuid: UUID):
        super().__init__(uuid)
        self.player_name = player_name
        self.radius = 1
        self.x = 0.0
        self.y = 0.0
        self.color = None

    def update_position(self, directions: Dict[str, bool], delta: float):        
        if directions['U']: #UP
            self.y += AgarntPlayer.VELOCITY / self.radius * delta
        if directions['D']: #DOWN
            self.y -= AgarntPlayer.VELOCITY / self.radius * delta
        if directions['L']: #LEFT
            self.x -= AgarntPlayer.VELOCITY / self.radius * delta
        if directions['R']: #RIGHT
            self.x += AgarntPlayer.VELOCITY / self.radius * delta
    
    def get_radius(self) -> int:
        return self.radius

    def eat_food(self, number_of_eaten_food: int):
        self.radius += number_of_eaten_food
        