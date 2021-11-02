from flask import request, jsonify, Blueprint
import uuid
from bots_battles.games.game_factory import GameFactory

game_factory = GameFactory() # think about it
game_bp = Blueprint("game", __name__)

@game_bp.route('/games/types/')
def game_types():
    return jsonify({ 'game_types': list(game_factory.get_all_games()) })

@game_bp.route('/games/', methods=['POST', 'GET'])
def games():
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
def join_game(invite_key: None):
    # todo: add logic to join to the game  in the future
    # invite_key == id
    return f"Successfully joined the game! Your invite key is: {invite_key}."
