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

@game_bp.route('/game_config/<game_type>', methods=['GET'])
def game_config(game_type: Optional[str]=None) -> Response:
    game_config = this.game_server.game_factory.get_game_config_as_json(game_type)
    return game_config

@game_bp.route('/games/', methods=['POST', 'GET'])
def games() -> Union[str, Response]:
    if request.method == 'POST':
        print("HOST:", request.host)
        
        host = request.host
        content: Dict[str, str] = request.json
        
        host = host.split(':')[0]
        session_id = game_server.create_new_session_sync()
        game_config = content['config'] if 'config' in content else None
        game_server.create_new_game_sync(session_id, content['type'], game_config)
    
        return jsonify({
            "session_id": session_id
        })
    else:
        return jsonify(game_server.sessions_info)

@game_bp.route('/games/<session_id>', methods=['GET'])
def check_if_game_exists(session_id: Optional[str]=None) -> Response:
    result, game_type = game_server.check_session_exists(session_id)
    return json_game_exists_message("Game with given session id exists!", game_type) \
            if result else json_game_exists_message( "Game with given session id does not exist.", "", 404)

@game_bp.route('/games/<session_id>/<name>', methods=['GET'])
def check_if_name_in_game_exists(session_id: Optional[str], name: Optional[str]) -> Response:
    result = game_server.check_session_name_exists(session_id, name)
    return json_player_name_exists_message(f"Player named '{name}' already exists!", 406) \
         if result else json_player_name_exists_message(f"Player named '{name}' does not exists!")

def json_game_exists_message(message: str, game_type: str, status: int=200):
    return jsonify({
            "message": message,  
            "game_type": game_type
        }), status

def json_player_name_exists_message(message: str, status: int=200):
    return jsonify({"message": message}), status
