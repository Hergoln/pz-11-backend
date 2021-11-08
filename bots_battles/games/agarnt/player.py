from uuid import UUID 
class Player:
    VELOCITY = 5

    def __init__(self, player_name: str, uuid: UUID):
        self.player_name = player_name
        self.uuid = uuid
        self.mass = 1
        self.x = 0.0
        self.y = 0.0
        self.color = None

    def update_position(self, direction: str):        
        if direction == "UP":
            self.y += Player.VELOCITY / self.mass 
        elif direction == "DOWN":
            self.y -= Player.VELOCITY / self.mass 
        elif direction == "LEFT":
            self.x -= Player.VELOCITY / self.mass 
        elif direction == "RIGHT":
            self.x += Player.VELOCITY / self.mass 
        else:
            raise RuntimeError("Not defined direction!")
    
    def get_radius(self) -> int:
        return self.mass

    def eated_food(self, number_of_eaten_food: int):
        self.mass += number_of_eaten_food