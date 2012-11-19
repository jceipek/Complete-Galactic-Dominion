from Event import WorldManipulationEvent

class Callback():
    """
    Performs a basic, one operation callback with a variable length
    argument list.
    """
    def __init__(self, callback, *args):
        
        self.callback = callback
        self.args = args
        
    def execute(self):
        """
        Executes the callback and returns the results.
        """
        return self.callback(*self.args)

class GroupCallback(Callback):
    """
    Performs a list of callbacks with the same variable length
    argument list.
    """
    def __init__(self, callbackList, *args):
        
        self.callback = callbackList
        self.args = args
        
    def execute(self):
        """
        Executes the callbacks and returns the results in a list.
        """
        results = []
        
        for callback in self.callback:
            results.append(callback(*self.args))
        
        return results

class SeriesCallback(Callback):
    """
    Performs a series of callbacks in which the variable length
    argument list is passed to the first callback, and the result
    of the first callback is passed to the next callback in the list,
    and so on.  The result of the final callback is returned in the 
    form of a list.
    """
    def __init__(self, callback, *args):
        
        self.callback = [callback]
        self.args = args
        
    def addCallback(self,newCallback):
        """
        Adds a new callback to the chain of callbacks.
        """
        self.callback.append(newCallback)
        
    def execute(self):
        """
        Executes the callbacks and returns the result of the final
        callback in the form of a list.
        """
        args = self.args
        
        for callNumber in xrange(len(self.callback)):
            args = (self.callback.pop(0))(*args)
            
            if not (isinstance(args,tuple) or isinstance(args,list)):
                args = [args]
        
        return args

class ParallelCallback(Callback):
    """
    Performs multiple callbacks in the order given, each with
    a separate argument list.  The results of all callbacks are
    returned.
    """
    def __init__(self, callback, *args):
        
        self.callback = [callback]
        self.args = [args]
        
    def addCallback(self,newCallback,*newArgs):
        """
        Adds a new callback to the chain or callbacks.  It will be 
        called with the supplied variable length argument list.
        """
        self.callback.append(newCallback)
        self.args.append(newArgs)
        
    def execute(self):
        """
        Executes the callbacks and returns the results in a list.
        """
        results = []

        for callNumber in xrange(len(self.callback)):
            results.append( (self.callback.pop(0))(*self.args.pop(0)) )

        return results

def networkClassCreator(className,*args):
    """
    Creates a world manipulation event which will create an instance
    of the given class with the given arguments if received by
    the server.
    """

    print 'In networkClassCreator: ',args
    return WorldManipulationEvent(['create',className,args])

if __name__ == "__main__":

    """
    Testing callbacks...
    """

    def printSomething(myStr,astr):
        print myStr + astr

    a=Callback(printSomething,'Berit', 'Yo')
    a.execute()

    class A(object):
        def myMethod(self,num):
            return num
    
    class B(object):
    
        def __init__(self):
            self.x = 'IBETTERWORK'
            self.y = 'blahblah'
        
        def myMethod(self,t='I',s=' worked.  woo.'):
            print t+s
    
    a = [A(),A()]
    
    aCalls = []
    for item in a:
        aCalls.append(item.myMethod)
    
    test = GroupCallback(aCalls,999)
    print test.execute()
    
    def giveAnumber():
        return 100
        
    def printAnumber(n):
        print 'Your number is: %d'%n
    
    seriesTest=SeriesCallback(giveAnumber)
    seriesTest.addCallback(printAnumber)
    seriesTest.execute()
    
    seriesTest2=SeriesCallback(B)
    print seriesTest2.callback[0]
    x = 'test'
    seriesTest2.addCallback(lambda b: b.myMethod(x,b.y))
    seriesTest2.execute()
    
    parallelTest=ParallelCallback(giveAnumber)
    parallelTest.addCallback(printAnumber,50)
    
    #import pickle
    #pickle.loads(pickle.dumps(parallelTest)).execute()
    
    parallelTest.execute()
