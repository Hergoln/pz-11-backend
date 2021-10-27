import asyncio
import websockets
import logging
from urllib.parse import urlparse, parse_qs 
from secrets import token_hex

from .session import Session

class GameServer:
    '''
    Class which defines main game server. Handles all connections and process them.
    '''

    def __init__(self, game_factory, url, port):
        '''
        Constructor of GameServer class/
        
        Parameters:
        game_factory: GameFactory object. Using this object games instances can be created.
        url: URL of server
        port: Port on which server will be listening.
        '''
        
        self.__url = url
        self.__port = port
        self.__sessions = dict()
        self.__game_factory = game_factory
        self.__loop = asyncio.get_event_loop()

    def listen(self):
        '''Main function of server, starts a endless loop, listening on url.'''

        logging.info(f'listening started')
        service = websockets.serve(self.__handle_new_connection, self.__url, self.__port)
        self.__loop.run_until_complete(service)
        self.__loop.run_forever()
        logging.info(f'listening finished')

    async def __handle_new_connection(self, websocket, path):
        '''Async method to handle and propagate to proper methods connections.'''

        logging.info(f'new connection with {websocket.id}, with path = {path}')
        query = parse_qs(urlparse(path).query)

        if '/create_game' in path:
            session_id = await self.create_new_session()
            await self.create_new_game(session_id, 'agarnt')
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


    async def create_new_game(self, session_id, game_type, game_config = None):
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

    async def terminate_game(self, session_id):
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
