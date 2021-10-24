from game_engine.game_logic import GameLogic


class AgarntGameLogic(GameLogic):
    def apply_rules(self, message):
        print(f'agarnt game logic, {message}')

    def get_state(self):
        return ""