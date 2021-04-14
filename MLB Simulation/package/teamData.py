from . import action
from . import range_
from . import team_stats
class TeamData:
    
    def __init___(self):
        self.Name = ""
        self.Counters = []
        self.rangeA = []
        self.rangeB = []

    
    @property
    def counters(self):
        return {counter.name : counter for counter in self.Counters}

    @property
    def Counters(self):
        return self.Counters
    
    @property
    def rangeA(self):
        return list(self.rangeA)
    
    @property
    def rangeB(self):
        return list(self.rangeB)

    def __init__(self, teamStats = team_stats):

        self.Name = teamStats.id
        self.Counters = [Action(teamStats.base_On_balls.__name__, teamStats.base_On_balls),
        Action(teamStats.double_played._name__,teamStats.double_played),
        Action(teamStats.doubles.__name__,teamStats.doubles),
        Action(teamStats.fg_outs.__name__,teamStats.fg_outs),
        Action(teamStats.hit_by_pitch.__name__,teamStats.hit_by_pitch),
        Action(teamStats.home_runs.__name__,teamStats.home_runs),
        Action(teamStats.sacrifice.__name__,teamStats.sacrifice),
        Action(teamStats.singles.__name__,teamStats.singles),
        Action(teamStats.strike_out.__name__,teamStats.strike_out),
        Action(teamStats.triple.__name__,teamStats.triple)]
    
        fulldiv = lambda num,dem: float(num)/float(dem)

        for item in self.Counters:
            item.valueA = fulldiv(item.count, teamStats.plates)
            if item.key == teamStats.sacrifice.__name__ or item.key == teamStats.double_played.__name__ :
                item.valueB = 0
            else:
                item.valueB = fulldiv(item.count, (teamStats.plates - teamStats.sacrifice - teamStats.double_played))
        
        counter = 0
        self.rangeA = []
        listA = []

        for x in self.Counters:
            obj = type('', (object,),{'Llave': x.key,'ValorA':x.valueA})()
            listA.append(obj)
        myfun = lambda e: e.valueA
        listA.sort(reverse=True, key=myfun)
        for item in listA:
            Range = Range(counter, item.valueA, item.key)
            self.rangeA.append(Range)
            counter+=item.valueA
        
        counter = 0

        self.rangeB = []
        listB = []
        
        for i in self.Counters:
            if i.key != teamStats.sacrifice.__name__ and i.key != teamStats.double_played.__name__:
                obj = type('', (object,),{'Llave': x.key,'ValorA':x.valueA})()
                listB.append(obj)
        
        listB.sort(reverse=True,key=myfun)

        for item in listB:
            Range_ = Range(counter, item.valueB, item.key)
            self.rangeB.append(Range_)
            counter+=item.valueB





        


            




            
    


