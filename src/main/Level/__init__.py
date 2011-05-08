"""
A Level is (currently) a listing of objects throughout the level

It should also define start position as well as level size
"""
from main.Vector import Vector

import os
import pygame

class Level:
    
    Levels = {}
    
    def __init__(self,name,objects = None,width=800,height=600,start=None):
        Level.Levels[name]=self
        self.name = name
        self.start = start
        if start == None:
            self.start = Vector(0, 600)
        self.objects = objects
        self.rect = pygame.Rect((0,0),(width,height))
        print "start",start
