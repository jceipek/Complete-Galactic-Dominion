import networking
from Listener import Listener
import Event

class GameClient(networking.Client,Listener):
    """
    Forewards WorldManipulationEvents to the game server
    and responds to WorldManipulationEvents sent by the server
    """
    ID = None
    def __init__(self,manager,host = 'localhost',port = 51423):
        networking.Client.__init__(self,host,port)
        print self.socketThread
        eventTypes = [Event.WorldManipulationEvent,Event.LoadGameEvent]
        Listener.__init__(self,manager,eventTypes)
        self.loaded=False
        
    def processInput(self,sockThrd,data):
        if 'newPlayer' in data:
            playerID = data.split(':')[1]
            playerID = int(playerID)
            self.manager.post(Event.NewPlayerEvent(playerID))
        elif not self.loaded and 'finishedLoading' in data:
            self.loaded = True
            self.manager.post(Event.GameLoadedEvent())
        elif self.ID == None and data[:3] == 'ID:':
            IDList = data.split(':')
            GameClient.ID = int(IDList[1])
            sockThrd.write('newPlayer:%d'%self.ID)
            self.manager.post(Event.ClientIDCollected(self.ID))
        else:
            event = Event.EventExecutionEvent(data)
            self.manager.post(event)
        
    def notify(self,evt):
        if isinstance(evt,Event.LoadGameEvent):
            print 'Loading the game'
            self.socketThread.write('GetWorld')
        elif isinstance(evt,Event.WorldManipulationEvent):
            evtString = evt.toPacket()
            self.sendRequest(evtString)
