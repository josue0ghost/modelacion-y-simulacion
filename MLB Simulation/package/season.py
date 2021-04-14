from journie import Journie
from batting import Batting

class Season:
    # Private attributes
    __results = {}
    __journies = []
    __summary = []

    @property
    def results(self):
        return self.__results
    
    @property
    def journies(self):
        return self.__journies
    
    @property
    def summary(self):
        return self.__summary


    def __init__(self, teams = []):

        __journies = []

        for i in range(0, 54):
            serie = self.combination(teams)
            
            for j in range(0, 3):
                journies.append(Journie(serie))

        __result = {}
        
        for item in teams:
            __result[item.Name] = [0,0]
        
        listJ = []
        for j in self.__journies:
            obj = type('', (object,), {'res':j.results})()
            listJ.append(obj)

        for dicc in listJ:
            for key,value in dicc.res.items():
                res = __result[key]
                if value:
                    __result[key][0] = res[0] + 1
                else:
                    _result[key][1] = res[1] + 1

        def first_or_default(summary = [], team="", scenario=""):
            for item in summary:
                if item.team == team and item.scenario == scenario:
                    return item
            return

        summary = []
        for journy in self.journies:
            for game in journy.games:
                for simulation in game.Simulations:
                    item = first_or_default(summary, simulation.team, simulation.scenario)
                    if item == None:
                        summary.append(Batting(simulation.scenario, simulation.team))
                    else:
                        item.count += 1
        #end

    def combination(self, teams=[]):
        import random
        import datetime
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


