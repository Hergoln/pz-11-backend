import asyncio
import logging
import time
from asyncio.tasks import sleep
from .agarnt_game_logic import AgarntGameLogic
from game_engine import Game, Clock

class AgarntGame(Game):
    intance_counter = 0

    def __init__(self, game_config, communication_handler):
        super().__init__(AgarntGameLogic(), game_config, communication_handler)
        AgarntGame.intance_counter = AgarntGame.intance_counter + 1
        self.object_counter = AgarntGame.intance_counter
        self.clock = Clock()

        logging.info(f'Create Agarnt game {self.object_counter}')
        

    async def run(self):
        print('run agarnt')
        print(__name__)
        while not self._is_end():
            self._communication_handler.handle_incomming_messages(lambda msg: self._game_logic(msg))

            await self.clock.tick(30)
        self._cleanup()

    def _is_end(self):
        '''Check if game should end.'''
        return False or self._is_terminated

    def _cleanup(self):
        pass
            