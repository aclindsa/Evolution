import random

def startEvolution():
    organism = Organism(20, 20, 2)
    
    displayStatesTable(organism.states)

    for i in range(100):
        print "state: "+str(organism.state)
        print "location: "+str(organism.location)
        print "memory :"+str(organism.memory)+"\n"

        organism.liveALittle()

class State:
    newValue = 0
    newState = 0
    newLocation = 0

    def __init__(self, nvalue=0, nstate=0, nlocation=0):
        self.newValue = nvalue
        self.newState = nstate
        self.newLocation = nlocation
    def __str__(self):
        return unicode(self)
    def __unicode__(self):
        return "v="+str(self.newValue)+",s="+str(self.newState)+",l="+str(self.newLocation)
        

def getRandomState(validValues=(0,100), validStates=(0,100), validLocations=(0,100)):
    """ Returns a random State object
    
        The validValues, validStates, and validLocations are all tuples of length 2 defining the minimum and maximum values 
    """
    return State(random.randint(validValues[0], validValues[1]), random.randint(validStates[0], validStates[1]), random.randint(validLocations[0], validLocations[1]))

def displayStatesTable(states):
    for i in range(len(states)):
        print "State "+str(i)+": \t\t",
        for j in range(len(states[i])):
            print states[i][j].__str__()+"\t\t",
        print

class Organism:
    state = 0 #the current state of the organism
    states = [] #the state table
    location = 0 #the current location in memory that we're dealing with
    memory = [] #the memory we're dealing with
    
    #all the sizes of things
    numStates = 0
    memorySize = 0
    numValues = 0

    #if the initStates or initMemory parameters are not provided, the states and/or memory will be generated randomly
    def __init__(self, numStates, memorySize, numValues, initStates=None, initMemory=None):
        if initStates is not None:
            self.states = initStates
        else:
            self.states = [[getRandomState((0,numValues-1), (0,numStates-1), (0,memorySize-1)) for j in range(numValues)] for i in range(numStates)]
            
        if initMemory is not None:
            self.memory = initMemory
        else:
            self.memory = [random.randint(0,numValues-1) for i in range(0,memorySize)]
            
        self.numStates = numStates
        self.memorySize = memorySize
        self.numValues = numValues

    #make the organism go through a state or a few
    def liveALittle(self, numStates = 1):
        if numStates < 1:
            return
        for i in range(numStates):
            #find the info about the next state, and execute it
            currentState = self.states[self.state][self.memory[self.location]]
            self.memory[self.location] = currentState.newValue
            self.location = currentState.newLocation
            self.state = currentState.newState


if __name__ == "__main__":
    startEvolution()