import json
from threading import Lock
from typing import Callable, Dict, Tuple
from uuid import UUID

class CommunicationHandler:
    '''
    Defines the 'bridge' between networking structure (or another) and game engine.
    '''

    def __init__(self, broadcast_handler: Callable[[str], None]) :
        self.__incomming_messages_lock = Lock()
        self.__incoming_messages: Dict[str, str] = dict()
        self.__broadcast_handler = broadcast_handler

    def set_last_message(self, player_uuid: UUID, message: Dict[str, str]):
        '''
        Method which store last incoming message into internal structure 
        for futher processing.
        Threadsafe.
        '''

        with self.__incomming_messages_lock:
            self.__incoming_messages[player_uuid] = message

    def handle_incomming_messages(self, fun: Callable[[str, Dict[str, str]], None]):
        '''
        Method which will process all messages stored into queue 
        by passing them to callback 'fun' to futher handling.
        Threadsafe.
        '''

        with self.__incomming_messages_lock:
            for uuidWithMessage in self.__incoming_messages.items():
                fun(uuidWithMessage)

    async def handle_game_state(self, state: Dict[str, str]):
        # TODO change json
        await self.__broadcast_handler(state)