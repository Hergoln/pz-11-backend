from typing import Optional, Union
from flask import request, jsonify, Blueprint
import uuid
from flask.wrappers import Response
from bots_battles import GameFactory
from settings import GAMES
game_factory = GameFactory(GAMES) # think about it
game_bp = Blueprint("game", __name__)

@game_bp.route('/games/types/')
def game_types() -> Response:
    return jsonify({ 'game_types': list(game_factory.get_all_games()) })

@game_bp.route('/games/', methods=['POST', 'GET'])
def games() -> Union[str, Response]:
    if request.method == 'POST':
        content = request.json
        return jsonify({
            "id": uuid.uuid4(), # invite key
            "name": content['name'],
            "type": content['type']
        })
    else:
        return "All games (in the future)"

@game_bp.route('/games/<invite_key>', methods=['PUT'])
def join_game(invite_key: Optional[str] =None) -> Response:
    # todo: add logic to join to the game  in the future
    # invite_key == id
    return f"Successfully joined the game! Your invite key is: {invite_key}."
