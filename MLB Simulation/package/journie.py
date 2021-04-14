from game import Game

class Journie:

    # Public Attributes
    games = []
    results = {}

    # Private Attributes
    # __games = []
    # __results = {}

    def __init__(self, data):
        for item in data:
            teamDataA = item[0]
            teamDataB = item[1]
            self.games.append(Game(teamDataA, teamDataB))
        
        for item in self.__games:
            if item.RunsA > item.RunsB:
                results.append(item.TeamA.Name, True)
                results.append(item.TeamB.Name, False)
            else:
                results.append(item.TeamA.Name, False)
                results.append(item.TeamB.Name, True)
