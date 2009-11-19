import random #random number generation

class State:
    newValue = 0
    newState = 0
    newLocation = 0

    def __init__(self, nvalue=0, nstate=0, nlocation=0):
        self.newValue = nvalue
        self.newState = nstate
        self.newLocation = nlocation
    @staticmethod
    def getRandomState(validValues=(0,100), validStates=(0,100),
                       validLocations=(0,100)):
        """randomize this state according to the valid states passed in
        
        The validValues, validStates, and validLocations are all tuples of
        length 2 defining the minimum and maximum values"""
        return State(random.randint(validValues[0], validValues[1]),
                     random.randint(validStates[0], validStates[1]),
                     random.randint(validLocations[0], validLocations[1]))
        """randomize this state according to the valid states passed in"""
    def __str__(self):
        return unicode(self)
    def __unicode__(self):
        return "v="+str(self.newValue)+",s="+str(self.newState)+",l="+str(self.newLocation)
