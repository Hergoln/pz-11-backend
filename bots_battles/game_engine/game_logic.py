import abc

class GameLogic(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def applyRules(self, message):
        pass
