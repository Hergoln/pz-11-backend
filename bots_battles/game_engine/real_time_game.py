import orjson
from uuid import UUID
from typing import Dict, Set
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
            print("asdasd")
            components_to_update = self._communication_handler.handle_incomming_messages(self._game_logic.process_input, delta)
            delta = await self._clock.tick(self._game_config['fps'])
            await self.update_game_state(components_to_update, delta)
            
        self._cleanup()

        
    async def update_game_state(self, components_to_update: Set[str], delta: float):
        '''
        Helper method which can be used to get all players states and pass them to communication handler.
        '''
        if len(components_to_update) == 0:
            return 


        states: Dict[UUID, str] = dict()
        for player_uuid in self._players.keys():
            player_state = self.get_state_for_player(components_to_update, player_uuid)
            player_state['delta'] = delta
            states[player_uuid] = orjson.dumps(player_state).decode("utf-8")
        await self._communication_handler.handle_game_state(states)


        states = dict()
        spectator_state = self.get_state_for_spectator(components_to_update)
        spectator_state['delta'] = delta
        for spectator_uuid in self._spectators.keys():
            states[spectator_uuid] = orjson.dumps(spectator_state).decode("utf-8")
        await self._communication_handler.handle_game_state(states)
