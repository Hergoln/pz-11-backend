import asyncio
import logging

from .communication_handler import CommunicationHandler
from .game_client import GameClient
from games.agarnt import AgarntGame, AgarntGameConfig


class Session:
    '''
    Define Session class, which handles one game instance and manage all it's plyers.
    Each session instance has a CommunicationHandler object which will be 
    shared between all players.
    '''

    def __init__(self, session_id):
        self.__session_id = session_id
        self.__players = []
        self.__game = None
        self.__communication_handler = CommunicationHandler()

        logging.info("Session created!")

    async def create_player(self, websocket):
        '''Async method to create player and add them to game
        Parameters:
        websocket - player websocket
        '''
        game_client = GameClient(websocket, self.__communication_handler)
        self.__players.append(game_client)

        try:
            await game_client.handle_messages()
        except:
            logging.info('Client disconnected')

    async def create_game(self, game_type: str):
        '''Async method to create game instance.
        If game exists in session instance, runtime execption will be raised
        Parameters:
        game_type - define game type to be created
        '''
        if self.__game != None:
            raise RuntimeError('Game in this session already exists!')

        if game_type == 'agarnt':
            self.__game = AgarntGame(AgarntGameConfig(), self.__communication_handler)
        else:
            raise RuntimeError('Not supported game!')
        logging.info(f"Create new game, game type {game_type}")
        
        await asyncio.create_task(self.__game.run())

    async def terminate_game(self):
        '''Async method to terminate existing game.
        If game not exists in session instance, runtime execption will be raised
        '''
        if self.__game == None:
            raise RuntimeError('Game in this session do not exists!')

        logging.info('Game terminated')
        self.__game.terminate()
        self.__game = None

    @property
    def session_id(self):
        '''Returns a unique session id.'''
        return self.__session_id



