"""
All debug setings can be configured with debug.config
This file must simply be updated every time a new
debugable event or debug option is added to the program.
"""

import Event

class Debugger(object):
    """
    #Attributes:
    #   SYMBOLS_ENABLED
    #   VERBOSE_MODE
    #   trackedEvents
    """
    
    def __init__(self):
        self.SYMBOLS_ENABLED = False
        self.VERBOSE_MODE = False
        self.trackedEvents = []
        
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
                     if line[len(etrack):] == "MouseClickedEvent":
                        self.trackedEvents.append(Event.MouseClickedEvent)
                     elif line[len(etrack):] == "QuitEvent":
                        self.trackedEvents.append(Event.QuitEvent)
                     elif line[len(etrack):] == "GenericDebugEvent":
                        self.trackedEvents.append(Event.GenericDebugEvent)
                     elif line[len(etrack):] == "StartEvent":
                        self.trackedEvents.append(Event.StartEvent)
                     elif line[len(etrack):] == "RenderEvent":
                        self.trackedEvents.append(Event.RenderEvent)
                     elif line[len(etrack):] == "RefreshEvent":
                        self.trackedEvents.append(Event.RefreshEvent)
                     elif line[len(etrack):] == "UpdateEvent":
                        self.trackedEvents.append(Event.UpdateEvent)
                        
                     #ADD MORE EVENTS HERE
        
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
        if self.SYMBOLS_ENABLED and type(event) in self.trackedEvents:
            print(type(event))
            if self.VERBOSE_MODE:
                print(event.verboseInfo)