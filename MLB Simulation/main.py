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
    
    def in_range(self, number):
        return (self.__start <= number) and (number < self.__close)

    def to_string(self):
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

    '''
        Copy an inning
    '''
    def copy(self):
        copy = Inning()
        copy.runs = self.runs
        copy.outs = self.outs
        copy.__bases = cpy.deepcopy(self.__bases)
        return copy

    '''
        Moves n given bases in a inning

        Parámeters:
        number -- times bases are moving

        Exceptions:
        if number < 0
    '''
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

    '''
        Makes n given outs in a inning

        Parameters:
        number -- amount of outs
    '''
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

    '''
        Makes a run in a inning

        If the team is winner, does add_plate() and move(4)
        Then does out() 3 times

        Parameters:
        is_winner -- Boolean
    '''
    def one_run(self, is_winner=True):
        ini = Inning()
        if is_winner:
            ini = ini.add_plate()
            ini = ini.move(4)

        # 3 outs
        ini = ini.out()
        ini = ini.out()
        ini = ini.out()
        
        return ini

    '''
        Simulates an out of the batting player
        and a runner
    '''
    def double_play(self):
        copy = self.out()

        if copy.__bases[3] == True:
            copy.__bases[3] = False
        elif copy.__bases[2] == True:
            copy.__bases[2] = False
        else:
            copy.__bases[1] = False
        
        return copy

    '''
        Simulates adding a player to home
    '''
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

    '''
        Collect the probability data of the two teams
        participating in a match

        Parameters:
        teamStats -- statistics of a team
    '''
    def __init__(self, teamStats = TeamStats):
        self.Name = teamStats.teamid
        self.Counters = [
            Action("base_on_balls", teamStats.base_on_balls),
            Action("double_played", teamStats.double_played),
            Action("doubles", teamStats.doubles),
            Action("fg_outs", teamStats.fg_outs),
            Action("hit_by_pitch", teamStats.hit_by_pitch),
            Action("home_runs", teamStats.home_runs),
            Action("sacrifice", teamStats.sacrifice),
            Action("singles", teamStats.singles),
            Action("strike_out", teamStats.strike_out),
            Action("triple", teamStats.triple)
            ]
    
        full_div = lambda num,dem: float(num)/float(dem)

        ts_plates = teamStats._plates
        res = teamStats._plates - teamStats._sacrifice - teamStats._double_played

        for item in self.Counters:
            item.valueA = full_div(item.count, ts_plates)
            if item.key == "sacrifice" or item.key == "double_played":
                item.valueB = 0
            else:
                item.valueB = full_div(item.count, res)
        
        list_team_a = [x for x in self.Counters]    
        list_team_a.sort(key=lambda x: x.valueA, reverse=True)

        self._rangeA = []
        counter = 0
        for item in list_team_a:
            Range_ = Range(counter, item.valueA, item.key)
            self._rangeA.append(Range_)
            counter+=item.valueA
        
        list_team_b = [i for i in self.Counters if i.key != "sacrifice" and i.key != "double_played"]
        list_team_b.sort(key=lambda x: x.valueB, reverse=True)

        counter = 0
        self._rangeB = []
        for item in list_team_b:
            Range_ = Range(counter, item.valueB, item.key)
            self._rangeB.append(Range_)
            counter+=item.valueB

