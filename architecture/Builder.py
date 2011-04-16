from Entity import Entity

class Builder(Entity):
    """
    A kind of entity that can create things (units or structures).
    Attributes:
    description: description of behavior, abilities (inherited from Entity)
    x: position (inherited from Entity)
    y: position (inherited from Entity)
    maxHealth: maximum/ default health points (inherited from Entity)
    curHealth: current health (inherited from Entity)
    size: radius of collision (inherited from Entity)
    
    ---------------------methods inherited from SuperClasses
    die(self): entity is removed from map
    changeHealth(self, numHits): decreases the health of the entity based 
	on number of hits
	
    """
    
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.'):
		     
	Entity.__init__(self,imagePath,x,y,world,colorkey,description)
	
	self.blockable=True
	
	# Dictionary which maps from strings defining units which can
	# be produced by a builder to callbacks
	self.buildDict={}
	
	# Queue of entities to build
	self.buildQueue=[]

    def Build(self):
	"""A particular builder creates builder1 after a certain timeToBuild"""
	buildQueue = self.buildQueue
	if len(buildQueue) > 0:
	    entityToBuild = buildQueue.pop(0)
	# CURRENTLY A STUB
	
    def buildOptions(self):
	"""
	Returns list of class options from self.buildDict.
	"""
	return self.buildDict.keys()
	
    def buildOptionChoice(self,choice):
	"""
	Returns the callback of the Builder constructor called for by
	choice.  This choice can be obtained from self.buildOptions().
	
	@param choice: string as key for self.buildDict
	"""
	return self.buildDict.get(choice,None)


if __name__ == "__main__":
    
    import pygame
    # TESTS TO SHOW ENTITIES WORK
    
    screenSize = (width, height) = (1024, 768)
    screenLoc = [0.0, 0.0]
    
    from World import World

    RUNNING = True
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    screenZone = screen.get_rect()

    w = World()
    print 'World initialized'
    
    # Creates entities to test with in world w
    for i in range(10):
        w.addEntity(Entity('ball.png',i*50,i*50, w, (255,255,255)))
        #print Entity.IDcounter
    
    MAX_FPS = 60
    gameClock = pygame.time.Clock()
    pygame.init()
    
    while RUNNING:
        
        # calls update function of all Entities in world
        w.update()
        
        screen.fill((0,0,0))
        
        # Grabs all entities that are currently on the screen from the 
        # world
        curScreenEntities = w.getScreenEntities(screenZone)
        #print 'Currently %d entities on the screen'%len(curScreenEntities)
        
        for ent in w.allEntities.values():
            
            ent.draw(screen)
            
        pygame.display.flip()
        
        ms_elapsed = gameClock.tick(MAX_FPS)
        print 'Current frames per second: %d'%int(1000.0/ms_elapsed)
