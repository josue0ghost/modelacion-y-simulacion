import batting
import random
import datetime

class Season:

    # Public Attributes
    results = {}
    journies = []
    summary = []

    # Private attributes
    __results = {}
    __journies = []
    __summary = []

    def __init__(self, teams):

        journies = []

        for i in range(0, 54):
            serie = self.combination(teams)
            
            for j in range(0, 3):
                journies.append() ##jornadas.Add(new Jornada(new List<TeamData[]>(serie)));


    def combination(self, teams=[]):
        combs = []
        copy = teams

        random.seed(datetime.datetime.fromtimestamp)
        rand = random.random()

        while len(copy) > 0:
            index1 = 0
            index2 = 0

            while index1 == index2:
                index1 = random.randint(0, len(copy))
                index2 = random.randint(0, len(copy))

            teamData = [
                copy[index1],
                copy[index2]
            ]
            combs.append(teamData)

            if index1 > index2:
                copy.pop(index1)
                copy.pop(index2)
            else:
                copy.pop(index2)
                copy.pop(index1)
        
        return combs


