from typing import Dict, Optional, Union
from flask import request, jsonify, Blueprint
import uuid
from flask.wrappers import Response
from bots_battles import GameFactory
import sys
from settings import PREFFERED_WS_PORT
import os
from websocket import create_connection
import urllib

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]
this.game_factory =None

def init_factory(factory: GameFactory): this.game_factory = factory

game_bp = Blueprint("game", __name__)

@game_bp.route('/games/types/')
def game_types() -> Response:
    return jsonify({ 'game_types': list(this.game_factory.get_all_games()) })

@game_bp.route('/games/', methods=['POST', 'GET'])
def games() -> Union[str, Response]:
    if request.method == 'POST':
        print("HOST:", request.host)
        
        host =  request.host
        content: Dict[str, str] = request.json
        
        host = host.split(':')[0]

        return create_new_game(content, host)
        
    else:
        return "All games (in the future)"


def create_new_game(content:Dict[str, str], host: str) -> Response:
    """Connects temporarily with GameServer to create new instance of provided
    game in @content parameter. 

    Args:
        content (Dict[str, str]): Obtained json from request, it stores name and type of game to create
        host (str): Extracted host from request url.

    Returns:
        Response: JSON response that contains:
            - session id obtained from websocket server - to allow players to join newly created game;
            - name of game
            - type of game
    """
    port = os.environ.get("WS_PORT", PREFFERED_WS_PORT)
    url = f"ws://{host}:{port}/create_game?{urllib.parse.quote_plus('&'.join([f'{k}={v}' for k, v in content.items()]))}"
    print("WS URL: ", (url))
    ws = create_connection((url))
    
    session_id:str = ws.recv()
    ws.close()

    return jsonify({
        "id": session_id, # invite key
        "name": content['name'],
        "type": content['type']
    })

#TODO: endpoint deprecated
@game_bp.route('/games/<invite_key>', methods=['PUT'])
def join_game(invite_key: Optional[str] =None) -> Response:
    # todo: add logic to join to the game  in the future
    # invite_key == id
    return f"Successfully joined the game! Your invite key is: {invite_key}."
