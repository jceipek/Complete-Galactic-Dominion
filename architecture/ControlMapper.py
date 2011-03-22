

class ControlMapper(object):
    """
    Reads from a configuration file in order to establish a control scheme.
    """
    def __init__(self):
        #Set up a dictionary of all events in the Event module.
        #This will allow the debugger to understand any event in the config file
        self.mapping = dict()
        
        setupFile = open("controlScheme.config")
        
        for line in debugFile:
            #Strip extra whitespace
            line = line.strip()
            line = line.replace(" ","")
            line = line.replace("\t","")
            
            line = line.split('#')[0]
            if len(line)>0:

                if line.find("SELECTION") == 0:
                     rem =  line[len("SELECTION"):]
                
        
        print("Control Scheme Setup:")
        if self.SYMBOLS_ENABLED:
            print("\tDebugging Enabled")
            
            if self.VERBOSE_MODE:
                print("\tVerbose Logging Active")
            
            if self.trackedEvents:
                print "\tEvents that are being tracked:"
                for event in self.trackedEvents:
                    print("\t\t"+str(event))
            else:
                print "\tNo events are being tracked."
                print "\t\tDisabling debug mode."
                self.SYMBOLS_ENABLED = False
                self.VERBOSE_MODE = False
        else:
            print("\tDebugging Disabled")
            
    def logMsg(self,event):
        if self.SYMBOLS_ENABLED and type(event) in self.trackedEvents:
            print(str(event.timeFired)+" "+str(type(event)))
            if self.VERBOSE_MODE:
                print(event.verboseInfo)