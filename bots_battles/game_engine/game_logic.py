import abc

class GameLogic(metaclass=abc.ABCMeta):
    '''Abstract class which defines a rules of game.'''

    @abc.abstractmethod
    def applyRules(self, message):
        '''Abstract method where message will be parsed and all games rules will be check.'''
        pass

    @abc.abstractmethod
    def getState(self):
        '''Returns actual state of game'''
        pass
