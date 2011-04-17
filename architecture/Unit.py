from Entity import Entity
from GameData import Locals
from Overlay import HealthBar
from NaturalObject import Resource,Gold
import cPickle
from Inventory import Inventory

from collections import deque
import specialMath

import pygame

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
        self.buildQueue = []
        self.currentTask = None
        self.currentBuildTime = 0
        self.inventory=Inventory()

    def _hasResourcesToBuild(self,entityClass):
        
        for resourceClass, amount in entityClass.costToBuild:
            if not self.world.hasResources(self.owner,resourceClass,amount):
                return False
        return True

    def addToBuildQueue(self,entityClass):
        if entityClass in self.buildDict \
        and self._hasResourcesToBuild(entityClass):
            self.buildQueue.append(entityClass)
            
            for resource,cost in entityClass.costToBuild:
                self.world.removeResource(self.owner,resource,cost)

    def update(self):
        if not self.hasFullHealth():
            self.regenerate()
            
        if self.currentTask == None:
            self.nextBuildTask()
        
        if not self.currentTask == None:
            self.Build()
    
    def hasBuildTask(self):
        return len(self.buildQueue) > 0
    
    def nextBuildTask(self):
        if self.hasBuildTask():
            self.currentTask = self.buildQueue.pop(0)
        else:
            self.currentTask = None
    
    def Build(self):
        """A particular builder creates builder1 after a certain timeToBuild"""
        self.currentBuildTime += self.getTimeElapsed()/1000.0

        if self.currentBuildTime > self.currentTask.timeToBuild:
            self.buildDict[self.currentTask]()
            self.currentBuildTime = 0
            self.nextBuildTask()
	
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


