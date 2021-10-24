import asyncio
import websockets

class GameClient:
    def __init__(self, websocket, communication_handler):
        self.__communication_handler = communication_handler
        self.__websocket = websocket

    async def handle_messages(self):
        async for msg in self.__websocket:
            self.__communication_handler.on_receive(msg)


