from .game_logic import GameLogic
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
        delta = 0
        while not self._is_end():
            self._communication_handler.handle_incomming_messages(self._game_logic.process_input, delta)
            delta = await self._clock.tick(self._game_config['fps'])
            await self.update_game_state(delta)
            
        self._cleanup()