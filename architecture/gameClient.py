import networking
from Listener import Listener
import Event

class GameClient(networking.Client,Listener):
    """
    Forewards WorldManipulationEvents to the game server
    and responds to WorldManipulationEvents sent by the server
    """
    def __init__(self,manager,host = 'localhost',port = 51423):
        networking.Client.__init__(self,host,port)
        print self.socketThread
        eventTypes = [Event.WorldManipulationEvent]
        Listener.__init__(self,manager,eventTypes)
        
    def processInput(self,sockThrd,data):
        event = Event.EventExecutionEvent(data)
        self.manager.post(event)
        
    def notify(self,evt):
        evtString = evt.toPacket()
        self.sendRequest(evtString)
