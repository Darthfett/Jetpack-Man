"""
An Object is an object that is drawn to the screen.

It can have animations, position, and size.
"""

class Object:
    Objects = []

    def getNextFrame(self):
        """
        Calculates the current animation.
        """
        
        self.currentAnimation = self.objectType.animations['idle']

        return self.currentAnimation.frame[0]

    def __init__(self, whichType, position = [0, 0]):
        """
        Creates a basic Entity of a specific type.
        """
        
        Object.Objects.append(self)
        self.flipped = False

        self.position = position

        self.objectType = whichType
        self.currentAnimation = self.objectType.animations['idle']
        self.currentFrame = self.objectType.animations['idle'].frame[0]
