import orjson
import datetime
import logging
from uuid import UUID
from typing import Dict, Set
from .game_logic import GameLogic
from .game import Game 
from .game_logic import GameLogic 
from .game_config import GameConfig 
from .clock import Clock 
from .communication_handler import CommunicationHandler

class JSONGame():
    def __init__(self, info) -> None:
        self.states = list()
        self.info = info

    def dump_to_archive(self) -> None:
        logging.info("dumping to archive")
        with open(f"agarnt_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}", 'wb', encoding='utf-8') as archive:
            archive.write(orjson.dumps(self))
        logging.info("game dumped")


class RealtimeGame(Game):
    def __init__(self, game_logic: GameLogic, game_config: GameConfig, communication_handler: CommunicationHandler):
        super().__init__(game_logic, game_config, communication_handler)
        self._clock = Clock()
        self._ping_timer = 0.0

        info = {'game_config':game_config.to_json(), 'game_type':'agarnt'}
        self.archive_record = JSONGame(info)

    async def run(self):
        delta = 0
        while not self._is_end():
            components_to_update = self._communication_handler.handle_incomming_messages(self._game_logic.process_input, delta)
            delta = await self._clock.tick(self._game_config['fps'])
            await self.update_game_state(components_to_update, delta)
            await self.send_ping(delta)

        logging.info("Game stopped")
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

