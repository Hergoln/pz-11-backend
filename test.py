import logging
from bots_battles import GameServer, GameFactory
from settings import GAMES

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    server = GameServer(GameFactory(GAMES), 'localhost', 2137)
    server.listen()
