def resourcesRequiredStr(buildCost,creationName):
    '''
    Returns a string of the form ''
    '''
    count = len(buildCost)
    if count == 0:
        return "Making a "+creationName+" is free!"
    buildStr = "You need "
    for i in xrange(count):
        resource = buildCost[i][0]
        cost = buildCost[i][1]
        if count == 1:
            buildStr += str(cost) + ' ' + resource.name+' to engineer a '+creationName+'.'
            return buildStr
        if i == count-1:
            buildStr += ' and '
        buildStr += str(cost) + ' ' + resource.name
        if i < count-1:
            buildStr += ', '
        else:
            buildStr += ' to create a '+creationName+'.'
    return buildStr
