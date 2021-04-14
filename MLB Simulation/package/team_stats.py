class TeamStats:
    id = 0
    teamid = 0
    singles = 0
    doubles = 0
    triples = 0
    home_runs = 0
    base_on_balls = 0
    hit_by_pitch = 0
    sacrifce = 0
    double_played = 0
    strike_out = 0
    fg_out = 0
    plates = 0

    def __init__(self):
        super().__init__()

    @property
    def base_on_balls(self):
        return self.base_on_balls
    
    @property
    def double_played(self):
        return self.double_played
    @property
    def doubles(self):
        return self.doubles
    
    @property
    def fg_outs(self):
        return self.fg_out
    
    @property
    def hit_by_pitch(self):
        return self.hit_by_pitch
    
    @property
    def home_runs(self):
        return self.home_runs
    
    @property
    def sacrifice(self):
        return self.sacrifice
    
    @property
    def singles(self):
        return self.singles
    
    @property
    def strike_out(self):
        return self.strike_out
    
    @property
    def triple(self):
        return self.triples
