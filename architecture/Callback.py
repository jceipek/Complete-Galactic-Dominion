class Callback(object):
    
    def __init__(self, callback, *args):
        
        self.callback = callback
        self.args = args
        
    def execute(self):
        return self.callback(*self.args)

if __name__ == "__main__":
    a=Callback(lambda a,b: a+b,1,2)
    print a.execute()
