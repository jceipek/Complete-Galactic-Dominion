"""
All debug setings can be configured with debug.config
New events added to Event.py are automagically supported
"""

import Event

class Debugger(object):
    """
    The debugger is used for debugging purposes during development.
    When it is initialized, it reads from a text file (debug.config)
    specifying options such as which events to report and whether
    extra information about these events should be reported.
    
    @param SYMBOLS_ENABLED: If this is off, the debugger will do nothing.
    @type SYMBOLS_ENABLED: bool
    
    @param VERBOSE_MODE: Turn this on to obtain additional information contained
    in an event.
    @type VERBOSE_MODE: bool
     
    @param trackedEvents: Events that the debugger will report.
    @type trackedEvents: [*L{Event}.*]
    """
    
    def __init__(self):
    
        #Set up a dictionary of all events in the Event module.
        #This will allow the debugger to understand any event in the config file
        import Event
        events = dict()
        for name in dir(Event):
            obj = getattr(Event, name)
            if '<class' in str(obj):
                eventName = str(obj).split('.')[-1].replace("'>","")
                events[eventName] = obj
        
        self.SYMBOLS_ENABLED = False
        self.VERBOSE_MODE = False
        self.trackedEvents = []
        
        try:
            debugFile = open("debug.config")
                
            for line in debugFile:
                #Strip extra whitespace
                line = line.strip()
                line = line.replace(" ","")
                line = line.replace("\t","")
                
                line = line.split('#')[0]
                if len(line)>0:
                    dmode = "SYMBOLS_ENABLED="
                    vmode = "VERBOSE_MODE="
                    etrack = "Event."
                    if line.find(dmode) == 0:
                         if line[len(dmode):] == "True":
                            self.SYMBOLS_ENABLED = True
                         elif line[len(dmode):] == "False":
                            self.SYMBOLS_ENABLED = False
                    elif line.find(vmode) == 0:
                         if line[len(vmode):] == "True":
                            self.VERBOSE_MODE = True
                         elif line[len(vmode):] == "False":
                            self.VERBOSE_MODE = False
                    elif line.find(etrack) == 0:
                         if line[len(etrack):] in events:
                           self.trackedEvents.append(events[line[len(etrack):]])
        except:
            pass
        print("Debugging Setup:")
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
        """
        
        """
        if self.SYMBOLS_ENABLED and type(event) in self.trackedEvents:
            print(str(event.timeFired)+" "+str(type(event)))
            if self.VERBOSE_MODE:
                print(event.verboseInfo)