class Callback(object):
    
    def __init__(self, callback, *args):
        
        self.callback = callback
        self.args = args
        
    def execute(self):
        return self.callback(*self.args)

class GroupCallback(object):
    
    def __init__(self, callbackList, *args):
        
        self.callbackList = callbackList
        self.args = args
        
    def execute(self):
        
        results = []
        
        for callback in self.callbackList:
            results.append(callback(*self.args))
        
        return results

if __name__ == "__main__":
    a=Callback(lambda a,b: a+b,1,2)
    print a.execute()

    class A(object):
        def myMethod(self):
            return 1
    
    a = [A(),A()]
    
    aCalls = []
    for item in a:
        aCalls.append(item.myMethod)
    
    test = GroupCallback(aCalls)
    print test.execute()
