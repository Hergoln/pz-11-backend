class CommunicationHandler:
    def __init__(self, websocket_handler):
        # TODO assign callback onReceive to websocket
        self.websocket_handler = websocket_handler

    def on_receive(self, message):
        self._incoming_messages.append(message)

    def push_message(self, message):
        print("Communication handler: send message", message)
        self.websocket_handler.send(message)

    def on_disconnect(self, message):
        print("Communication handler: on diconnect")
        
    def on_connect(self, message):
        print("Communication handler: on connect")
