from Organism import Organism
from Map import Map

"""Model evolutionary tactics in order to evolve a program that can solve a maze relatively efficiently"""

#Constants Section
#Organism-definition Constants
MEMORY_SIZE = 20
NUM_STATES = 20
NUM_VALUES = 2

#Evolutionary Constants
GENERATION_SIZE = 20
MAX_TEST_LENGTH = 500

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

        print str(m)
        print m.printShortestPaths()
        m.findShortestPath(m.start)
        print m.printShortestPaths()

def testOrganism(map, organism):
    """Function to test an organism and return a numeric value representing how
    it fared in attempting to solve the supplied maze"""
    pass

#Function to start the whole process
if __name__ == "__main__":
    GOD()
