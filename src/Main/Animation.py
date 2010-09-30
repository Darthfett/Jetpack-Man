"""

An Animation is a list of frames.

"""

import pygame

class Animation:

    def add(self, path):
        self.frame.append(pygame.image.load(path).convert_alpha())
        return self

    def __init__(self):
        self.frame = []
