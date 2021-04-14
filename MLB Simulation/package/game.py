class Game:

    def get_bat_scenarios(self):
        from team_stats import TeamStats
        from bat_scenario import BatScenario
        v_team_stats = TeamStats()

        l_scenarios = [
            BatScenario(v_team_stats.singles.__name__, 1, 0),
            BatScenario(v_team_stats.doubles.__name__, 2, 0),
            BatScenario(v_team_stats.triple.__name__, 3, 0),
            BatScenario(v_team_stats.home_runs.__name__, 4, 0),
            BatScenario(v_team_stats.base_on_balls.__name__, 1, 0),
            BatScenario(v_team_stats.hit_by_pitch.__name__, 1, 0),
            BatScenario(v_team_stats.sacrifice.__name__, 1, 0),
            BatScenario(v_team_stats.strike_out.__name__, 0, 1),
            BatScenario(v_team_stats.double_played.__name__, 0, 2),
            BatScenario(v_team_stats.fg_outs.__name__, 0, 1),
        ]
        return {scenarios.name : scenarios for scenarios in l_scenarios}

    def ___init__(self):
        from teamData import TeamData
        super().__init__()
        self.TeamA = TeamData
        self.TeamB = TeamData
        self.ResultA = []
        self.ResultB = []
        self.simulations = []
        self.RunsA = 0
        self.RunsB = 0

    @property
    def TeamA(self):
        return self.TeamA

    @TeamA.setter
    def TeamA(self, teamA):
        self.TeamA = teamA
    @property
    def TeamB(self):
        return self.TeamB
    
    @TeamB.setter
    def TeamB(self, teamB):
        self.TeamB = teamB
    
    @property
    def ResultA(self):
        return self.ResultA
    @property
    def ResultB(self):
        return self.ResultB
    
    @property
    def Simulations(self):
        return list(self.simulations)
    
    @property
    def RunsA(self):
        list=[]
        for i in self.ResultA:
            list.append(i.runs)
        return sum(list)
    @property
    def RunsB(self):
        list=[]
        for i in self.ResultB:
            list.append(i.runs)
        return sum(list)

    def playInning(self,data = TeamData):
        from bats_result import BatsResult
        from inning import Inning as inning
        import random
        import datetime
        def firstElement(list = [], r = 0.0):
            for item in list:
                if item.inRange(r):
                    return item
        scenarios = self.get_bat_scenarios()
        random.seed(datetime.datetime.fromtimestamp)        
        v_inning = inning()
        while v_inning.is_active and v_inning.runs < 9 :
            rand = random.random()
            action = ""
            if v_inning.have_runners:
                element = firstElement(data.rangeA, rand)
                action = element.action
            else:
                element = firstElement(data.rangeB, rand)
                action = element.action
            
            scenario = scenarios[action]
            v_inning = v_inning.add_plate()
            v_inning = v_inning.out(scenario.outs)
            v_inning = v_inning.move(scenario.moves)
            self.simulations.append(BatsResult(scenario.name, data.Name))
        
        while v_inning.is_active:
            v_inning = v_inning.out(1)

        return v_inning
    
    def __init__(self, a = TeamData, b = TeamData):
        from inning import Inning as inning
        import random
        import datetime
        self.TeamA = a
        self.TeamB = b
        self.ResultA = []
        self.ResultB = []
        self.simulations = []               
        while len(self.ResultA) < 9 and len(self.ResultB) < 9:
            self.ResultA.append(self.playInning(self.TeamA))
            self.ResultB.append(self.playInning(self.TeamB))
        
        extraInning = 11

        while self.RunsA == self.RunsB and extraInning > 0:
            self.ResultA.append(self.playInning(self.TeamA))
            self.ResultB.append(self.playInning(self.TeamB))
            extraInning += -1
        
        if self.RunsA == self.RunsB:
            random.seed(datetime.datetime.fromtimestamp)
            rand = random.random()

            if rand < 0.5:
                self.ResultA.append(inning.one_run(True))
                self.ResultB.append(inning.one_run(False))
            else:
                self.ResultA.append(inning.one_run(False))
                self.ResultB.append(inning.one_run(True))






    