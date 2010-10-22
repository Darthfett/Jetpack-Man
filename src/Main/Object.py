"""
An Object is an object that is drawn to the screen.

It can have animations, position, and size.
"""
from Main.ObjectType import ObjectType
import random

class Object:
    Objects = []
    
    def detectCollision(self,object):
        if self == object:
            return False
        selfMinX = self.position[0]
        selfMinY = abs(self.position[1])
        selfMaxX = self.position[0] + self.objectType.width
        selfMaxY = abs(self.position[1] + self.objectType.height)
        objectMinX = object.position[0]
        objectMinY = abs(object.position[1])
        objectMaxX = object.position[0] + object.objectType.width
        objectMaxY = abs(object.position[1] + object.objectType.height)
        return not (selfMaxX < objectMinX or selfMinX > objectMaxX or selfMaxY < objectMinY or selfMinY > objectMaxY)


    def getNextFrame(self):
        """
        Calculates the current animation.
        """
        
        self.currentAnimation = self.objectType.animations['idle']

        return self.currentAnimation.frame[0]

    def __init__(self, whichType, position = None,flipped = False):
        """
        Creates a basic Entity of a specific type.
        """
        
        Object.Objects.append(self)
        self.flipped = flipped

        self.position = [random.randint(0, 400), random.randint(0, 400)]

        self.objectType = whichType
        self.currentAnimation = self.objectType.animations['idle']
        self.currentFrame = self.objectType.animations['idle'].frame[0]
