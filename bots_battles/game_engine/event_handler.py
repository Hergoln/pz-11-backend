import queue

class EventHandler:
    def __init__(self, game_logic, communication_handler):
        self.__incomingMessages = queue.Queue()
        self.__outgoingMessages = queue.Queue()
        self.__game_logic = game_logic
        self.__communication_handler = communication_handler

    def handleIncomingMessages(self):
        '''Handles a queue with incoming messages, by passing each message to game logic class and sending output message (if any) to queue with outgoing messages'''
        while not self.__incomingMessages.empty():
            for e in self.__game_logic.applyRules(self.__incomingMessages.get()):
                self.__outgoingMessages.put(e)

    def sendOutcommingMessages(self):
        '''Handles a queue with outgoing messages, by passing each message to communiation handler class instance.'''
        while not self.__outgoingMessages.empty():
            self.__communication_handler.pushMessage(self.self.__outgoingMessages.get())

    
