import asyncio
import websockets
import logging
from urllib.parse import urlparse, parse_qs 
from secrets import token_hex

from .session import Session

class GameServer:
    def __init__(self, url, port):
        self.__url = url
        self.__port = port
        self.__sessions = dict()
        self.__loop = asyncio.get_event_loop()

    async def __new_client_handler(self, websocket, path):
        logging.info(f'new connection with {websocket.id}, with path = {path}')
        if '/create_game' in path:
            session = Session(self.__create_unique_session_id())
            logging.info(f'Newly created session id = {session.session_id}')
            self.__sessions[session.session_id] = session 
            await session.create_game('agarnt')

        elif '/join_to_game' in path:
            # TODO extract to method
            query = parse_qs(urlparse(path).query)
            if query['session_id'][0] in self.__sessions:
                await self.__sessions[query['session_id'][0]].create_player(websocket)
            else:
                logging.error(f'Session with id {query["session_id"]} does not exist!')
        
        elif '/terminate_game' in path:
            query = parse_qs(urlparse(path).query)
            if query['session_id'][0] in self.__sessions:
                await self.__sessions[query['session_id'][0]].terminate_game()
            else:
                logging.error(f'Session with id {query["session_id"]} does not exist!')
        
        

    def listen(self):
        logging.info(f'listening started')
        service = websockets.serve(self.__new_client_handler, self.__url, self.__port)
        self.__loop.run_until_complete(service)
        self.__loop.run_forever()
        logging.info(f'listening finished')

    # async def clean(self):
    #     pass
    
    # async def broadcast(self, message):
    #     pass

    # async def send(self, to, message):
    #     logging.info(f'send to {to}:\t message: {message}')
    #     pass

    # async def receive(self, sender, message):
    #     logging.info(f'receive from {sender}:\t message: {message}')

        
    def __create_unique_session_id(self):
        session_id = f"session_{token_hex(8)}"
        while session_id in self.__sessions:
            session_id = f"session_{token_hex(8)}"
        
        return session_id
