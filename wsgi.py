from typing import List
from website import create_app
import os
import logging
production = 'PRODUCTION' in os.environ
logging.basicConfig(level=logging.WARNING if production else logging.DEBUG)

import asyncio

from bots_battles import GameFactory
from bots_battles import GameServer
from threading import Thread
from time import sleep
from settings import GAMES

global game_server
if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    ws_port = os.environ.get("WS_PORT", 2137)
    
    game_factory = GameFactory(GAMES)
    game_server = GameServer(game_factory, "0.0.0.0", ws_port)
    
    def game_server_init(game_server, game_factory):
        asyncio.set_event_loop(asyncio.new_event_loop())
        
        try:
            game_server.listen(asyncio.get_event_loop())
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt")
    

    game_thread = Thread(target=game_server_init, args=[game_server, game_factory])
    game_thread.start()

    app = create_app(game_server, game_factory)

    try:
        app.run(debug=not production, host="0.0.0.0", port=port, use_reloader=False)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt")

    print(game_server)
    game_server.terminate()
    game_thread.join()
    