active_groups = []

def getActiveGroups():
    active_groups.clear()
    filehandle = open('activeGroupsList.txt', 'r')
    for line in filehandle:
        currentId = line[:-1]
        active_groups.append(currentId)
    filehandle.close()

def addActiveGroup(idString):
    getActiveGroups()
    if idString not in active_groups:
        filehandle = open('activeGroupsList.txt', 'a+')
        filehandle.write('%s\n' % idString)
        filehandle.close()
        getActiveGroups()#refresh active group list

def removeActiveGroup(idString):
    getActiveGroups()
    filehandle = open('activeGroupsList.txt', 'w')
    for groupId in active_groups:
        if groupId != idString:
            filehandle.write("%s\n" % groupId)
    filehandle.close()
    getActiveGroups()

#def clearActiveGroups #empty the file?


