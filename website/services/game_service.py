from typing import Dict, Optional, Union
from flask import request, jsonify, Blueprint
import uuid
from flask.wrappers import Response
from bots_battles import GameFactory, GameServer
import sys
from bots_battles.networking import game_server
from settings import PREFFERED_WS_PORT
import os
import urllib
import asyncio

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]
this.game_server = None

def init_game_server(game_server: GameServer): this.game_server = game_server

game_bp = Blueprint("game", __name__)

@game_bp.route('/games/types/')
def game_types() -> Response:
    return jsonify({ 'game_types': list(this.game_server.
    game_factory.get_all_games()) })

@game_bp.route('/games/', methods=['POST', 'GET'])
def games() -> Union[str, Response]:
    if request.method == 'POST':
        print("HOST:", request.host)
        
        host = request.host
        content: Dict[str, str] = request.json
        
        host = host.split(':')[0]
        session_id = game_server.create_new_session_sync()
        game_server.create_new_game_sync(session_id, content['type'])
    
        return jsonify({
            "session_id": session_id
        })
        
    else:
        return "All active games (in the future)"

#TODO: endpoint deprecated
@game_bp.route('/games/<invite_key>', methods=['PUT'])
def join_game(invite_key: Optional[str] =None) -> Response:
    # todo: add logic to join to the game  in the future
    # invite_key == id
    return f"Successfully joined the game! Your invite key is: {invite_key}."
