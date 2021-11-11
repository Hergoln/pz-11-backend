from bots_battles.game_engine.game_logic import GameLogic
from .game import Game 
from .game_logic import GameLogic 
from .game_config import GameConfig 
from .clock import Clock 
from .communication_handler import CommunicationHandler

class RealtimeGame(Game):
    def __init__(self, game_logic: GameLogic, game_config: GameConfig, communication_handler: CommunicationHandler):
        super().__init__(game_logic, game_config, communication_handler)
        self._clock = Clock()

    async def run(self):
        while not self._is_end():
            self._communication_handler.handle_incomming_messages(lambda msg: self._game_logic.process_input(msg))
            await self._clock.tick(self._game_config.game_speed)
            await self.update_game_state()
            
        self._cleanup()