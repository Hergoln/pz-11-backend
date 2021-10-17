from game_engine import CommunicationHandler
from games.agarnt import AgarntGame

def createGame():
    websocket_handler = None
    communication_handler = CommunicationHandler(websocket_handler)
    game = AgarntGame(communication_handler)
    game.run()
    input()

print("Welcome")
createGame()
input()