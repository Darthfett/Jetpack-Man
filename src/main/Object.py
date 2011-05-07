"""
An Object is an object that is drawn to the screen.

It can have animations, position, and size.
"""
from main.ObjectType import ObjectType
from Vector import Vector
import pygame

class Object:
    Objects = []
    
    Left,Bottom,Top,Right = range(4)

    def detectCollision(self, object):
        if self == object:
            return False
        selfMinX = self.position.x
        selfMinY = self.position.y
        selfMaxX = self.position.x + self.objectType.width
        selfMaxY = self.position.y + self.objectType.height
        objectMinX = object.position.x
        objectMinY = object.position.y
        objectMaxX = object.position.x + object.objectType.width
        objectMaxY = object.position.y + object.objectType.height
        return not (selfMaxX <= objectMinX or selfMinX >= objectMaxX or selfMaxY <= objectMinY or selfMinY >= objectMaxY)

    def detectRectCollision(self,rect):
        selfMinX = self.position.x
        selfMinY = self.position.y
        selfMaxX = self.position.x + self.objectType.width
        selfMaxY = self.position.y + self.objectType.height
        return not (selfMaxX <= rect.left or selfMinX >= rect.right or selfMaxY <= rect.top or selfMinY >= rect.bottom)
        

    def getNextFrame(self):
        """
        Calculates the current animation.
        """

        self.currentAnimation = self.objectType.animations['idle']

        return self.currentAnimation.frame[0]

    def __init__(self, whichType, position = None, flipped = False, draw = True):
        """
        Creates a basic Entity of a specific type.
        """

        Object.Objects.append(self)
        self.flipped = flipped
        self.position = position
        if position == None:
            self.position = Vector()
        self.draw = draw

        self.objectType = whichType
        self.currentAnimation = self.objectType.animations['idle']
        self.currentFrame = self.objectType.animations['idle'].frame[0]
