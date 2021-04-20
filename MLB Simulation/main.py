import pandas as pd
import pyodbc
import random
import datetime
import copy as cpy

class Action:
    _key = ""
    count = 0
    valueA = 0
    valueB = 0

    def __init__(self, key, count):
        self._key = key
        self.count = count
    
    @property
    def key(self):
        return self._key
    @key.setter
    def key(self, value):
        self._key = value

class Range:

    # Public Attributes
    action = ""

    # Private Attributes
    __start = 0
    __close = 0

    def __init__(self, base, space, action):
        self.action = action
        self.__start = base
        self.__close = base + space
    
    def inRange(self, number):
        return (self.__start <= number) and (number < self.__close)

    def toString(self):
        return f"{self.action} | {self.__start} | {self.__close}"

class BatScenario:
    name = ""
    moves = 0
    outs = 0

    def __init__(self, name, moves, outs):
        self.name = name
        self.moves = moves
        self.outs = outs

class TeamStats:
    id = 0
    teamid = ""
    _singles = 0
    _doubles = 0
    _triples = 0
    _home_runs = 0
    _base_on_balls = 0
    _hit_by_pitch = 0
    _sacrifice = 0
    _double_played = 0
    _strike_out = 0
    _fg_out = 0
    _plates = 0
    _leagueID = ""
    _divID = ""
    name = ""

    def __init__(self, item):
        self.id = item[0]
        self.teamid = item[1]
        self._singles = item[2]
        self._doubles = item[3]
        self._triples = item[4]
        self._home_runs = item[5]
        self._base_on_balls = item[6]
        self._hit_by_pitch = item[7]
        self._sacrifice = item[8]
        self._double_played = item[9]
        self._strike_out = item[10]
        self._fg_out = item[11]
        self._plates = item[12]
        self._leagueID = item[13]
        self._divID = item[14]
        self.name = item[15]
    
    @property
    def leagueID(self):
        return self._leagueID
    
    @property
    def divID(self):
        return self._divID

    @property
    def base_on_balls(self):
        return self._base_on_balls
    @base_on_balls.setter
    def base_on_balls(self, value):
        self._base_on_balls = value
        
    @property
    def double_played(self):
        return self._double_played
    @double_played.setter
    def double_played(self, value):
        self._double_played = value

    @property
    def doubles(self):
        return self._doubles
    @doubles.setter
    def doubles(self, value):
        self._doubles = value
    
    @property
    def fg_outs(self):
        return self._fg_out
    @fg_outs.setter
    def fg_outs(self,value):
        self._fg_outs = value
    
    @property
    def hit_by_pitch(self):
        return self._hit_by_pitch
    @hit_by_pitch.setter
    def hit_by_pitch(self,value):
        self._hit_by_pitch = value

    @property
    def home_runs(self):
        return self._home_runs
    @home_runs.setter
    def home_runs(self,value):
        self._home_runs = value

    @property
    def sacrifice(self):
        return self._sacrifice
    @sacrifice.setter
    def sacrifice(self, value):
        self._sacrifice = value
    
    @property
    def singles(self):
        return self._singles
    @singles.setter
    def singles(self,value):
        self._singles = value
    
    @property
    def strike_out(self):
        return self._strike_out
    @strike_out.setter
    def strike_out(self,value):
        self._strike_out = value

    @property
    def triple(self):
        return self._triples
    @triple.setter
    def triple(self,value):
        self._triple = value

class Inning:
    
    # Private Attributes
    __bases = []

    # Public Attributes
    runs = 0
    outs = 0

    def __init__(self):
        self.__bases = [False, False, False, False, False]
        self.runs = 0
        self.outs = 0

    @property
    def is_active(self):
        return self.outs < 3
    
    @property
    def have_runners(self):
        return self.__bases.count(True) > 0

    def copy(self):
        copy = Inning()
        copy.runs = self.runs
        copy.outs = self.outs
        copy.__bases = cpy.deepcopy(self.__bases)
        return copy

    def move(self, number=""):
        if number == "":
            copy = self.copy()
            for i in range(4, 0, -1):
                copy.__bases[i] = copy.__bases[i - 1]
            copy.__bases[0] = False

            if copy.__bases[4]:
                copy.runs += 1
                copy.__bases[4] = False
            return copy
        else:
            v_copy = self.copy()
            while number > 0:
                v_copy = v_copy.move()
                number += -1
            return v_copy

    def out(self, number=""):
        if number == "":
            copy = self.copy()
            copy.__bases[0] = False
            copy.outs += 1
            return copy
        elif number == 1:
            return self.out()
        elif number == 2:
            return self.double_play()
        else:
            return self.copy()

    def one_run(self, is_winner=True):
        ini = Inning()
        if is_winner:
            ini = ini.add_plate()
            ini = ini.move(4)

        #for i in range(3):
        ini = ini.out()
        ini = ini.out()
        ini = ini.out()
        
        return ini

    def double_play(self):
        copy = self.out()
        if copy.__bases[3] == True:
            copy.__bases[3] = False
        elif copy.__bases[2] == True:
            copy.__bases[2] = False
        else:
            copy.__bases[1] = False
        
        return copy

    def add_plate(self):
        copy = self.copy()
        copy.__bases[0] = True
        return copy

