class Action:
    key = ""
    count = 0
    valueA = 0
    valueB = 0

    def __init__(self, key, count):
        self.key = key
        self.count = count
    
    @property
    def key(self):
        return self.key
    