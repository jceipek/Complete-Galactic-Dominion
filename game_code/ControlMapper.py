"""
NOT CURRENTLY IMPLEMENTED IN CGD.
"""

class ControlMapper(object):
    """
    Reads from a configuration file in order to establish a control scheme.
    """
    
    def eventForString(astr):
        import Event

    def pygameEventForString(astr):
        import pygame
        if astr == "LEFT_CLICK":
            return [pygame.MOUSEBUTTONDOWN,]
    
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
        
