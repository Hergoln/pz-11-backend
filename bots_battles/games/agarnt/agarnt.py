import asyncio
import logging
from .agarnt_game_logic import AgarntGameLogic
from game_engine import Game, Clock

class AgarntGame(Game):
    instance_counter = 0

    def __init__(self, game_config, communication_handler):
        super().__init__(AgarntGameLogic(), game_config, communication_handler)
        AgarntGame.instance_counter = AgarntGame.instance_counter + 1
        self.object_counter = AgarntGame.instance_counter
        self.clock = Clock()

        logging.info(f'create Agarnt game {self.object_counter}')
        

    async def run(self):
        while not self._is_end():
            self._communication_handler.handle_incomming_messages(lambda msg: self._game_logic.process_input(msg))

            await self.clock.tick(self._game_config.game_speed)

        self._cleanup()

    def _is_end(self):
        '''Check if game should end.'''
        return False or self._is_terminated

    def _cleanup(self):
        pass
            