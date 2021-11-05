from asyncio import Queue
from threading import Lock
from typing import Callable

class CommunicationHandler:
    '''
    Defines the 'bridge' between networking structure (or another) and game engine.
    '''

    def __init__(self) :
        self.__incomming_messages_lock = Lock()
        self.__incoming_messages = Queue()

    def on_receive(self, message: str):
        '''
        Method which store incoming message into internal queue 
        for futher processing.
        Threadsafe.
        '''

        print("Communication handler: receive message", message)
        with self.__incomming_messages_lock:
            self.__incoming_messages.put_nowait(message)

    def handle_incomming_messages(self, fun: Callable[[Queue], None]):
        '''
        Method which will process all messages stored into queue 
        by passing them to callback 'fun' to futher handling.
        Threadsafe.
        '''

        with self.__incomming_messages_lock:
            while not self.__incoming_messages.empty():
                fun(self.__incoming_messages.get_nowait())
