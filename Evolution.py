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
ORIGINAL_POOL_SIZE = 10000 #size of the original random generation of organisms
GENERATION_SIZE = 50 #size of each generation thereafter
CARRY_OVER = 10  #number of top organisms to 'select' to procreate to make the
                 #next generation
LIFETIME = 100 #number of 'ticks' the organism has to prove itself
PERCENT_MUTATION = 20 #percent of mutation to apply to each reproduction
NUM_GENERATIONS = 10000 #number of generations

def GOD():
    universe = Universe()

class Universe:
    generation = 0
    totalScores = 0
    def __init__(self):
        #create the map that defines this Universe
        self.map = Map("simple.map")

        #generate first set of parents
        self.parents = [Organism(NUM_STATES, MEMORY_SIZE, NUM_VALUES) for i in range(ORIGINAL_POOL_SIZE)]

        #for each generation,
        for i in range(NUM_GENERATIONS):
            self.currentGeneration = i+1
            self.testParents()
            self.selectParents()
            self.nextGeneration()

    def testParents(self):
        #test all the parents and see how they perform
        self.scores = {}
        scoresList = []
        for organism in self.parents:
            score = self.testOrganism(organism)
            scoresList.append(score)
            if score in self.scores.keys():
                self.scores[score].append(organism)
            else:
                self.scores[score] = [organism]
        #print out the average score for this generation and overall
        avgscore = reduce(lambda x, y: x+y, scoresList)*1.0 / len(scoresList)
        self.totalScores = self.totalScores + avgscore
        print "generation",self.currentGeneration,":",avgscore," overall:",self.totalScores/self.currentGeneration

    def selectParents(self):
        #sort them by scores and assign the best to be the new parents
        keys = self.scores.keys()
        keys.sort()
        keys.reverse()
        parents = []
        currentScoreArray = 0
        scoreInArray = 0
        for i in range(CARRY_OVER):
            parents.append(self.scores[keys[currentScoreArray]][scoreInArray])
            scoreInArray = scoreInArray + 1
            if scoreInArray >= len(self.scores[keys[currentScoreArray]]):
                currentScoreArray = currentScoreArray + 1
                scoreInArray = 0

    def nextGeneration(self):
        self.reproduce()
        #now, assign these new children to be the parents of the next generation
        self.parents = self.children

    def reproduce(self):
        self.children = []
        while(True):
            for i in range(len(self.parents)):
                for j in range(i+1,len(self.parents)):
                    if len(self.children) < GENERATION_SIZE:
                        #Note: this makes the percent mutation go down as we get up in the generations
                        c = self.parents[i].reproduce(self.parents[j], 1, PERCENT_MUTATION * (NUM_GENERATIONS-self.generation) / NUM_GENERATIONS)
                        self.children.append(c[0])
                    else:
                        return

    def testOrganism(self, organism):
        """Function to test an organism and return a numeric value representing how
        it fared in attempting to solve the supplied maze"""
        #get the starting point for the map
        coord = copy(self.map.start)
        i = 0
        distanceSum = 0
        while i < LIFETIME:
            i = i + 1
            #figure out which ways the organism can move
            # and set those in the first four blocks of memory in the organism
            if self.map.canMoveUp(coord):
                organism.memory[0] = 1
            else:
                organism.memory[0] = 0
            if self.map.canMoveDown(coord):
                organism.memory[1] = 1
            else:
                organism.memory[1] = 0
            if self.map.canMoveLeft(coord):
                organism.memory[2] = 1
            else:
                organism.memory[2] = 0
            if self.map.canMoveRight(coord):
                organism.memory[3] = 1
            else:
                organism.memory[3] = 0
            #make the organism live for one 'tick'
#            print organism.memory
            organism.liveALittle()
#            print organism.memory
            #now, check the 'outputs' (the last 4 blocks in the organism's memory)
            upDown = organism.memory[MEMORY_SIZE-4] - organism.memory[MEMORY_SIZE-3]
            leftRight = organism.memory[MEMORY_SIZE-2] - organism.memory[MEMORY_SIZE-1]
#            print self.map.toString("O",coord)
            if upDown > 0 and self.map.canMoveUp(coord):
                coord = coord.up()
            elif upDown < 0 and self.map.canMoveDown(coord):
                coord = coord.down()
            if leftRight > 0 and self.map.canMoveLeft(coord):
                coord = coord.left()
            elif leftRight < 0 and self.map.canMoveRight(coord):
                coord = coord.right()
#            print self.map.toString("O",coord)
            #add the current distance from the end point to the current coordinate
            distanceSum = distanceSum + self.map.findShortestPath(coord)
            #if we found the end coordinate, break
            if coord.equals(self.map.end):
                break
        #calculate the 'score' of this organism
        #the score is the the number of "tick"s that it didn't have to use
        #out of the total alloted (LIFETIME) plus the average distance from the end
        #of the organism
        return LIFETIME - i + self.map.M * self.map.N - self.map.findShortestPath(coord)/2 - distanceSum / LIFETIME / 2


#Function to start the whole process
if __name__ == "__main__":
    GOD()
