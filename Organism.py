import random #used to generate randomness for mutations, etc.
from copy import deepcopy #deep copy support

from State import State

class Organism:
    state = 0 #the current state of the organism
    states = [] #the state table
    location = 0 #the current location in memory that we're dealing with
    memory = [] #the memory we're dealing with
    
    #all the sizes of things
    numStates = 0
    memorySize = 0
    numValues = 0

    def __init__(self, numStates, memorySize, numValues, initStates=None,
                 initMemory=None):
        """Initialize this Organism. If teh initStates or initMemory parameters
        are not provided, the states and/or memory will be generated randomly"""
        if initStates is not None:
            self.states = initStates
        else:
            self.states = [[State.getRandomState((0,numValues-1),
                                                 (0,numStates-1),
                                                 (0,memorySize-1)) for j in
                            range(numValues)] for i in range(numStates)]
            
        if initMemory is not None:
            self.memory = initMemory
        else:
            self.memory = [random.randint(0,numValues-1) for i in
                           range(0,memorySize)]
            
        self.numStates = numStates
        self.memorySize = memorySize
        self.numValues = numValues

    def reset(self):
        """reset the memory, state and location to all 0's"""
        memorySize = len(self.memory)
        self.memory = [0 for i in range(0,memorySize)]
        self.state = 0
        self.location = 0

    def liveALittle(self, numStates = 1):
        """Make the Organism cycle through a state (default), or a few"""
        if numStates < 1:
            return
        for i in range(numStates):
            #find the info about the next state, and execute it
            currentState = self.states[self.state][self.memory[self.location]]
            self.location = currentState.newLocation
            self.state = currentState.newState
            self.memory[self.location] = currentState.newValue

    def reproduce(self, other, numChildren=2, percentMutation=5):
        """return numChildren Organisms that are offspring of this organism, and the
        'other' organism"""
        children = []
        for i in range(numChildren):
            #do "DNA crossover"
            child = self.crossOver(other, percentMutation)
            #average values for memory between the two
            for j in range(child.memorySize):
                child.memory[j] = (self.memory[j] + other.memory[j]) / 2
                #do this to adjust for always rounding down
                if (self.memory[j] + other.memory[j]) % 2 is not 0 and random.randint(0,1) is 1: 
                    child.memory[j] = (child.memory[j] + 1) % child.numValues
            #and introduce some random mutation
            pMutation = random.randint(max(percentMutation/2,0),
                                       min(percentMutation*3/2,100))
            numMutations = (child.numStates*child.numValues +
                            child.memorySize)*pMutation/100
            for j in range(numMutations):
                mutationLocation = random.randint(0,child.numStates*child.numValues + child.memorySize - 1)
                if mutationLocation < child.numStates*child.numValues:
                    state = mutationLocation / child.numValues
                    value = mutationLocation % child.numValues
                    child.states[state][value] = \
                        State.getRandomState((0,child.numValues-1),
                                             (0,child.numStates-1),
                                             (0,child.memorySize-1))
                else:
                    mem = mutationLocation-child.numStates*child.numValues
                    child.memory[mem] = random.randint(0,child.numValues-1)
            children.append(child)
        return children


    def crossOver(self, other, percentMutation=5):
        """return an Organism that is a combination of the calling Organism and
        'other'"""
        #deep copy the Organisms 
        org1 = deepcopy(self);
        org2 = deepcopy(other);

        #get the number of crossover points (and make the actual percentage
        #wobble a little
        pMutation = random.randint(max(percentMutation/2,0),
                                   min(percentMutation*3/2,100))
        numCrossoverPoints = self.numStates*pMutation/100
        for i in range(numCrossoverPoints):
            crossoverState = random.randint(0,self.numStates - 1)
            crossoverValue = random.randint(0,self.numValues - 1)
            #if we're not crossing over the last state,
            #move the state lists over after the one we're switching
            if (crossoverState < org1.numStates - 1):
                tmp = org1.states[crossoverState + 1:]
                org1.states[crossoverState + 1:] = org2.states[crossoverState + 1:]
                org2.states[crossoverState + 1:] = tmp
            #now, cross over the values inside the pivotal crossoverState
            #at crossoverValue
            tmp = org1.states[crossoverState][crossoverValue:]
            org1.states[crossoverState][crossoverValue:] = \
                    org2.states[crossoverState][crossoverValue:]
            org2.states[crossoverState][crossoverValue:] = tmp

        #randomize which one gets returned
        if random.randint(0,1) is 1:
            return org1
        else:
            return org2

    def displayStatesTable(self):
        """display the states table for this Organism"""
        for i in range(len(self.states)):
            print "State "+str(i)+": \t\t",
            for j in range(len(self.states[i])):
                print str(self.states[i][j])+"\t\t",
            print
