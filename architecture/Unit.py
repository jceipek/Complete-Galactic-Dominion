from Builder import Builder
from Entity import Entity
from GameData import Locals
from Overlay import HealthBar

from collections import deque
import specialMath

import pygame

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
        self.path=[] #queue of future tuple destinations
        self.dest=self.rect.center #current destination
        self.speed=.1
        self.attackRange=300
        self.attackRechargeTime=500
        self.timeSinceAttack=self.attackRechargeTime
        self.objectOfAction=None

    def update(self):
        """Called by game each frame to update object."""
        #FIXME !!!
        if self.status==Locals.MOVING:
            self.move()
        else:
            self.path=[]
            self.dest=self.rect.center
        if self.status==Locals.ATTACKING:
            self.attack(self.objectOfAction)
        self.timeSinceAttack+=self.getTimeElapsed()

    def attack(self, enemy, strength=10):
        """Moves unit such that enemy is within range and attacks it"""
        if specialMath.distance(self.rect.center, enemy.rect.center) > self.attackRange: #FIXME for somereason it works, but I don't know why

            self.dest=enemy.rect.center #FIXME pathfinding goes here
            self.move() 
        elif self.timeSinceAttack>=self.attackRechargeTime:
            enemy.changeHealth(-1*strength)
            self.timeSinceAttack=0

    def initAttack(self, enemy):
        print 'ATTACK'
        self.status=Locals.ATTACKING
        self.objectOfAction=enemy
            
        
    def move(self):
        """changes position of unit in direction of dest"""
        
        # Decides what the current self.dest should be
        self._definePath()
        
        if not self.status == Locals.IDLE:
            curX,curY = self.rect.center
            
            # difference between destination and current location
            dirx=self.dest[0]-curX #unscaled x direction of movement
            diry=self.dest[1]-curY #unscaled y direction of movement
            
            # distance between destination and current location
            distLocToDest = specialMath.hypotenuse(dirx,diry)
            
            # Unit vector of velocity
            dirx/=distLocToDest #unit x direction of movement
            diry/=distLocToDest #unit y direction of movement
            
            
            newX = curX + dirx*self.speed*self.getTimeElapsed()
            newY = curY + diry*self.speed*self.getTimeElapsed()
            
            #print 'Dir info: ',curX,curY,newX,newY
            #print 'Dest info: ',self.dest
            
            #if specialMath.hypotenuse(newX-curX,newY-curX) > distLocToDest:
            #    self.rect.center = self.dest
            #else:
            #    self.rect.center = newX, newY
            self.rect.center=newX,newY
            
    def _definePath(self):
        if self._isAtDestination(): #may need to have room for error
            if self.path == []:
                self.status = Locals.IDLE
                self.dest = self.rect.center
                return
            else: # path not empty - change path
                self.status = Locals.MOVING
                self.dest = self._optimalDestination()
                #print self.dest
        else: # Not at current destination
            pass
    
    def _isAtDestination(self, margin=2):
        if self.status == Locals.IDLE:
            return True
        return specialMath.distance(self.rect.center,self.dest) <= margin
    
    def _optimalDestination(self):
        """
        Returns the optimal destination given the current location
        of the unit and the desired end point.  Returns None if none
        is found.
        """
        destX,destY = self.path.pop(0)
        
        # Rectangle the size of the world which is centered
        # at the current location
        worldRect = pygame.Rect((0,0),self.worldSize)
        worldRect.center = self.rect.center
        
        for xShift in [0,-1,1]:
            for yShift in [0,-1,1]:
                
                testPoint = (destX+xShift*self.worldSize[0], \
                            destY+yShift*self.worldSize[1])
                #print 'Test Point: ',xShift,yShift,testPoint            
                if worldRect.collidepoint(testPoint):
                    return testPoint
        
        return None
    
    def moveWrap(self):
        """
        Wraps the position of the unit in the world according to the 
        size of the world in pixels.  Both the position and the 
        destination point wrap if the grid boundary is crossed.
        """
        if self.rect.left > self.worldSize[0]:
            self.rect.left = self.rect.left%self.worldSize[0]
            self.dest[0] = self.dest[0]%self.worldSize[0]
        if self.rect.top > self.worldSize[1]:
            self.rect.top = self.rect.top%self.worldSize[1]
            self.dest[1] = self.dest[1]%self.worldSize[1]
    
    def addToPath(self,coord):
        """
        Takes an x,y coordinate tuple in the grid and adds this location
        to the path.
        """
        
        self.path.append(coord)

if __name__ == "__main__":
    
    # BROKEN!
    
    screenSize = (width, height) = (1024, 768)
    screenLoc = [0.0, 0.0]
    
    import pygame
    
    from World import World
    import specialMath

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
    
    print specialMath.cartToIso((left,top))
    print specialMath.cartToIso((right,top))
    print specialMath.cartToIso((right,bottom))
    print specialMath.cartToIso((left,bottom))

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