class TeamData:
    _Name = ""
    _Counters = []
    _rangeA = []
    _rangeB = []

    
    @property
    def counters(self):
        return {counter.name : counter for counter in self._Counters}
    
    @counters.setter
    def counters(self, value):
        self._Counters = value
    
    @property
    def rangeA(self):
        return list(self._rangeA)
    @rangeA.setter
    def rangeA(self, value):
        self._rangeA = value

    @property
    def rangeB(self):
        return list(self._rangeB)
    
    @rangeB.setter
    def rangeB(self, value):
        self._rangeB = value

    def to_dict(self):
        return {
            'Name': self.Name,
            'rangeA': [ra.toString() for ra in self._rangeA],
            'rangeB': [rb.toString() for rb in self._rangeB]
        }

    def __init__(self, teamStats = TeamStats):
        self.Name = teamStats.teamid
        self.Counters = [
            Action("base_on_balls", teamStats.base_on_balls),
            Action("double_played",teamStats.double_played),
            Action("doubles",teamStats.doubles),
            Action("fg_outs",teamStats.fg_outs),
            Action("hit_by_pitch",teamStats.hit_by_pitch),
            Action("home_runs",teamStats.home_runs),
            Action("sacrifice",teamStats.sacrifice),
            Action("singles",teamStats.singles),
            Action("strike_out",teamStats.strike_out),
            Action("triple",teamStats.triple)
            ]
    
        fulldiv = lambda num,dem: float(num)/float(dem)

        ts_plates = teamStats._plates
        res = teamStats._plates - teamStats._sacrifice - teamStats._double_played
        for item in self.Counters:
            item.valueA = fulldiv(item.count, ts_plates)
            if item.key == "sacrifice" or item.key == "double_played":
                item.valueB = 0
            else:
                item.valueB = fulldiv(item.count, res)
        

        listA = [x for x in self.Counters]    
        listA.sort(key=lambda x: x.valueA, reverse=True)

        self._rangeA = []
        counter = 0
        for item in listA:
            Range_ = Range(counter, item.valueA, item.key)
            self._rangeA.append(Range_)
            counter+=item.valueA
        
        listB = [i for i in self.Counters if i.key != "sacrifice" and i.key != "double_played"]
        listB.sort(key=lambda x: x.valueB, reverse=True)

        counter = 0
        self._rangeB = []
        for item in listB:
            Range_ = Range(counter, item.valueB, item.key)
            self._rangeB.append(Range_)
            counter+=item.valueB

