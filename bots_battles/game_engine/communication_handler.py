from threading import Lock
from typing import Callable, Dict, Set, Tuple
from uuid import UUID

class CommunicationHandler:
    '''
    Defines the 'bridge' between networking structure (or another) and game engine.
    '''

    def __init__(self, send_to_handler: Callable[[UUID, str], None]) :
        '''
        Constructor.
        Parameters:
        send_to_handler: Outcomming messages from game will be passed to this callback.
        '''
        self.__incomming_messages_lock = Lock()
        self.__incoming_messages: Dict[str, str] = dict()
        self.__send_to_handler = send_to_handler

    def set_last_message(self, player_uuid: UUID, message: Dict[str, str]):
        '''
        Method which store last incoming message into internal structure 
        for futher processing.
        Threadsafe.
        '''

        with self.__incomming_messages_lock:
            self.__incoming_messages[player_uuid] = message

    def handle_incomming_messages(self, fun: Callable[[str, Dict[str, str]], None], delta: float) -> Set[str]:
        '''
        Method which will process all messages stored into queue 
        by passing them to callback 'fun' to futher handling.
        Threadsafe.
        Returns components names which defines which information should be updated.
        '''
        components_to_update = set()
        with self.__incomming_messages_lock:
            for uuidWithMessage in self.__incoming_messages.items():
                comp = fun(*uuidWithMessage, delta)
                components_to_update = components_to_update.union(comp)
            self.__incoming_messages.clear()
        return components_to_update

    async def handle_game_state(self, state: Dict[UUID, str]):
        '''
        Async method which pass actual state for all players to ouput callback.
        '''

        for player_uuid, player_state in state.items():
            await self.__send_to_handler(player_uuid, player_state)
