def distance(x1,x2):
    sqSum=0
    print x1, x2
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
            test = (x2[0]+xShift*worldSize[0], \
                        x2[1]+yShift*worldSize[1])
            if minx<=test[0] and test[0]>=maxx and \
                miny<=test[1] and test[1]>=maxy:
                    print worldSize
                    print test
                    return test
    return None
                    
    
def cartToIso(coord):
    return coord[0]+coord[1],-.5*coord[0]+.5*coord[1]
    
def isoToCart(coord):
    return .5*coord[0]-coord[1],.5*coord[0]+coord[1]

def hypotenuse(x,y):
    return pow(x**2+y**2,.5)

def centerOfEntityList(entities):
    """
    Determines the average location of a list of entities.
    This is useful for moving groups without losing integrity.
    @param entities: List of entities
    """
    center = [0,0]
    e = 0
    for e in xrange(1,len(entities)+1):
        c = entities[e-1].rect.center
        center[0] += c[0]
        center[1] += c[1]
    if e > 0:
        center[0] /= (e)
        center[1] /= (e)
    return tuple(center)

if __name__ == "__main__":
    print isoToCart((-10,-10))
    print isoToCart((-10,10))
    print isoToCart((10,10))
    print isoToCart((1024,768))
