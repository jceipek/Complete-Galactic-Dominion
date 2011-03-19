class Player(object):
    """
    A Player object contains all of the information needed for entity
    ownership and functions associated with an individual and all of their
    units.
    """
    
    def __init__(self,identifier):
        #Identifier, probably username
        self.id = identifier
