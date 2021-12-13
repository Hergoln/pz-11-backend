import abc
from uuid import UUID

class Player(metaclass=abc.ABCMeta):
    '''
    Defines a basic player structure with identificator.
    '''

    def __init__(self, uuid: UUID):
        self.uuid = uuid
        self.is_defeated = False
        

class Spectator(metaclass=abc.ABCMeta):
    '''
    Defines a basic spectator structure with identificator.
    '''

    def __init__(self, uuid: UUID, name: str):
        self.uuid = uuid
        self.name = name
