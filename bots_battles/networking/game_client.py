import asyncio
import json
import websockets
from websockets.legacy.client import WebSocketClientProtocol
from ..game_engine import CommunicationHandler

class GameClient:
    '''
    Defines GameClient class which represent a player in network structure.
    '''
    
    def __init__(self, websocket: WebSocketClientProtocol, communication_handler: CommunicationHandler):
        self.__communication_handler = communication_handler
        self.__websocket = websocket

    async def handle_messages(self):
        '''
        Async method to handle incoming messages from player 
        by passing them to CommunicationHandle object.
        '''

        async for msg in self.__websocket:
            self.__communication_handler.on_receive(json.load(msg))
    
    async def terminate(self):
        await self.__websocket.close_connection()
        await self.__websocket.close()
    
    async def send(self, msg: str):
        await self.__websocket.send(msg)


