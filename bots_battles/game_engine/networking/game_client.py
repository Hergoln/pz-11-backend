import asyncio
import websockets

class GameClient:
    '''
    Defines GameClient class which represent a player in network structure.
    '''
    def __init__(self, websocket, communication_handler):
        self.__communication_handler = communication_handler
        self.__websocket = websocket

    async def handle_messages(self):
        '''
        Async method to handle incoming messages from player 
        by passing them to CommunicationHandle object.
        '''
        async for msg in self.__websocket:
            self.__communication_handler.on_receive(msg)


