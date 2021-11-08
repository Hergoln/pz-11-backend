from __future__ import annotations

import asyncio
from asyncio.events import AbstractEventLoop
import time
from typing import Dict, Optional
from websockets.legacy.client import WebSocketClientProtocol
from websockets.legacy.server import serve
import logging
from urllib.parse import urlparse, parse_qs, unquote_plus 
from secrets import token_hex
from ..game_factory import GameFactory
from ..game_engine import GameConfig
from .session import Session

class GameServer:
    '''
    Class which defines main game server. Handles all connections and process them.
    '''

    def __init__(self, game_factory: GameFactory, url: str, port: int):
        '''
        Constructor of GameServer class/
        
        Parameters:
        game_factory: GameFactory object. Using this object games instances can be created.
        url: URL of server
        port: Port on which server will be listening.
        '''
        
        self.__url = url
        self.__port = port
        self.__sessions: Dict[str, Session] = dict()
        self.__game_factory = game_factory

    def listen(self, event_loop):
        '''Main function of server, starts a endless loop, listening on url.'''

        self.__loop = event_loop
        logging.info(f'listening started')
        self.__service = serve(self.__handle_new_connection, self.__url, self.__port)
        
        self.__listen_task = self.__loop.run_until_complete(self.__service)
        self.__loop.run_forever()
        logging.info(f'listening finished')

    async def __handle_new_connection(self, websocket: WebSocketClientProtocol, path: str):
        '''Async method to handle and propagate to proper methods connections.'''

        logging.info(f'new connection with {websocket.id}, with path = {path}')
        query = parse_qs(urlparse(unquote_plus(path)).query)
        logging.info(f"PARSED QUERY: {query}")
        if '/create_game' in path:
            session_id = await self.create_new_session()
            name = query['name'][0]
            _type = query['type'][0]
            print(name, _type)
            await websocket.send(session_id)
            await self.create_new_game(session_id, _type)

        elif '/join_to_game' in path:
            await self.join_to_game(websocket, query['session_id'][0])
        elif '/terminate_game' in path:
            await self.terminate_game(query['session_id'][0])
            

    def __create_unique_session_id(self):
        '''Creates new, unique session id'''

        session_id = f"session_{token_hex(8)}"
        while session_id in self.__sessions:
            session_id = f"session_{token_hex(8)}"
        
        return session_id

    async def create_new_session(self):
        '''
        Async method to create new session.
        Each session have a unique id, which can be used to determinate them.
        Also it is used as connection key when player wants to join to game.

        Returns session_id of created session.
        '''

        session = Session(self.__game_factory, self.__create_unique_session_id())
        self.__sessions[session.session_id] = session 
        
        logging.info(f'Newly created session id = {session.session_id}')

        return session.session_id

    async def create_new_game(self, session_id: str, game_type: str, game_config: Optional[GameConfig] = None):
        '''
        Async method to create game in existing session with given id.
        If game_type will be not defined, runtime error will be raised.
        
        Parameters:
        game_type: Game type, for example 'agarnt'.
        game_type: Game config, if None is set, default config will be set.
        '''
        
        await self.__sessions[session_id].create_game(game_type, game_config)

    async def join_to_game(self, websocket, session_id):
        '''
        Async method which handles joining to game by client.
        Game should be created before. Proper session will be selected based on session_id.
        If game will be not created, runtime error will be raised.
        
        Parameters:
        websocket: client websocket.
        session_id: session id where new player will be assign.
        '''

        if session_id in self.__sessions:
            await self.__sessions[session_id].create_player(websocket)
        else:
            logging.error(f'Session with id {session_id} does not exist!')

    async def terminate_game(self, session_id: str):
        '''
        Async method to terminate game.
        If game will be not running, runtime error will be raised.
        
        Parameters:
        session_id: session id which defines session, where game should be terminated.
        '''
        
        if session_id in self.__sessions:
            await self.__sessions[session_id].terminate_game()
        else:
            logging.error(f'Session with id {session_id} does not exist!')

    def create_new_session_sync(self):
        return asyncio.run_coroutine_threadsafe(self.create_new_session(), self.__loop).result()

    def create_new_game_sync(self, session_id: str, game_type: str, game_config: Optional[GameConfig] = None):
        asyncio.run_coroutine_threadsafe(self.create_new_game(session_id, game_type, game_config), self.__loop)

    def terminate(self):
        async def wrapper():
            [await session.clear() for session in self.__sessions.values()]
            self.__sessions.clear()

        asyncio.run(wrapper())
        self.__service.ws_server.close()
        print(self.__service.ws_server.close_task)
        
        async def stop_listen_task():
            self.__listen_task.close()
        self.__loop.run_until_complete(asyncio.wait([stop_listen_task()]))

        self.__loop.stop()
        
        self.__loop.close()

    @property
    def game_factory(self):
        '''Returns a game factory instance.'''
        return self.__game_factory
