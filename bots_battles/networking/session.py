import asyncio
import websockets
import logging

from .communication_handler import CommunicationHandler
from .game_client import GameClient
from games.agarnt import AgarntGame, AgarntGameConfig



class Session:
    def __init__(self, session_id):
        self.__session_id = session_id
        self.__players = []
        self.__game = None
        self.__communication_handler = CommunicationHandler()

        logging.info("Session created!")

    async def create_player(self, websocket):
        game_client = GameClient(websocket, self.__communication_handler)
        self.__players.append(game_client)

        try:
            await game_client.handle_messages()
        except:
            logging.info('Client disconnected')

    async def create_game(self, game_type: str):
        if game_type == 'agarnt':
            self.__game = AgarntGame(AgarntGameConfig(), self.__communication_handler)
        else:
            raise RuntimeError('Not supported game!')
        # await self.__game.run()
        logging.info(f"Create new game, game type {game_type}")
        
        await asyncio.create_task(self.__game.run())


    async def terminate_game(self):
        logging.info('Game terminated')
        self.__game.terminate()

    @property
    def session_id(self):
        return self.__session_id



