# from game_engine import CommunicationHandler
# from games.agarnt import AgarntGame, AgarntGameConfig

# def createGame():
#     websocket_handler = None
#     communication_handler = CommunicationHandler(websocket_handler)
#     config = AgarntGameConfig()
#     game = AgarntGame(config, communication_handler)
#     game.run()

# print("Welcome in bots battles test!")
# createGame()
# input()

import logging
from networking import GameServer

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # watek od servera
    # watek od flaska
    # 
    echo = GameServer('localhost', 2137)
    echo.listen()
