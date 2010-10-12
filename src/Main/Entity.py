"""
An Entity is an Object that moves and can collide

It can have velocity, acceleration, and several other properties
"""

from Object import Object

class Entity(Object):
    Entities = []

    def getNextFrame(self):
        """
        Calculates the current animation.
        """
        self.currentAnimation = self.objectType.animations['idle']
        if (self.velocity[0] != 0):
            self.currentAnimation = self.objectType.animations['move']

        return self.currentAnimation.frame[0]
    
    def onLand(self):
        self.isFalling = False
        self.velocity[1] = 0
        self.acceleration[1] = 0

    def __init__(self, whichType, position = [0, 0], velocity = [0, 0], acceleration = [0, 0]):
        """
        Creates a basic Entity of a specific type.
        """
        Object.__init__(self, whichType, position)
        Entity.Entities.append(self)
        Object.Objects.pop(-1)
        
        self.velocity = velocity
        self.acceleration = acceleration
        