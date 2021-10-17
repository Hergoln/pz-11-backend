class CommunicationHandler:
    def __init__(self, websocketHandler):
        # TODO assign callback onReceive to websocket
        self._websocketHandler = websocketHandler

    def onReceive(self, message):
        self._incomingMessages.append(message)

    def pushMessage(self, message):
        print("Communication handler: send message", message)
        self._websocketHandler.send(message)

    def onDisconnect(self, message):
        print("Communication handler: on diconnect")
        
    def onConnect(self, message):
        print("Communication handler: on connect")
