from Entity import Entity
from GameData import Locals
from Overlay import HealthBar
from NaturalObject import Resource,Gold
import cPickle
from Inventory import Inventory

from collections import deque
import specialMath

from Callback import Callback
from Event import NotificationEvent

#import pygame

class BuildTask(object):
    """
    Used by Builders in the self.buildQueue list to build things.
    """
    
    def __init__(self, buildClass, callback):
        """
        BuildTask containing a class of entity to be built and a 
        callback which will build the entity.
        
        Precondition: callback is of class Callback.
        """
        object.__init__(self)
        
        self.buildClass = buildClass
        self.callback = callback
        self.timeToBuild = self.buildClass.timeToBuild
        self.buildTime = 0
        
    def execute(self):
        """
        Runs the contained Callback, and returns the result.
        Can only be called once.  This allows for groups to work
        on the same BuildTask without its Callback being fired twice.
        """
        if self.callback is not None:
            callbackReturn = self.callback.execute()
        else:
            return None
        self.callback = None
        return callbackReturn
        
    def addTime(self,time):
        self.buildTime+=time
        
    def isReady(self):
        return self.buildTime >= self.timeToBuild

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
                 description = 'No information available.', movable=False, owner='tmp'):
             
        Entity.__init__(self,imagePath,x,y,world,colorkey,description, movable,
            owner)
        
        self.blockable=True
        
        # Dictionary which maps from strings defining units which can
        # be produced by a builder to callbacks
        self.buildDict={}
        
        # Queue of entities to build
        self.buildQueue = []
        self.currentTask = None
        self.inventory=Inventory()
        
        # first to define these attributes
        # sets where a new entity should be constructed
        self.buildX,self.buildY = self.rect.center

    def _hasResourcesToBuild(self,entityClass):
        
        for resourceClass, amount in entityClass.costToBuild:
            if not self.world.hasResources(self.owner,resourceClass,amount):
                return False
        return True

    def addToBuildQueue(self,entityClass,buildPos=None,callback=None):
        
        if buildPos is None:
            self.buildX,self.buildY = self.rect.center
        else:
            self.buildX,self.buildY = buildPos

        if entityClass in self.buildDict:
            if self._hasResourcesToBuild(entityClass):    
                self.addNotification(NotificationEvent(
                    'Building %s in %1.2f seconds.'%(entityClass.name,entityClass.timeToBuild)
                    ))
                
                if callback is None:
                    self.buildQueue.append(
                        BuildTask(entityClass,
                            Callback(self.buildDict[entityClass],self.buildX,self.buildY))
                        )
                else:
                    self.buildQueue.append(
                        BuildTask(entityClass,callback)
                    )
        
                for resource,cost in entityClass.costToBuild:
                    self.world.removeResource(self.owner,resource,cost)
            else:
                self.addNotification(NotificationEvent(
                    'You do not have sufficient resources to build a %s.'%entityClass.name))
        else:
            msg='%s cannot build %s,'%(self.name,entityClass.name)
            msg+=' but can build:'
            for option in self.buildDict:
                msg+=' %s,'%option.name
            self.addNotification(NotificationEvent(msg[:-1]+'.'))

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

        self.currentTask.addTime(self.getTimeElapsed()/1000.0)
        
        if self.currentTask.isReady():
            self.currentTask.execute()
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
    
    name = 'Unit'
    
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.',
                 owner='tmp'):
        Builder.__init__(self,imagePath,x,y,world,colorkey,description,
            owner='tmp', movable=True)
    
        #self.__class__.allUnits.add(self)
        if True:#loadList == None:
            self.status=Locals.IDLE
            self.efficiency={Locals.MOVE:.1, Locals.GATHER: 5, Locals.ATTACK: 10} #move, build, gather, attack
            self.path=[] #queue of future tuple destinations
            self.dest=self.realCenter=list(self.rect.center) #current destination
            self.speed=.1
            self.attackRange=300
            self.attackRechargeTime=500
            self.radius={Locals.GATHER: 100, Locals.ATTACK: 200}
            self.timeSinceLast={0:0,Locals.ATTACK:self.attackRechargeTime}
            self.objectOfAction=None
        '''
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
            '''
        
        self.regenRate = .5        
        from Structure import TestTownCenter
        self.buildDict = {
            TestTownCenter:
                lambda x,y : 
                    TestTownCenter(x, y, self.world, self.owner)
            }

    def __getstate__(self):
        print 'In Unit get state'
        state = self.__dict__.copy()
        
        if self.world != None:
            state['world'] = self.world.worldID
            
        if state['image'] != None:
            del state['image']
            
        if hasattr(state['objectOfAction'],'entityID'):
            state['objectOfAction'] = state['objectOfAction'].entityID
        
        del state['healthBar']
        
        for attr in state:
            print attr
            print state[attr].__class__ 
            print       
        return state
        
    def __setstate__(self,state):
        print "In Unit set state"
        self.__dict__ = state
            
        self.loadImage(self.imagePath, self.colorkey)
        self.rect.center = self.realCenter

    def update(self):
        """Called by game each frame to update object."""
        #FIXME !!!
        if not self.hasFullHealth():
            self.regenerate()
        if self.status==Locals.MOVING:
            self.move()
        elif self.status==Locals.IDLE:
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
        if self.currentTask == None:
            self.nextBuildTask()
        
        if not self.currentTask == None:
            self.Build()

    def attack(self):
        """Moves unit such that enemy is within range and attacks it"""
        if self.moveCloseToObject(self.radius[Locals.ATTACK]) and self.timeSinceLast[Locals.ATTACK]>=self.attackRechargeTime:
            self.objectOfAction.changeHealth(-1*self.efficiency[Locals.ATTACK])
            self.timeSinceLast[Locals.ATTACK]=0
        if self.objectOfAction.curHealth<=0:
            self.status=Locals.IDLE
            self.dest=self.realCenter

    def gather(self):
        """moves unit close to resource, adds resource to containment"""
        if self.moveCloseToObject(self.radius[Locals.GATHER]):
            amount = self.inventory.add(self.objectOfAction,self.efficiency[Locals.GATHER])
            if amount > self.objectOfAction.curHealth:
                amount=self.objectOfAction.curHealth
        
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
        if isinstance(obj, Builder):#Unit):
            self.status=Locals.ATTACKING
        elif isinstance(obj, Resource): 
            self.status=Locals.GATHERING

    def moveCloseToObject(self,radius):
        """
        Moves unit within specified radius of objectOfAction. Returns True if within radius, False if otherwise
        """
        closest=specialMath.findClosest(self.realCenter, self.objectOfAction.realCenter, self.worldSize)
        self.dest=closest
        if specialMath.distance(self.realCenter, self.dest) > radius:
            self.move()
            return False
        else: return True
            
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
        print self.path
        
    def getMiniMapColor(self):
        return (20,20,255)
        
    def __str__(self):
        return cPickle.dumps(['Unit', self.imagePath, self.realCenter, 'world'])

class TestUnit(Unit):
    """Defines implementation of a unit."""
    
    name = 'TestUnit'
    
    def __init__(self, x, y, world, owner='tmp'):
        Unit.__init__(self,'testCraft.png',x,y,world,'alpha','A test unit.',owner)