class Game:
    _TeamA = TeamData
    _TeamB = TeamData
    _ResultA = []
    _ResultB = []
    _simulations = []
    _RunsA = 0
    _RunsB = 0

    def get_bat_scenarios(self):
        item = [0,"",0,0,0,0,0,0,0,0,0,0,0,"","",""]
        v_team_stats = TeamStats(item)

        l_scenarios = [
            BatScenario("singles", 1, 0),
            BatScenario("doubles", 2, 0),
            BatScenario("triple", 3, 0),
            BatScenario("home_runs", 4, 0),
            BatScenario("base_on_balls", 1, 0),
            BatScenario("hit_by_pitch", 1, 0),
            BatScenario("sacrifice", 1, 1),
            BatScenario("strike_out", 0, 1),
            BatScenario("double_played", 0, 2),
            BatScenario("fg_outs", 0, 1),
        ]
        return {scenarios.name : scenarios for scenarios in l_scenarios}

    @property
    def TeamA(self):
        return self._TeamA

    @TeamA.setter
    def TeamA(self, teamA):
        self._TeamA = teamA

    @property
    def TeamB(self):
        return self._TeamB
    
    @TeamB.setter
    def TeamB(self, teamB):
        self._TeamB = teamB
    
    @property
    def ResultA(self):
        return self._ResultA
    @ResultA.setter
    def ResultA(self, value):
        self._ResultA = value
    
    @property
    def ResultB(self):
        return self._ResultB
    @ResultB.setter
    def ResultB(self, value):
        self._ResultB = value
    
    @property
    def Simulations(self):
        return list(self._simulations)
    @Simulations.setter
    def Simulations(self, value):
        self._simulations = value
    
    @property
    def RunsA(self):
        ra_list = [i.runs for i in self._ResultA]
        return sum(ra_list)
        
    @property
    def RunsB(self):
        rb_list = [i.runs for i in self._ResultB]
        return sum(rb_list)

    def playInning(self, data = TeamData):
        d_rangeA = data.rangeA
        d_rangeB = data.rangeB

        scenarios = self.get_bat_scenarios()
        random.seed(datetime.datetime.now().microsecond)
        v_inning = Inning()
        while v_inning.is_active: # and v_inning.runs < 9 :
            rand = random.random()
            action = ""
            if v_inning.have_runners:  
                element = next(x for x in d_rangeA if x.inRange(rand))
                action = element.action
            else:   
                element = next(x for x in d_rangeB if x.inRange(rand))            
                action = element.action
            
            scenario = scenarios[action]
            v_inning = v_inning.add_plate()
            v_inning = v_inning.out(scenario.outs)
            if(v_inning.is_active):
                v_inning = v_inning.move(scenario.moves)

        while v_inning.is_active:
            v_inning = v_inning.out(1)

        return v_inning
    
    def __init__(self, a = TeamData, b = TeamData):

        self.TeamA = a
        self.TeamB = b
        self.ResultA = []
        self.ResultB = []

        while len(self.ResultA) < 9: # and len(self.ResultB) < 9: (len(self.ResultB) will always be the same as A's)
            self.ResultA.append(self.playInning(self.TeamA))
            self.ResultB.append(self.playInning(self.TeamB))

        extraInning = 11
        while self.RunsA == self.RunsB and extraInning > 0:
            self.ResultA.append(self.playInning(self.TeamA))
            self.ResultB.append(self.playInning(self.TeamB))
            extraInning += -1

        if self.RunsA == self.RunsB:
            random.seed(datetime.datetime.now().microsecond)
            rand = random.random()
            if rand < 0.5:
                self.ResultA.append(Inning.one_run(True))
                self.ResultB.append(Inning.one_run(False))
            else:
                self.ResultA.append(Inning.one_run(False))
                self.ResultB.append(Inning.one_run(True))

class Journie:
    games = []
    results = {}

    def to_dict(self):
        return {
            'results': self.results
        }

    def __init__(self, data):
        
        self.games = []
        self.results = {}
        
        self.games = [Game(item[0], item[1]) for item in data]
        
        for item in self.games:
            if item.RunsA > item.RunsB:
                self.results[item.TeamA.Name] = True
                self.results[item.TeamB.Name] = False
            else:
                self.results[item.TeamA.Name] = False
                self.results[item.TeamB.Name] = True

class Season:
    # Private attributes
    __results = {}
    __journies = []

    @property
    def results(self):
        return self.__results
    
    @property
    def journies(self):
        return self.__journies


    def __init__(self, teams = []):
        for i in  range(54):
            serie = self.combination(teams)
            self.__journies += [Journie(serie) for j in range(3)]
        
        self.__results = {item.Name:[0,0] for item in teams}
                
        listJ = [type('', (object,), {'res':j.results})() for j in self.journies]

        for dicc in listJ:
            dic = dicc.res.items()
            for key,value in dic:
                res = self.__results[key]
                if value:
                    self.__results[key][0] = res[0] + 1
                else:
                    self.__results[key][1] = res[1] + 1
        #end

    def combination(self, teams=[]):
        combs = []
        copy = cpy.deepcopy(teams)

        random.seed(datetime.datetime.now().microsecond)

        while len(copy) > 0:
            index1 = 0
            index2 = 0

            while index1 == index2:
                index1 = random.randint(0, len(copy)-1)
                index2 = random.randint(0, len(copy)-1)

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

class Engine:
    # Private attributes
    __seasons = []

    # Public attributes
    seasons = []
    teams = {}

    def __init__(self, simulations):
        conn = pyodbc.connect(
            'Driver={SQL Server};'
            'Server=url-2021.database.windows.net;'
            'Database=mys_url;'
            'UID=url_2021;'
            'PWD=L0g!n_landivar2o21;'
        )

        SQL = "SELECT * FROM teamStats"
        df = pd.read_sql_query(SQL, conn)

        stats = df.values.tolist()
        data = []
        _stats = []
        
        index = 0
        for item in stats:
            st = TeamStats(item)
            data.append(TeamData(st))
            _stats.append(st)
            index += 1
        
        self.teams = {x.teamid: x for x in _stats}
        
        for index in range(simulations):
            print(f"Simulating season #{index+1}... please, wait")
            self.__seasons.append(Season(data))
        
        self.seasons = cpy.deepcopy(self.__seasons)
        
# Post Season Tagging

