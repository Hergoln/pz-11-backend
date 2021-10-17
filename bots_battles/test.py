from game_engine import CommunicationHandler
from games.agarnt import AgarntGame, AgarntGameConfig

def createGame():
    websocket_handler = None
    communication_handler = CommunicationHandler(websocket_handler)
    config = AgarntGameConfig()
    game = AgarntGame(config, communication_handler)
    game.run()

print("Welcome in bots battles test!")
createGame()
input()