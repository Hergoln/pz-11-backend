from queue import Queue
from threading import Lock

class CommunicationHandler:
    def __init__(self) :
        self.__incomming_messages_lock = Lock()
        self.__incoming_messages = Queue()

    def on_receive(self, message):
        print("Communication handler: receive message", message)
        with self.__incomming_messages_lock:
            self.__incoming_messages.append(message)

    def handle_incomming_messages(self, fun):
        with self.__incomming_messages_lock:
            while not self.__incoming_messages.empty():
                fun(self.__incoming_messages.get())

    # def push_message(self, message):
    #     print("Communication handler: send message", message)

    # def on_disconnect(self, message):
    #     print("Communication handler: on diconnect")
        
    # def on_connect(self, message):
    #     print("Communication handler: on connect")

