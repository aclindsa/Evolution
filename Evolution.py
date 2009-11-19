from Organism import Organism

"""Model evolutionary tactics in order to evolve a program that can solve a maze relatively efficiently"""

#Constants Section
#Organism-definition Constants
MEMORY_SIZE = 20
NUM_STATES = 20
NUM_VALUES = 2

def GOD():
    universe = Universe()
    universe.start()

class Universe:
    generation = 0
    def __init__(self):
        self.adam = Organism(NUM_STATES, MEMORY_SIZE, NUM_VALUES)
        self.eve = Organism(NUM_STATES, MEMORY_SIZE, NUM_VALUES)

    def start(self):
        print "Adam: \n"
        self.adam.displayStatesTable()
        print "\nmemory :"+str(self.adam.memory)+"\n\n"
        print "Eve: \n"
        self.eve.displayStatesTable()
        print "\nmemory :"+str(self.eve.memory)+"\n\n"

        #neworg = self.adam.meiosis(self.eve)
        neworgs = self.adam.reproduce(self.eve, 1, 10)
        neworg = neworgs[0]
        
        neworg.displayStatesTable()
        print "\nmemory :"+str(neworg.memory)+"\n\n"

#Function to start the whole process
if __name__ == "__main__":
    GOD()
