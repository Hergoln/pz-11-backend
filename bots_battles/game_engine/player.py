import abc
from uuid import UUID

class Player(metaclass=abc.ABCMeta):
    def __init__(self, uuid: UUID):
        self.uuid = uuid