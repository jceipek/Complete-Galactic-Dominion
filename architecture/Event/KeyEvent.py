from Event import Event

class KeyLocals:
    DOWN = 0
    UP = 1

class NumberKeyPressEvent(Event):
    
    def __init__(self,key,state,comboKeys):
        Event.__init__(self)
        self.key = key
        self.state = state
        self.comboKeys = comboKeys
        self.verboseInfo = "\tKey pressed: " + str(key) + "\n"