class Game:
    _team_a = TeamData
    _team_b = TeamData
    _result_a = []
    _result_b = []
    _simulations = []

    '''
        Collect the possible outcomes when a batter
        goes to a plate
    '''
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
        return self._team_a

    @TeamA.setter
    def TeamA(self, teamA):
        self._team_a = teamA

    @property
    def TeamB(self):
        return self._team_b
    
    @TeamB.setter
    def TeamB(self, teamB):
        self._team_b = teamB
    
    @property
    def ResultA(self):
        return self._result_a
    @ResultA.setter
    def ResultA(self, value):
        self._result_a = value
    
    @property
    def ResultB(self):
        return self._result_b
    @ResultB.setter
    def ResultB(self, value):
        self._result_b = value
    
    @property
    def Simulations(self):
        return list(self._simulations)
    @Simulations.setter
    def Simulations(self, value):
        self._simulations = value
    
    @property
    def RunsA(self):
        ra_list = [i.runs for i in self._result_a]
        return sum(ra_list)
        
    @property
    def RunsB(self):
        rb_list = [i.runs for i in self._result_b]
        return sum(rb_list)

    '''
        Simulates an inning of a team

        Parameterse:
        data -- Probabilities of a team -- type: TeamData 
    '''
    def playInning(self, data = TeamData):
        data_range_a = data.rangeA
        data_range_b = data.rangeB

        scenarios = self.get_bat_scenarios()
        random.seed(datetime.datetime.now().microsecond)
        inning_ = Inning()

        while inning_.is_active:
            rnd = random.random()
            action = ""
            if inning_.have_runners:  
                element = next(x for x in data_range_a if x.in_range(rnd))
                action = element.action
            else:   
                element = next(x for x in data_range_b if x.in_range(rnd))            
                action = element.action
            
            scenario = scenarios[action]
            inning_ = inning_.add_plate()
            inning_ = inning_.out(scenario.outs)

            if(inning_.is_active):
                inning_ = inning_.move(scenario.moves)

        while inning_.is_active:
            inning_ = inning_.out(1)

        return inning_
    

    '''
        Simulates a game between two teams

        Parameters:
        team_a_data -- Probabilities of team A -- type: TeamData
        team_b_data -- Probabilities of team B -- type: TeamData
    '''
    def __init__(self, team_a_data = TeamData, team_b_data = TeamData):

        self.team_a = team_a_data
        self.team_b = team_b_data
        self.ResultA = []
        self.ResultB = []

        while len(self.ResultA) < 9: # and len(self.ResultB) < 9: (len(self.ResultB) will always be the same as A's)
            self.ResultA.append(self.playInning(self.team_a))
            self.ResultB.append(self.playInning(self.team_b))

        extraInning = 11
        while self.RunsA == self.RunsB and extraInning > 0:
            self.ResultA.append(self.playInning(self.team_a))
            self.ResultB.append(self.playInning(self.team_b))
            extraInning += -1

        if self.RunsA == self.RunsB:
            random.seed(datetime.datetime.now().microsecond)
            rnd = random.random()
            if rnd < 0.5:
                self.ResultA.append(Inning.one_run(True))
                self.ResultB.append(Inning.one_run(False))
            else:
                self.ResultA.append(Inning.one_run(False))
                self.ResultB.append(Inning.one_run(True))

class Journie:
    games = []
    results = {}

    '''
        Simulates a Journie collecting the results

        Parameters:
        data -- list of teams combinations for matches
    '''
    def __init__(self, data):
        
        self.games = []
        self.results = {}
        
        self.games = [Game(item[0], item[1]) for item in data]
        
        for item in self.games:
            if item.RunsA > item.RunsB:
                self.results[item.team_a.Name] = True
                self.results[item.team_b.Name] = False
            else:
                self.results[item.team_a.Name] = False
                self.results[item.team_b.Name] = True

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

    '''
        Simulates a Season
        consisting in 162 games (3 journies * 54)

        Parameters:
        teams -- list of TeamData of all the teams
    '''
    def __init__(self, teams = []):

        for i in  range(54):
            serie = self.combination(teams)
            self.__journies += [Journie(serie) for j in range(3)]
        
        self.__results = {item.Name:[0,0] for item in teams}
                
        journies_list = [type('', (object,), {'res':j.results})() for j in self.journies]

        for dicc in journies_list:
            results = dicc.res.items()
            for key,value in results:
                res = self.__results[key]
                if value:
                    self.__results[key][0] = res[0] + 1
                else:
                    self.__results[key][1] = res[1] + 1
        

    '''
        Returns posible combinations of teams for matches

        Parameters:
        teams -- list of TeamData of all the teams
    '''
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

            team_data = [
                copy[index1],
                copy[index2]
            ]
            combs.append(team_data)

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

    '''
        Runs n given Season simulations

        Parameters:
        simulations -- number of Season to simulate
    '''
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
        
        for item in stats:
            st = TeamStats(item)
            data.append(TeamData(st))
            _stats.append(st)

        
        self.teams = {x.teamid: x for x in _stats}
        
        for index in range(simulations):
            print(f"Simulating season #{index+1}... please, wait")
            self.__seasons.append(Season(data))
        
        self.seasons = cpy.deepcopy(self.__seasons)
        
# Post Season Tagging

