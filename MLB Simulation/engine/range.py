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
