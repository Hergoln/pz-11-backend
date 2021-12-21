from __future__ import annotations

import asyncio
import json
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
            game_type = query['type'][0]

            await websocket.send(session_id)
            await self.create_new_game(session_id, game_type)

        elif '/join_to_game' in path:
            player_name = unquote_plus(query['player_name'][0])
            session_id = unquote_plus(query['session_id'][0])
            is_spectator = (query['is_spectator'][0] == "True") if 'is_spectator' in query else False
            
            await self.join_to_game(websocket, player_name, session_id, is_spectator)
        elif '/terminate_game' in path:
            await self.terminate_game(websocket, query['session_id'][0])
            

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

    async def create_new_game(self, session_id: str, game_type: str, game_config: Optional[str] = None):
        '''
        Async method to create game in existing session with given id.
        If game_type will be not defined, runtime error will be raised.
        
        Parameters:
        game_type: Game type, for example 'agarnt'.
        game_type: Game config, if None is set, default config will be set, else it will be parsed to concrete game config
        '''
    
        config = self.__game_factory.get_game_config(game_type, game_config) if game_config else None
        await self.__sessions[session_id].create_game(game_type, config)

    async def join_to_game(self, websocket: WebSocketClientProtocol, player_name: str, session_id: str, is_spectator):
        '''
        Async method which handles joining to game by client.
        Game should be created before. Proper session will be selected based on session_id.
        If game will be not created, runtime error will be raised.
        
        Parameters:
        websocket: client websocket.
        session_id: session id where new player will be assign.
        is_spectator: Define if new player is spectator.
        '''

        if session_id in self.__sessions:
            if is_spectator:
                await self.__sessions[session_id].create_spectator(websocket, player_name)
            else:
                if self.__sessions[session_id].is_full():
                    await self.__send_full_session_session_message(websocket, session_id)
                else:
                    await self.__sessions[session_id].create_player(websocket, player_name)
        else:
            await self.__send_invalid_session_message(websocket, session_id)

    async def terminate_game(self, websocket: WebSocketClientProtocol, session_id: str):
        '''
        Async method to terminate game.
        If game will be not running, runtime error will be raised.
        
        Parameters:
        session_id: session id which defines session, where game should be terminated.
        '''
        
        if session_id in self.__sessions:
            await self.__sessions[session_id].terminate_game()
        else:
            await self.__send_invalid_session_message(websocket, session_id)

    def create_new_session_sync(self):
        '''
        Sync version of create_new_session method. 
        It wait for finish and returns a session_id of fresh session.
        It can be used in non asynchronus methods.
        '''
    
        return asyncio.run_coroutine_threadsafe(self.create_new_session(), self.__loop).result()

    def create_new_game_sync(self, session_id: str, game_type: str, game_config: Optional[str] = None):
        '''
        Sync version of create_new_game_method.
        It can be used in non asynchronus methods.
        '''
                    
        future = asyncio.run_coroutine_threadsafe(self.create_new_game(session_id, game_type, game_config), self.__loop)
        future.add_done_callback(lambda f: f.result())

    def terminate(self):
        for task in asyncio.all_tasks(self.__loop):
            task.cancel()
        self.__loop.stop()
        time.sleep(1)
        self.__loop.close()

    def check_session_exists(self, session_id: str):
        result = session_id in self.__sessions
        return result, self.__sessions[session_id].game_type if result else None

    @property
    def game_factory(self):
        '''Returns a game factory instance.'''
        return self.__game_factory

    @property
    def sessions_info(self):
        ''' Returns current games basic info'''
        list_of_sessions = []
        for session in self.__sessions.values():
            session_info = {
                "session_id": session.session_id,
                "game_type": session.game_type,
                "number_of_players": session.number_of_players
            }
            config = session.config
            if config is not None and 'max_player_number' in config:
                session_info['max_number_of_players'] = config['max_player_number']
            list_of_sessions.append(session_info)
        return list_of_sessions


    async def __send_invalid_session_message(self, websocket: WebSocketClientProtocol, session_id: str):
        '''Helper function which will send to given websocket information about invalid session'''
        
        logging.debug(f'Session with id {session_id} does not exist!')
        await websocket.send(json.dumps({'error': f'Session with {session_id} does not exist!'}))
        await websocket.close()

    async def __send_full_session_session_message(self, websocket: WebSocketClientProtocol, session_id: str):
        '''Helper function which will send to given websocket information about full game session'''
        
        logging.debug(f'Cannot join to session id {session_id}, players limit reached!')
        await websocket.send(json.dumps({'error': f'Cannot join to session id {session_id}, players limit reached!'}))
        await websocket.close()
