from Builder import Builder
from Entity import Entity,Locals

from collections import deque

class Unit(Builder):
    """A kind of Builder that can move around."""

    # Static class attribute--keeps track of all units initialized
    # by this computer (one particular player)
    from pygame.sprite import Group
    allUnits = Group()
    
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.'):
        Builder.__init__(self,imagePath,x,y,world,colorkey,description)
	
        self.__class__.allUnits.add(self)

        self.status=Locals.IDLE
        self.efficiency=1
        self.path=[]#queue of future tuple destinations
        self.dest=None #current destination
        self.speed=1

    def update(self):
        """Called by game each frame to update object."""
        #FIXME !!!
        #self.dtime()#updates time
        pass
        
    def move(self):
        """changes position of unit in direction of dest"""
        if (self.x,self.y)==self.dest: #may need to have room for error
            if len(self.path)<1:
                self.status=Locals.IDLE
                return 
            else:
                self.dest=self.path.popleft()
                
        dirx=self.dest[0]-self.x #unscaled x direction of movement
        diry=self.dest[1]-self.y #unscaled y direction of movement
        mag=pow(dirx**2+diry**2, .5) #magnitude of unscaled direction
        dirx/=mag #unit x direction of movement
        diry/=mag #unit y direction of movement

        #sets new position based on direction, speed, frame rate
        self.x+=dirx*self.speed*self.timePassed
        self.y+=diry*self.speed*self.timePassed

def cartToiso(coord):
    return coord[0]+coord[1],-.5*coord[0]+.5*coord[1]
     
if __name__ == "__main__":
    
    # TESTS TO SHOW Builders WORK
    
    screenSize = (width, height) = (1024, 768)
    screenLoc = [0.0, 0.0]
    
    import pygame
    
    from World import World

    RUNNING = True
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    screenZone = screen.get_rect()

    w = World()
    print 'World initialized'
    
    # Creates entities to test with in world w
    for i in range(50):
        w.addEntity(Unit('ball.png',i*50,i*50, w, (255,255,255)))
        #print Entity.IDcounter
    
    MAX_FPS = 60
    gameClock = pygame.time.Clock()
    pygame.init()
    
    testRect = pygame.Rect((0,0,200,100))
    
    trect = testRect
    left,top = trect.topleft
    right,bottom = trect.bottomright
    
    print cartToiso((left,top))
    print cartToiso((right,top))
    print cartToiso((right,bottom))
    print cartToiso((left,bottom))

    while RUNNING:
        
        # calls update function of all Entities in world
        w.update()
        
        screen.fill((0,0,0))
        
        # Grabs all entities that are currently on the screen from the 
        # world
        curScreenEntities = w.getScreenEntities(screenZone)
        
        for ent in w.getScreenEntities(screenZone):
            
            ent.draw(screen)
            
        pygame.display.flip()
        
        ms_elapsed = gameClock.tick(MAX_FPS)
        #print 'Current frames per second: %d'%int(1000.0/ms_elapsed)
