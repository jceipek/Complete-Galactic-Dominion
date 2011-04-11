#import time
import datetime

class EventTimer(object):
    """
    This object is in charge of always knowing what time it is
    with respect to server-client synchronization
    """
    
    def getTime(self):
        #Will return the system time in microseconds
        #On Windows, will only be accurate to ms level

        now = datetime.datetime.now()
        y = int(now.year * 3.1536*10**13)
        m = int(now.month * 2.628 * 10**12)
        d = int(now.day * 8.64*10**10)
        h = int(now.hour * 3.6*10**9)
        now = datetime.datetime.now()
        s = int(now.second * 10.0**6)
        now = datetime.datetime.now()
        m = now.microsecond
        return y+m+d+h+s+m