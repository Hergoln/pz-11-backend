import abc

class GameConfig(metaclass=abc.ABCMeta):
    '''Abstract class, used to define the game config.'''
    max_player_number = 10