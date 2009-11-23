class Map:
    """Class to hold an implementation of a map for a maze
    The format of the map file will be as follows:
    The first line will contain 'M N' only, where M is the number
    of rows and N is the number of columns. The next M rows will
    contain M symbols, NOT separated by any spaces.
    These symbols may be 'S','F','.', or 'W' which represent
    The starting position, finished position, empty space, and walls
    respectively"""
    M = 10
    N = 10
    map = []
    shortestPath = []
    def __init__(self, mapFile=None):
        #if a mapfile was specified attempt to read from it
        if mapFile is not None:
            self.initFromFile(mapFile)
        else:
            self.map = [["." for j in range(self.N)] for i in range(self.M)]

        self.__findStartPoint()
        self.__findEndPoint()
        #initialize the shortestPath list
        self.shortestPath =  [[None for j in range(self.N)] for i in range(self.M)]
        self.shortestPath[self.end.i][self.end.j] = 0

    def initFromFile(self, mapFile):
        """Initialize this map from a map file"""
        try:
            file = open(mapFile, 'r')
            nm = file.readline().strip().split(" ")
            self.N,self.M = int(nm[0]),int(nm[1])
            for i in range(self.N):
                self.map.append([])
                row = file.readline().strip()
                for j in range(self.M):
                    if row[j] in "SF.W":
                        self.map[i].append(row[j])
                    else:
                        self.map[i].append(".")
            file.close()
        except Exception:
            print "Exception occurred in Map when attempting to import a map file\n"
            self.map = [["." for j in range(self.N)] for i in range(self.M)]

    def __findStartPoint(self):
        #now, find the starting and ending coordinates for the map
        for i in range(self.M):
            for j in range(self.N):
                if self.map[i][j] is "S":
                    self.start = Coordinate()
                    self.start.i = i
                    self.start.j = j
                    return
        #if we didn't find one, create one
        self.map[0][0] = "S"
        self.start = Coordinate()
        self.start.i = 0
        self.start.j = 0

    def __findEndPoint(self):
        """Find the end point and store it"""
        for i in range(self.M):
            for j in range(self.N):
                if self.map[i][j] is "F":
                    self.end = Coordinate()
                    self.end.i = i
                    self.end.j = j
                    return
        #if we didn't find one, create one
        self.map[self.M-1][self.N-1] = "F"
        self.end = Coordinate()
        self.end.i = self.M-1
        self.end.j = self.N-1

    def canMoveUp(self, coord):
        return coord.i > 0 and \
           self.map[coord.i-1][coord.j] is not "W"
    def canMoveDown(self, coord):
        return coord.i < self.M-1 and \
           self.map[coord.i+1][coord.j] is not "W"
    def canMoveLeft(self, coord):
        return coord.j > 0 and \
           self.map[coord.i][coord.j-1] is not "W"
    def canMoveRight(self, coord):
        return coord.j < self.N-1 and \
           self.map[coord.i][coord.j+1] is not "W"

    def findShortestPath(self, coord):
        if self.shortestPath[coord.i][coord.j] is not None:
            return self.shortestPath[coord.i][coord.j] 
        while self.shortestPath[coord.i][coord.j] is None:
            minimum = self.M*self.N + 1
            mincoord = Coordinate()
            for i in range(self.M):
                for j in range(self.N):
                    c = Coordinate(i,j)
                    if self.shortestPath[i][j] is not None:
                        nextmin = self.shortestPath[i][j] + 1
                        if nextmin < minimum:
                            if self.canMoveUp(c) and \
                                   self.shortestPath[i-1][j] is None:
                                minimum = nextmin
                                mincoord = c.up()
                            if self.canMoveDown(c) and \
                                   self.shortestPath[i+1][j] is None:
                                minimum = nextmin
                                mincoord = c.down()
                            if self.canMoveLeft(c) and \
                                   self.shortestPath[i][j-1] is None:
                                minimum = nextmin
                                mincoord = c.left()
                            if self.canMoveRight(c) and \
                                   self.shortestPath[i][j+1] is None:
                                minimum = nextmin
                                mincoord = c.right()
            #if we didn't find another possible path (aka minimum is still what
            #we set it to,from what we've already, we can't get there from here,
            #so quit trying already
            if minimum is self.M*self.N + 1:
                self.shortestPath[coord.i][coord.j] = -1
                return -1
            #but if we did find something, store it
            else:
                self.shortestPath[mincoord.i][mincoord.j] = minimum
        return self.shortestPath[coord.i][coord.j]

    def printShortestPaths(self):
        toReturn = ""
        for i in range(self.M):
            for j in range(self.N):
                sp = "       ."
                if self.shortestPath[i][j] is not None:
                    sp = str(self.shortestPath[i][j]) 
                    while len(sp) < 8:
                        sp = " "+sp
                toReturn += sp
            toReturn += "\n"
        return toReturn

    def toString(self, character=None, coord=None):
        toReturn = ""
        for i in range(self.M):
            for j in range(self.N):
                if coord is not None and coord.i is i and coord.j is j:
                    toReturn += character[0] + " "
                else:
                    toReturn += str(self.map[i][j]) + " "
            toReturn = toReturn[:-1] + "\n"
        return toReturn


    def __str__(self):
        return self.toString()
    def __unicode__(self):
        return self.toString()

class Coordinate:
    i = 0
    j = 0
    def __init__(self, i=0, j=0):
        self.i = i
        self.j = j
    def up(self):
        return Coordinate(self.i-1, self.j)
    def down(self):
        return Coordinate(self.i+1, self.j)
    def left(self):
        return Coordinate(self.i, self.j-1)
    def right(self):
        return Coordinate(self.i, self.j+1)
    def equals(self, other):
        return self.i is other.i and self.j is other.j
