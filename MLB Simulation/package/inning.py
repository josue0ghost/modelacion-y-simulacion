class Inning:
    
    # Private Attributes
    __bases = []

    # Public Attributes
    runs = 0
    outs = 0

    def __init__(self):
        self.__bases = []
        self.runs = 0
        self.outs = 0

    @property
    def is_active(self):
        return outs < 3
    
    @property
    def have_runners(self):
        return self.__bases.count(True) > 0

    def copy(self):
        copy = Inning()
        copy.runs = self.runs
        copy.outs = self.outs
        copy.__bases = self.__bases.copy()
        return copy

    def move(self):
        copy = self.copy()
        for i in range(4, 1, -1):
            copy.__bases[i] = copy.__bases[i - 1]
        
        copy.__bases[0] = False

        if copy.__bases[4]:
            copy.runs += 1
            copy.__bases[4] = False
        
        return copy
    
    def move(self, number):
        v_copy = self.copy()
        while number > 0:
            v_copy = v_copy.move()
            number += -1
        
        return copy

    def out(self):
        copy = self.copy()
        copy.__bases[0] = False
        copy.outs += 1
        return copy

    def out(self, number):
        if number == 1:
            return self.out()
        elif number == 2:
            return self.double_play()
        else:
            return self.copy()

    def one_run(self, is_winner):
        ini = Inning()
        if is_winner:
            ini = ini.move(4)

        for i in range(3):
            ini = ini.out()
        
        return ini

    def double_play(self):
        copy = self.out()
        if copy.__bases[3]:
            copy.__bases[3] = False
        elif copy.__bases[2]:
            copy.__bases[2] = False
        else:
            copy.__bases[1] = False
        
        return copy

    def add_plate(self):
        copy = self.copy()
        copy.__bases[0] = True
        return copy