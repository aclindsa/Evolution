from copy import copy #deep copy support

from Organism import Organism
from Map import Map

"""Model evolutionary tactics in order to evolve a program that can solve a maze relatively efficiently"""

#Constants Section
#Organism-definition Constants
MEMORY_SIZE = 8
NUM_STATES = 8
NUM_VALUES = 2

#Evolutionary Constants
GENERATION_SIZE = 20
LIFETIME = 500
PERCENT_MUTATION = 5
NUM_GENERATIONS = 1000

def GOD():
    universe = Universe()
    universe.start()

class Universe:
    generation = 0
    def __init__(self):
        self.adam = Organism(NUM_STATES, MEMORY_SIZE, NUM_VALUES)
        self.eve = Organism(NUM_STATES, MEMORY_SIZE, NUM_VALUES)

    def start(self):
        m = Map("simple.map")

        mom = copy(self.eve)
        dad = copy(self.adam)
        for i in range(NUM_GENERATIONS):
            children = mom.reproduce(dad, GENERATION_SIZE, PERCENT_MUTATION)
            scores = {}
            scoresList = []
            #test all the children and see how they do
            for child in children:
                score = testOrganism(m, child)
                scoresList.append(score)
                if score in scores.keys():
                    scores[score].append(child)
                else:
                    scores[score] = [child]
            #sort them by scores and assign the best to be the new mom and dad
            keys = scores.keys()
            keys.sort()
            keys.reverse()
            mom = scores[keys[0]][0]
            if len(scores[keys[0]]) > 1:
                dad = scores[keys[0]][1]
            else:
                dad = scores[keys[1]][0]
            #print out the average score
            scoresum = reduce(lambda x, y: x+y, scoresList)
            print scoresum*1.0/GENERATION_SIZE

def testOrganism(map, organism):
    """Function to test an organism and return a numeric value representing how
    it fared in attempting to solve the supplied maze"""
    #get the starting point for the map
    coord = copy(map.start)
    i = 0
    distanceSum = 0
    while i < LIFETIME:
        i = i + 1
        #figure out which ways the organism can move
        # and set those in the first four blocks of memory in the organism
        if map.canMoveUp(coord):
            organism.memory[0] = 1
        else:
            organism.memory[0] = 0
        if map.canMoveDown(coord):
            organism.memory[1] = 1
        else:
            organism.memory[1] = 0
        if map.canMoveLeft(coord):
            organism.memory[2] = 1
        else:
            organism.memory[2] = 0
        if map.canMoveRight(coord):
            organism.memory[3] = 1
        else:
            organism.memory[3] = 0
        #make the organism live for one 'tick'
        organism.liveALittle()
        #now, check the 'outputs' (the last 4 blocks in the organism's memory)
        upDown = organism.memory[MEMORY_SIZE-4] - organism.memory[MEMORY_SIZE-3]
        leftRight = organism.memory[MEMORY_SIZE-2] - organism.memory[MEMORY_SIZE-1]
        if upDown > 0 and map.canMoveUp(coord):
            coord = coord.up()
        elif upDown < 0 and map.canMoveDown(coord):
            coord = coord.down()
        if leftRight > 0 and map.canMoveLeft(coord):
            coord = coord.left()
        elif leftRight < 0 and map.canMoveRight(coord):
            coord = coord.right()
        #add the current distance from the end point to the current coordinate
        distanceSum = distanceSum + map.findShortestPath(coord)
        #if we found the end coordinate, break
        if coord.equals(map.end):
            break
    #calculate the 'score' of this organism
    #the score is the the number of "tick"s that it didn't have to use
    #out of the total alloted (LIFETIME) plus the average distance from the end
    #of the organism
    return LIFETIME - i + map.M * map.N - map.findShortestPath(coord)/2 - distanceSum / LIFETIME / 2


#Function to start the whole process
if __name__ == "__main__":
    GOD()
