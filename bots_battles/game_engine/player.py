import abc
from uuid import UUID

class Player(metaclass=abc.ABCMeta):
    '''
    Defines a basic player structure with identificator.
    '''

    def __init__(self, uuid: UUID):
        self.uuid = uuid