class SimulationsTeamResults:
    _strID = 0
    _iteracion = 0
    _teamID = ""
    _teamName = ""
    _league = ""
    _division = ""
    _wins = 0
    _losses = 0

    leagueRank = 0
    divRank = 0
    isInPS = ""

    def toRow(self):
        row = []
        row.append(self._strID)
        row.append(self._iteracion)
        row.append(self._teamID)
        row.append(self._teamName)
        row.append(self._league)
        row.append(self._division)
        row.append(self._wins)
        row.append(self._losses)
        row.append(self.leagueRank)
        row.append(self.divRank)
        row.append(self.isInPS)
        return row

    def __init__(self, item):
        self._strID = item[0]
        self._iteracion = item[1]
        self._teamID = item[2]
        self._teamName = item[3]
        self._league = item[4]
        self._division = item[5]
        self._wins = item[6]
        self._losses = item[7]
        self.isInPS = False
    
    @property
    def strID(self):
        return self._strID
    @property
    def iteration(self):
        return self._iteracion
    @property
    def teamID(self):
        return self._teamID
    @property
    def teamName(self):
        return self._teamName
    @property
    def league(self):
        return self._league
    @property
    def division(self):
        return self._division
    @property
    def wins(self):
        return self._wins
    @property
    def losses(self):
        return self._losses

eng = Engine(10)
season = 1
rowNum = 0
results = []
for item in eng.seasons:
    res = item.results.items()
    for key,value in res:
        t = eng.teams[key]
        results.append([rowNum, season, key, t.name, t.leagueID, t.divID, value[0], value[1]])
        rowNum += 1
    season += 1
print("======================================================")
dfr = pd.DataFrame(results, columns=['RowNum', 'Season', 'TEAM_ID', 'TEAM_NAME', 'LEAGUE', 'DIVISION', 'WINS', 'LOSSES'])
print(dfr)
print("======================================================")
print("Simulation finished")

STRlist = []
dfr.sort_values(by='RowNum', ascending=True, inplace=True)
for line in dfr.values.tolist():
    STRlist.append(SimulationsTeamResults(line))

# functions to assign positions
def leaguePosition(sortedDF):
    lpos = 1
    lis = sortedDF.values.tolist()
    for row in lis:
        rowNum = row[0]
        STRlist[rowNum].leagueRank = lpos
        lpos += 1
def divisionPosition(sortedDF):
    dpos = 1
    lis = sortedDF.values.tolist()
    for row in lis:
        rowNum = row[0]
        STRlist[rowNum].divRank = dpos
        dpos += 1

# assign positons
iterationsCount = int(len(STRlist) / 30)
for i in range(iterationsCount):
    seasonNum = i + 1
    nlTable = dfr.query('Season == ' + str(seasonNum) + ' and LEAGUE == "NL"', inplace = False)
    alTable = dfr.query('Season == ' + str(seasonNum) + ' and LEAGUE == "AL"', inplace = False)
    # sort for position in league
    nlTable.sort_values(by=['WINS'], ascending=False, inplace=True)
    leaguePosition(nlTable)
    alTable.sort_values(by=['WINS'], ascending=False, inplace=True)
    leaguePosition(alTable)
    # sort for positions in Division
    for div in ["W","C","E"]:
        # NL
        qd = 'DIVISION == "' + div + '"'
        nldTable = nlTable.query(qd, inplace=False)
        nldTable.sort_values(by=['WINS'], ascending=False, inplace=True)
        divisionPosition(nldTable)
        # AL
        aldTable = alTable.query(qd, inplace=False)
        aldTable.sort_values(by=['WINS'], ascending=False, inplace=True)
        divisionPosition(aldTable)
# rules for Post Season
for item in STRlist:
    if(item.divRank == 1):
        item.isInPS = True

for i in range(iterationsCount):
    seasonNum = i + 1
    def extraInLeague(l):
        def candFilter(strObj):
            val = True
            val = val & (strObj.iteration == seasonNum)
            val = val & (strObj.divRank != 1)
            val = val & (strObj.league == l)
            return val
        candidateList = list(filter(candFilter, STRlist))
        candidateList.sort(key=lambda x: x.leagueRank)

        teamid_A = candidateList[0].strID
        teamid_B = candidateList[1].strID

        STRlist[teamid_A].isInPS = True
        STRlist[teamid_B].isInPS = True

    extraInLeague("NL")
    extraInLeague("AL")

positonsResults = []
for item in STRlist:
    positonsResults.append(item.toRow())
print("======================================================")
cols=['RowNum', 'Season', 'TEAM_ID', 'TEAM_NAME', 'LEAGUE', 'DIVISION', 'WINS', 'LOSSES','LEAGUE_RANK','DIV_RANK','POSTSEASON']
finalDFR = pd.DataFrame(positonsResults, columns=cols)
print(finalDFR)
print("======================================================")
print("Post Season Tagging Finished")


