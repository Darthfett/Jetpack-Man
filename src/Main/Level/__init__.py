"""
A Level is (currently) a listing of objects throughout the level

It should also define start position as well as level size
"""

import os
import pygame

class Level:
    
    Levels = {}
    
    def __init__(self,name,objects,width=800,height=600,start=[80,0]):
        Level.Levels[name]=self
        self.name = name
        self.start = start
        self.objects = objects
        self.rect = pygame.Rect((0,0),(width,height))