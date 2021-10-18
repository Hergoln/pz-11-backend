import queue

class EventHandler:
    def __init__(self, game_logic, communication_handler):
        self.__incoming_messages = queue.Queue()
        self.__game_logic = game_logic
        self.__communication_handler = communication_handler

    def handleIncomingMessages(self):
        '''Handles a queue with incoming messages, by passing each message to game logic class'''
        while not self.__incoming_messages.empty():
            self.__game_logic.applyRules(self.__incoming_messages.get())

    def updateGameState(self):
        '''Get actual state of game from GameLogic class instance and pass it to communication handler'''
        self.__communication_handler.pushMessage(self.self.__game_logic.getState())

    
