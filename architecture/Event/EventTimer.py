import time

class EventTimer(object):
    """
    This object is in charge of always knowing what time it is
    with respect to server-client synchronization
    """
    
    def getTime(self):
        #THIS FUNCTION IS NOWHERE NEAR BEING IMPLEMENTED PROPERLY
        return time.time()