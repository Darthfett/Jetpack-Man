"""
An Entity is an Object that moves and can collide

It can have velocity, acceleration, and several other properties
"""

from Object import Object
import math

class Entity(Object):
    Entities = []

    def getNextFrame(self):
        """
        Calculates the current animation.
        """
        return self.objectType.animations['idle']

    def onLand(self):
        """
        Called upon landing on an object
        """
        self.acceleration[1] = 0

    def onObjectCollision(self, object):
        """
        Upon collision with an Object, entities are moved towards the side of the bounding rect that they would have hit first.
        """
        if self.velocity[0] < 0:
            vxDiff = object.rect.right - self.rect.left
        elif self.velocity[0] > 0:
            vxDiff = object.rect.left - self.rect.right
        else:
            if self.velocity[1] < 0:
                self.rect.top = object.rect.bottom
            else:
                self.rect.bottom = object.rect.top
                
            return Object.Bottom if self.velocity[1] < 0 else Object.Top

        if self.velocity[1] > 0:
            vyDiff = object.rect.top - self.rect.bottom
        elif self.velocity[1] < 0:
            vyDiff = object.rect.bottom - self.rect.top
        else:
            self.rect.left += vxDiff
            return Object.Left if vxDiff > 0 else Object.Right

        if (abs(vyDiff / self.velocity[1]) > abs(vxDiff / self.velocity[0])):
            self.rect.left += vxDiff
            return Object.Left if vxDiff > 0 else Object.Right
                
        else:
            self.rect.top += vyDiff
            return Object.Bottom if vyDiff > 0 else Object.Top

    def colliding(self, isColliding, object):
        if isColliding:
            if self.projectile:
                self.destroy = True
                return
            else:
                collisionType = self.onObjectCollision(object)
            
            if collisionType == Object.Left:
                self.collidingLeft = True
            elif collisionType == Object.Right:
                self.collidingRight = True
            elif collisionType == Object.Top:
                self.collidingTop = True
            else:
                self.collidingBottom = True
                
            if collisionType != Object.Bottom:
                self.onLand()

    def __init__(self, whichType, position = [0, 0], velocity = [0, 0], acceleration = [0, 0], flipped = False, projectile = False):
        """
        Creates a basic Entity of a specific type.
        """
        Object.__init__(self, whichType, position, flipped = flipped)
        Entity.Entities.append(self)
        Object.Objects.pop(-1)
        
        #Collision
        self.collideState = None
        self.collidingLeft,self.collidingRight,self.collidingTop,self.collidingBottom = [False] * 4

        #Physics
        self.acceleration = acceleration
        self.velocity = velocity
        
        self.wallSliding = False
        self.slidingSide = None

        self.projectile = projectile
        self.destroy = False
