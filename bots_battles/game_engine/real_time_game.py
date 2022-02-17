import imp
import orjson
from uuid import UUID
from typing import Dict, Set
from .game_logic import GameLogic
from .game import Game 
from .game_logic import GameLogic 
from .game_config import GameConfig 
from .clock import Clock 
from .communication_handler import CommunicationHandler
from .game_archive import JSONGame

class RealtimeGame(Game):
    def __init__(self, game_logic: GameLogic, game_config: GameConfig, communication_handler: CommunicationHandler):
        super().__init__(game_logic, game_config, communication_handler)
        self._clock = Clock()
        self._ping_timer = 0.0

        info = {'game_type':'none'}
        self.archive_record = JSONGame(info)

    async def run(self):
        delta = 0
        while not self._is_end():
            components_to_update = self._communication_handler.handle_incomming_messages(self._game_logic.process_input, delta)
            delta = await self._clock.tick(self._game_config['fps'])
            await self.update_game_state(components_to_update, delta)
            await self.send_ping(delta)

        self.archive_record.dump_to_archive()
        self._cleanup()

        
    async def update_game_state(self, components_to_update: Set[str], delta: float):
        '''
        Helper method which can be used to get all players states and pass them to communication handler.
        '''  
        if len(components_to_update) == 0:
            return 

        states = dict() 
        spectator_state = self.get_state_for_spectator(components_to_update)
        spectator_state['delta'] = delta
        for spectator_uuid in self._spectators.keys():
            states[spectator_uuid] = orjson.dumps(spectator_state).decode("utf-8")
        await self._communication_handler.handle_game_state(states)

        states: Dict[UUID, str] = dict()
        archived_states: Dict(str, str) = dict()
        for player_uuid in self._players.keys():
            player_state = self.get_state_for_player(components_to_update, player_uuid)
            player_state['delta'] = delta
            states[player_uuid] = orjson.dumps(player_state).decode("utf-8")
            archived_states[str(player_uuid)] = player_state
        # save players states changes into archive record
        self.archive_record.states.append(archived_states)
        await self._communication_handler.handle_game_state(states)

    async def send_ping(self, delta):
        if self._ping_timer >= 5.0:
            self._ping_timer = 0
            states: Dict[UUID, str] = dict()
            for player_uuid in self._players.keys():
                player_state = dict()
                player_state['delta'] = delta
                states[player_uuid] = orjson.dumps(player_state).decode("utf-8")
            await self._communication_handler.handle_game_state(states)
        self._ping_timer += delta

