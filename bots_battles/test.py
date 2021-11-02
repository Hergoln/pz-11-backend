import logging
from game_engine.networking import GameServer
from games import GameFactory

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    server = GameServer(GameFactory(), 'localhost', 2137)
    server.listen()
