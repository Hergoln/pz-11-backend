import asyncio
import websockets
import gzip
import orjson
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

        websocket_id = self.__websocket.id

        async for msg in self.__websocket:
            try:
                self.__communication_handler.set_last_message(websocket_id, orjson.loads(gzip.decompress(msg)))
            except Exception as e:
                print("PARSE ERROR: ", repr(e))
    
    async def terminate(self):
        await self.__websocket.close_connection()
        await self.__websocket.close()
    
    async def send(self, msg: str):
        '''
        Async method which send message by websocket.
        '''

        await self.__websocket.send(gzip.compress(msg.encode('utf-8')))


