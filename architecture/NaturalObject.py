from Entity import Entity

class NaturalObject(Entity):
    """
    description: description of behavior, abilities (inherited from Entity)
    x: position (inherited from Entity)
    y: position (inherited from Entity)
    maxHealth: maximum/ default health points (inherited from Entity)
    curHealth: current health (inherited from Entity)
    size: radius of collision (inherited from Entity)
    """
    
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.'):
        Entity.__init__(self,imagePath,x,y,world,colorkey,description)
        self.blockable=True
        self.collectable=False
        self.maxHealth = self.curHealth = 0
	
    def collect(self):
        if not self.collectable:
            pass

class Resource(NaturalObject):
    """
    Object on the map which can be collected.  Health may or may 
    not regenerate over time.
    """
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.',
                 resourceName='Null'):
                     
        NaturalObject.__init__(self,imagePath,x,y,world,colorkey,description)
	
        self.maxHealth = self.curHealth = 500
        self.resourceName = resourceName
    
    def update(self):
        pass
	
    def regenerate(self):
        pass

class Gold(Resource):
    """Wrapper for Gold."""
    def __init__(self,x,y,world):
        Resource.__init__(self,'Gold-ore.png',x,y,world,(255,255,255),\
            'Gold ore.','Gold')

class Obstacle(NaturalObject):
    """
    Object on the map which is only an obstacle.  Health may or may 
    not regenerate over time.
    
    If the obstacle can never be removed, we may want to add it to the
    background set of images at the initialization of the game...
    We may not want to have to look for it each time separately from
    the background.
    """
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.'):
        NaturalObject.__init__(self,imagePath,x,y,world,colorkey,description)
	
    def update(self):
        pass

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
    for i in xrange(10):
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
