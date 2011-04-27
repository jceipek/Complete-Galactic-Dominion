"""
NOT CURRENTLY IMPLEMENTED IN CGD.
"""

class InputDeviceMastermind(object):
    """
    Will map from input device to action, read from a configuration file.
    Not currently implemented (lacks this functionality).
    
    Attributes:
        scrollPosition
        cursorPosition
        dictionary(String:Boolean)
    """
    def __init__(self):
        scrollPosition=cursorPosition=0
        self.state=dict()

    def updateState(self,command,value=None):
        """
        Takes a string and updates the state
        """
        if value==None:
            self.state[command]= not self.state.get(command,False)
        elif isinstance(value,bool):
            self.state[command]=value
        else:
            self.state[command]=value
