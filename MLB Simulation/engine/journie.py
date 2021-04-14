import game

class Journie:

    # Public Attributes
    games = []
    results = []

    # Private Attributes
    __games = []
    __results = []

    def __init__(self, data):
        for item in data:
            teamDataA = item[0]
            teamDataB = item[1]


            self.__games.append()