"""
An Object is an object that is drawn to the screen.

It can have animations, position, and size.
"""
from Main.ObjectType import ObjectType
import pygame

class Object:
    Objects = []
    
    Left,Bottom,Top,Right = range(4)
    
    @staticmethod
    def detectCollisionXY(selfMinX, selfMaxX, selfMinY, selfMaxY, objectMinX, objectMaxX, objectMinY, objectMaxY):
        return not (selfMaxX < objectMinX or selfMinX > objectMaxX or selfMaxY <= objectMinY or selfMinY >= objectMaxY)

    @staticmethod
    def detectRectOnRectCollision(rectEnt,rectObj):
        return Object.detectCollisionXY(rectEnt.left, rectEnt.right, rectEnt.top, rectEnt.bottom, rectObj.left, rectObj.right, rectObj.top, rectObj.bottom)
        
    def detectRectCollision(self,rectObj):
       return Object.detectRectOnRectCollision(self.rect,rectObj)

    def detectCollision(self, object):
        if self == object:
            return False
        return Object.detectRectOnRectCollision(self.rect,object.rect)
        

    def getNextFrame(self):
        """
        Calculates the current animation.
        """

        self.currentAnimation = self.objectType.animations['idle']

        return self.currentAnimation.frame[0]

    def __init__(self, whichType, position = [0, 0], flipped = False, draw = True):
        """
        Creates a basic Entity of a specific type.
        """

        Object.Objects.append(self)
        self.objectType = whichType
        
        self.flipped = flipped
        self.position = position
        self.rect = self.objectType.rect.move(position[0],position[1])
        
        self.currentAnimation = self.objectType.animations['idle']
        self.currentFrame = self.objectType.animations['idle'].frame[0]
        self.draw = draw