class Unit(Builder):
    """A kind of Builder that can move around."""

    # Static class attribute--keeps track of all units initialized
    # by this computer (one particular player)
    #from pygame.sprite import Group
    #allUnits = Group()
    
    costToBuild = [(Gold,75)]
    
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.',loadList=None):
        Builder.__init__(self,imagePath,x,y,world,colorkey,description)
	
        #self.__class__.allUnits.add(self)
        self.imagePath=imagePath
        if loadList == None:
            self.status=Locals.IDLE
            self.efficiency={Locals.MOVE:.1, Locals.GATHER: 5, Locals. ATTACK: 10} #move, build, gather, attack
            self.path=[] #queue of future tuple destinations
            self.dest=self.realCenter=list(self.rect.center) #current destination
            self.speed=.1
            self.attackRange=300
            self.attackRechargeTime=500
            self.radius={Locals.GATHER: 100, Locals.ATTACK: 200}
            self.timeSinceLast={0:0,Locals.ATTACK:self.attackRechargeTime}
            self.objectOfAction=None
        else:
            #loadList = [status,efficiency,path,dest,speed,
            #attackRange,attackRechargeTime,radius,timeSinceLast
            #objectOfAction]
            self.status = loadList['status']
            self.efficiency = loadList['efficiency']
            self.path = loadList['path']
            self.dest = loadList['dest']
            self.speed = loadList['speed']
            self.attackRange = loadList['attackRange']
            self.attackRechargeTime = loadList['attackRechargeTime']
            self.radius = loadList['radius']
            self.timeSinceLast = loadList['timeSinceLast']
            self.objectOfAction = loadList['objectOfAction']
        
        self.regenRate = .5

    def update(self):
        """Called by game each frame to update object."""
        #FIXME !!!
        if not self.hasFullHealth():
            self.regenerate()
        if self.status==Locals.MOVING:
            self.move()
        else: self.path=[]
        if self.status==Locals.ATTACKING:
            self.attack()
        elif self.status==Locals.GATHERING:
            if not self.inventory.isFull():
                self.gather()
            else:
				self.status=Locals.IDLE
				self.objectOfAction=None
        self.timeSinceLast[Locals.ATTACK]+=self.getTimeElapsed()

    def attack(self):
        """Moves unit such that enemy is within range and attacks it"""
        closest=specialMath.findClosest(self.realCenter, self.objectOfAction.realCenter, self.worldSize)
        self.dest=closest
        if specialMath.distance(self.realCenter, self.dest) > self.radius[Locals.ATTACK]:
            self.move() 
        elif self.timeSinceLast[Locals.ATTACK]>=self.attackRechargeTime:
            self.objectOfAction.changeHealth(-1*self.efficiency[Locals.ATTACK])
            self.timeSinceLast[Locals.ATTACK]=0
        if self.objectOfAction.curHealth<=0:
            self.status=Locals.IDLE
            self.dest=self.realCenter

    def gather(self):
        """moves unit close to resource, adds resource to containment"""
        if specialMath.distance(self.realCenter, self.dest) > self.radius[Locals.GATHER]:
            self.move()
        else:
            amount = self.inventory.add(self.objectOfAction,self.efficiency[Locals.GATHER])
        
            if amount == 0:
                self.status = Locals.IDLE
                self.dest=self.realCenter
            else:
                self.objectOfAction.changeHealth(-1*amount)
                self.timeSinceLast[Locals.ATTACK]=0 
        
    def initAction(self, obj): 
        """
        Initialized appropriate action by setting dest and status given the type of entity.
        """
        self.objectOfAction=obj
        closest=specialMath.findClosest(self.realCenter, self.objectOfAction.rect.center, self.worldSize)
        self.dest=closest
        if isinstance(obj, Builder):#Unit):
            self.status=Locals.ATTACKING
        elif isinstance(obj, Resource): 
            self.status=Locals.GATHERING
            
    def move(self):
        """changes position of unit in direction of dest"""
        
        # Decides what the current self.dest should be
        self._definePath()
        if not self.status == Locals.IDLE:
            curX,curY = self.realCenter
            
            # difference between destination and current location
            dirx = self.dest[0] - curX #unscaled x direction of movement
            diry = self.dest[1] - curY #unscaled y direction of movement
            
            # distance between destination and current location
            distLocToDest = specialMath.hypotenuse(dirx,diry)
            
            # Unit vector of velocity
            dirx /= distLocToDest #unit x direction of movement
            diry /= distLocToDest #unit y direction of movement
            #print dirx, diry, (dirx**2 + diry**2)
            
            
            newX = curX + dirx*self.speed*self.getTimeElapsed()
            newY = curY + diry*self.speed*self.getTimeElapsed()
            
            #print 'Dir info: ',curX,curY,newX,newY
            #print 'Dest info: ',self.dest
            
            #if specialMath.hypotenuse(newX-curX,newY-curX) > distLocToDest:
            #    self.rect.center = self.dest
            #else:
            #    self.rect.center = newX, newY
            self.realCenter = [newX,newY]
            self.rect.center = tuple(self.realCenter)
            self.moveWrap()
            
    def _definePath(self):
        if self._isAtDestination(): #may need to have room for error
            if self.path == []:
                self.status = Locals.IDLE
                self.dest = self.realCenter
                return
            else: # path not empty - change path
                self.status = Locals.MOVING
                self.dest = self._optimalDestination()
        else: # Not at current destination
            pass
    
    def _isAtDestination(self, margin=2):
        if self.status == Locals.IDLE:
            return True
        return specialMath.distance(self.realCenter,self.dest) <= margin
    
    def _optimalDestination(self):
        """
        Returns the optimal destination given the current location
        of the unit and the desired end point.  Returns None if none
        is found.
        """
        destX,destY = self.path.pop(0) 
        
        # Rectangle the size of the world which is centered
        # at the current location
        return specialMath.findClosest(self.realCenter, (destX, destY), self.worldSize)
    
    def moveWrap(self):
        """
        Wraps the position of the unit in the world according to the 
        size of the world in pixels.  Both the position and the 
        destination point wrap if the grid boundary is crossed.
        """
        if self.entityID == 1:
            print self.realCenter, self.dest

        for i in xrange(2):
            if not 0<self.realCenter[i]<self.worldSize[i]:
                newVal=self.realCenter[i]%self.worldSize[i]
                di = self.dest[i]-self.realCenter[i]+newVal
                self.realCenter[i]=newVal
                self.dest[i]=di
            
        self.rect.center = tuple(self.realCenter)
    
    def addToPath(self,coord):
        """
        Takes an x,y coordinate tuple in the grid and adds this location
        to the path.
        """
        self.path.append(list(coord))
        
    def getMiniMapColor(self):
        return (20,20,255)
    def __str__(self):
        return cPickle.dumps(['Unit', self.imagePath, self.realCenter, 'world'])
    def __getstate__(self):
        d=dict()
        d['imagePath']=self.imagePath
        d[positio]
        pass#return a dict
    def __setstate__(self,dict):
        pass        


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
    for i in xrange(50):
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
