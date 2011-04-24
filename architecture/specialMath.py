from math import atan2
def distance(x1,x2):
    """
    Returns the square root of the sum of squares of two lists 
    of equal length.  It acts as an n-dimensional distance formula.
    """
    sqSum=0
    #print x1, x2
    for x,y in zip(x1,x2):
        sqSum+=(x-y)**2
    return sqSum**.5

def worldDist(x1, x2, worldSize):
    """finds shortest distance in wrapping world"""
    return distance(x1, findClosest(x1, x2, worldSize))

def findClosest(x1, x2, worldSize):
    """returns x2 closest to x1 in wrapping world"""
    minx, maxx= x1[0]-worldSize[0]/2.0, x1[0]+worldSize[0]/2.0
    miny, maxy= x1[1]-worldSize[1]/2.0, x1[1]+worldSize[1]/2.0
    for xShift in [0,-1,1]:
        for yShift in [0,-1,1]:
            test = [x2[0]+xShift*worldSize[0], \
                        x2[1]+yShift*worldSize[1]]
            if minx<=test[0] and test[0]<=maxx and \
                miny<=test[1] and test[1]<=maxy:
                    return test
    print 'Something has gone wrong!- specialMath.findClosest'
    return list[x2] #returns original point if optimal not found
                    
def cartToIso(coord):
    """
    Performs the cartesian-to-isometric linear transformation on a 
    coordinate (tuple of length two, representing an x,y coordinate).
    """
    return coord[0]+coord[1],-.5*coord[0]+.5*coord[1]
    
def isoToCart(coord):
    """
    Performs the isometric-to-cartesian linear transformation on a 
    coordinate (tuple of length two, representing an x,y coordinate).
    """
    return .5*coord[0]-coord[1],.5*coord[0]+coord[1]

def hypotenuse(x,y):
    """
    Calculates the length of the hypotenuse of two sides of a right 
    triangle with length x and y.
    """
    return pow(x**2+y**2,.5)

def centerOfEntityList(entities, worldSize):
    """
    Determines the average location of a list of entities.
    This is useful for moving groups without losing integrity.
    @param entities: List of entities
    """
    center = [0,0]
    i = 0
    first=-1
    for e in range(len(entities)):
        if entities[e].movable:
            if first<0:
                first=e
                c=entities[e].realCenter
            else:
                c = findClosest(entities[first].realCenter, entities[e].realCenter, worldSize)
            center[0] += c[0]
            center[1] += c[1]
            i+=1
    if i > 0:
        center[0] /= (i)
        center[1] /= (i)
    return tuple(center)



def closestEntity(entities,loc):
    """
    Returns the entity closest to an isometric coordinate (x,y tuple) on
    the display of the world (from the viewport).
    """
    #Note: using sort() seems like it would be really slow,
    #which is why I am using this technique.
    minDist = None
    closest = None
    for e in entities:
        drawRect = e.rect.move(e.drawOffset)
        drawRect.center = cartToIso(drawRect.center)
        
        selectRect = e.getSelectionRect(drawRect)
        
        dist = distance(selectRect.center,loc)
        if not minDist or dist < minDist:
            minDist = dist
            closest = e
    return closest

def imageNum(x,y,n):
    """returns image number for entity facing cartesian x,y direction"""
    isoVectX,isoVectY =cartToIso(x, y)
    isoTheta=atan2(isoVectY, isoVectX)
    isoTheta=-1*isoTheta/(2*3.14)%1

    return int(n*isoTheta)

if __name__ == "__main__":
    print isoToCart((-10,-10))
    print isoToCart((-10,10))
    print isoToCart((10,10))
    print isoToCart((1024,768))
    
