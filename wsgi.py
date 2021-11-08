from typing import List
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

global game_server
#app = create_app(game_factory)
if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    game_server: List[GameServer] = [None]
    game_factory = GameFactory(GAMES)
    ws_port = os.environ.get("WS_PORT", 2137)
    
    def game_server_init(game_factory):
        asyncio.set_event_loop(asyncio.new_event_loop())
        game_server[0] = GameServer(game_factory, "0.0.0.0", ws_port)
        
        try:
            game_server[0].listen()
        except KeyboardInterrupt:
            print("haha bongosy")
    

    game_thread = Thread(target=game_server_init, args=[game_factory])
    game_thread.start()

    app = create_app(game_factory)
    try:

        app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)
    except KeyboardInterrupt:
        print("HAHA BONGOSY")
    print(game_server[0])
    game_server[0].terminate()
    game_thread.join()
    