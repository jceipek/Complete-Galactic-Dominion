class InputDeviceMastermind(object):
    '''
    Attributes:
        scrollPosition
        cursorPosition
        dictionary(String:Boolean)
    '''
    def __init__(self):
        scrollPosition=cursorPosition=0\
        state=dict()

    def updateState(command,value=None)
        '''
        Takes a string and updates the state
        '''
        if value==None:
            state[command]= not state.get(command,False)
        elif isinstance(value,bool):
            state[command]=value
        else
            state[command]=value
