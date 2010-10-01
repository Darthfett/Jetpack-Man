"""
An Entity is an object that is drawn to the screen.

It can have animations, as well as position, velocity, and acceleration.
"""

import pygame

class Entity:
    Entities = []

    def getNextFrame(self):
        """
        Calculates the current animation.
        """
        self.currentAnimation = self.entityType.animations['idle']
        if (self.velocity[0] != 0):
            self.currentAnimation = self.entityType.animations['move']

        return self.currentAnimation.frame[0]

    def __init__(self, whichType, position = [0, 0], velocity = [0, 0], acceleration = [0, 0]):
        """
        Creates a basic Entity of a specific type.
        """
        Entity.Entities.append(self)
        self.flipped = True

        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

        self.entityType = whichType
        self.currentAnimation = self.entityType.animations['idle']
        self.currentFrame = self.getNextFrame()
