class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    
    def __str__(self) -> str:
        return "(%s, %s, %s)" % (self.r, self.g, self.b)