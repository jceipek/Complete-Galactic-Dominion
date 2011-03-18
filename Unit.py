import Builder
import pygame
from collections import deque

class Unit(pygame.sprite.Sprite):
    """A kind of Builder that can move around."""

    # Static class attribute--keeps track of all units initialized
    # by this computer (one particular player)
    allUnits = pygame.sprite.Group()
    
    def __init__(self, imagePath, colorkey=None):
        # Will set the image and rect properties required by Sprite
        Builder.__init__(self, imagePath, colorkey)
        Unit.allUnits.add(self)

        self.status=Entity.Locals.IDLE
        self.efficiency=1
        self.path=[]#queue of future tuple destinations
        self.dest=None #current destination
        self.speed=1

    def update(self):
        """Called by game each frame to update object."""
        self.dtime()#updates time

    def kill(self):
        """Removes the current Sprite from all groups.  It will no longer
        be associated with this class."""
        pygame.sprite.Sprite.kill(self)

    def move(self):
        """changes position of unit in direction of dest"""
        if (self.x,self.y)==self.dest: #may need to have room for error
            if len(self.path)<1:
                self.status=Entity.Stats.IDLE
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
        
        
        

    def die(self):
        """removes Unit from map"""
        self.kill()
        del self #This is a guess and is probably wrong
        
