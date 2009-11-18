import random #used to generate randomness for mutations, etc.
import copy #deep copy support

"""Model evolutionary tactics in order to evolve a program that can solve a maze relatively efficiently"""

#Constants Section
#Organism-definition Constants
MEMORY_SIZE = 20
NUM_STATES = 20
NUM_VALUES = 2

#Reproduction Constants
MIN_CROSSOVER_POINTS = 2
MAX_CROSSOVER_POINTS = 10

def GOD():
    universe = Universe()
    universe.start()
    
    organism = Organism(20, 20, 2)
    
    displayStatesTable(organism.states)

    for i in range(100):
        print "state: "+str(organism.state)
        print "location: "+str(organism.location)
        print "memory :"+str(organism.memory)+"\n"

        organism.liveALittle()

class Universe:
    generation = 0
    def __init__(self):
        self.adam = Organism(NUM_STATES, MEMORY_SIZE, NUM_VALUES)
        self.eve = Organism(NUM_STATES, MEMORY_SIZE, NUM_VALUES)

        self.adam.reproduce(self.eve)

    def start(self):
        pass

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

    #return numChildren Organisms that are offspring of this organism, and the 'other' organism
    def reproduce(self, other, numChildren=2, percentMutation=5):
        children = []
        for i in range(numChildren):
            #do "DNA crossover"
            child = self.meiosis(other)
            #average values for memory between the two
            for j in range(child.memorySize):
                child.memory[j] = (self.memory[j] + other.memory[j]) / 2
                if random.randint(0,1) is 1: #do this to adjust for always rounding down
                    child.memory[j] = (child.memory[j] + 1) % child.memorySize
            #and introduce some random mutation
            numMutations = random.randint(max(percentMutation-percentMutation/2,0), min(percentMutation+percentMutation/2,100))*(child.numStates*child.numValues + child.memorySize)
            for j in range(numMutations):
                mutationLocation = random.randint(0,child.numStates*child.numValues + child.memorySize - 1)
                if mutationLocation < child.numStates*child.numValues:
                    child.states[mutationLocation/child.numValues][mutationLocation%child.numValues] = getRandomState((0,child.numValues-1), (0,child.numStates-1), (0,child.memorySize-1))
                else:
                    child.memory[mutationLocation-child.numStates*child.numValues] = random.randint(0,child.numValues)
            children.append(child)
        return children


    #return an Organism that is a combination of this Organism and 'other'
    def meiosis(self, other):
        #deep copy the Organisms 
        org1 = copy.copy(self);
        org2 = copy.copy(other);
        #randomize which one gets returned, and which gets to be the "base" for crossing over
        if random.randint(0,1) is 1:
            tmp = org1
            org2 = org1
            org1 = tmp

        #get the number of crossover points
        numCrossoverPoints = random.randint(MIN_CROSSOVER_POINTS, MAX_CROSSOVER_POINTS)
        for i in range(numCrossoverPoints):
            crossoverState = random.randint(0,self.numStates - 1)
            crossoverValue = random.randint(0,self.numValues - 1)
            #if we're not crossing over the last state, move the state lists over after the one we're switching
            if (crossoverState < org1.numStates - 1):
                org1.states[crossoverState + 1:] = org2.states[crossoverState + 1:]
            #now, cross over the values inside the pivotal crossoverState at crossoverValue
            print crossoverState
            print crossoverValue
            org1.states[crossoverState][crossoverValue:] = org2.states[crossoverState][crossoverValue:]
        return org1


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


#Function to start the whole process
if __name__ == "__main__":
    GOD()