class SimulationsTeamResults:
    _sims_team_res_id = 0
    _iteracion = 0
    _team_id = ""
    _team_name = ""
    _league = ""
    _division = ""
    _wins = 0
    _losses = 0

    league_rank = 0
    division_rank = 0
    is_in_post_season = False

    def to_row(self):
        row = []
        row.append(self._sims_team_res_id)
        row.append(self._iteracion)
        row.append(self._team_id)
        row.append(self._team_name)
        row.append(self._league)
        row.append(self._division)
        row.append(self._wins)
        row.append(self._losses)
        row.append(self.league_rank)
        row.append(self.division_rank)
        row.append(self.is_in_post_season)
        return row

    def __init__(self, item):
        self._sims_team_res_id = item[0]
        self._iteracion = item[1]
        self._team_id = item[2]
        self._team_name = item[3]
        self._league = item[4]
        self._division = item[5]
        self._wins = item[6]
        self._losses = item[7]
        self.is_in_post_season = False
    
    @property
    def strID(self):
        return self._sims_team_res_id
    @property
    def iteration(self):
        return self._iteracion
    @property
    def teamID(self):
        return self._team_id
    @property
    def teamName(self):
        return self._team_name
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

# MAIN EXCECUTION

eng = Engine(10)
season = 1
row = 0
results = []
for item in eng.seasons:
    res = item.results.items()
    for key,value in res:
        t = eng.teams[key]
        results.append([row, season, key, t.name, t.leagueID, t.divID, value[0], value[1]])
        row += 1
    season += 1

print("======================================================")
dfr = pd.DataFrame(results, columns=['Row', 'Season', 'TEAM_ID', 'TEAM_NAME', 'LEAGUE', 'DIVISION', 'WINS', 'LOSSES'])
print(dfr)
print("======================================================")
print("Simulation finished")

sims_team_result_list = []
dfr.sort_values(by='Row', ascending=True, inplace=True)
for line in dfr.values.tolist():
    sims_team_result_list.append(SimulationsTeamResults(line))

# functions to assign positions
def league_position(sorted_data_frame):
    league_pos = 1
    sorted_df_list = sorted_data_frame.values.tolist()
    for row in sorted_df_list:
        row_num = row[0]
        sims_team_result_list[row_num].league_rank = league_pos
        league_pos += 1

def division_position(sorted_data_frame):
    division_pos = 1
    sorted_df_list = sorted_data_frame.values.tolist()
    for row in sorted_df_list:
        row_num = row[0]
        sims_team_result_list[row_num].division_rank = division_pos
        division_pos += 1

# assign positons
iterations = int(len(sims_team_result_list) / 30)

for i in range(iterations):
    season = i + 1
    national_league_df = dfr.query('Season == ' + str(season) + ' and LEAGUE == "NL"', inplace = False)
    american_league_df = dfr.query('Season == ' + str(season) + ' and LEAGUE == "AL"', inplace = False)

    # sort for position in league
    national_league_df.sort_values(by=['WINS'], ascending=False, inplace=True)
    league_position(national_league_df)

    american_league_df.sort_values(by=['WINS'], ascending=False, inplace=True)
    league_position(american_league_df)

    # sort for positions in Division
    for division in ["W","C","E"]:
        # NL
        qd = 'DIVISION == "' + division + '"'
        national_league_division_df = national_league_df.query(qd, inplace=False)
        national_league_division_df.sort_values(by=['WINS'], ascending=False, inplace=True)
        division_position(national_league_division_df)
        # AL
        american_league_division_df = american_league_df.query(qd, inplace=False)
        american_league_division_df.sort_values(by=['WINS'], ascending=False, inplace=True)
        division_position(american_league_division_df)

# rules for Post Season
for item in sims_team_result_list:
    if(item.division_rank == 1):
        item.is_in_post_season = True

for i in range(iterations):
    season = i + 1
    def extra_in_league(l):
        def candidates_filter(str_obj=SimulationsTeamResults):
            val = True
            val = val & (str_obj.iteration == season)
            val = val & (str_obj.division_rank != 1)
            val = val & (str_obj.league == l)
            return val

        candidates_list = list(filter(candidates_filter, sims_team_result_list))
        candidates_list.sort(key=lambda x: x.league_rank)

        teamid_A = candidates_list[0].strID
        teamid_B = candidates_list[1].strID

        sims_team_result_list[teamid_A].is_in_post_season = True
        sims_team_result_list[teamid_B].is_in_post_season = True

    extra_in_league("NL")
    extra_in_league("AL")

positions_results = [item.to_row() for item in sims_team_result_list]

print("======================================================")
cols=['Row', 'Season', 'TEAM_ID', 'TEAM_NAME', 'LEAGUE', 'DIVISION', 'WINS', 'LOSSES','LEAGUE_RANK','DIV_RANK','POSTSEASON']
final_results_df = pd.DataFrame(positions_results, columns=cols)
print(final_results_df)
print("======================================================")
print("Post Season Tagging Finished")
