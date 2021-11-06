from website import create_app
import os
import logging
logging.basicConfig(level=logging.DEBUG)


import asyncio

from bots_battles import GameFactory
from bots_battles import GameServer
from threading import Thread
from time import sleep
from settings import GAMES


#app = create_app(game_factory)
if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)

    game_factory = GameFactory(GAMES)

    print("sikikupapierd")
    def game_server_init(game_factory):
        asyncio.set_event_loop(asyncio.new_event_loop())
        ws_port = os.environ.get("WS_PORT", 2137)
        game_server = GameServer(game_factory, "0.0.0.0", ws_port)
        game_server.listen()
    

    game_thread = Thread(target=game_server_init, args=[game_factory])
    game_thread.start()

    app = create_app(game_factory)
    app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)