"""
A Level is (currently) a listing of objects throughout the level

It should also define start position as well as level size
"""

    import os

class Level:
    
    Levels = {}
    
    def __init__(self,name,objects):
        Level.Levels[name]=self
        self.name = name
        self.objects = objects