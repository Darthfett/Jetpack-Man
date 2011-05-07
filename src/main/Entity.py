"""
An Entity is an Object that moves and can collide

It can have velocity, acceleration, and several other properties
"""

from Object import Object
from Vector import Vector
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
        self.acceleration.y = 0

    def onObjectCollision(self, object):
        """
        Upon collision with an Object, entities are moved towards the side of the bounding rect that they would have hit first.
        """
        if self.velocity.x < 0:
            vxDiff = (object.position.x + object.objectType.width) - self.position.x
        elif self.velocity.x > 0:
            vxDiff = object.position.x - (self.position.x + self.objectType.width)
        else:
            self.position.y = (object.position.y - self.objectType.height) if (self.velocity.y > 0) else (object.position.y + object.objectType.height) 
                
            return Object.Bottom if self.velocity.y > 0 else Object.Top

        if self.velocity.y < 0:
            vyDiff = (object.position.y + object.objectType.height) - self.position.y
        elif self.velocity.y > 0:
            vyDiff = object.position.y - (self.position.y + self.objectType.height)
        else:
            self.position.x += vxDiff
            return Object.Left if vxDiff > 0 else Object.Right

        if (abs(vyDiff / self.velocity.y) > abs(vxDiff / self.velocity.x)):
            self.position += Vector(vxDiff, 0)
            if self.position == None:
                print "error line 50"
            return Object.Left if vxDiff > 0 else Object.Right
                
        else:
            self.position += Vector(0, vyDiff) 
            if self.position == None:
                print "error line 56"
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

    def __init__(self, whichType, position = None, velocity = None, acceleration = None, flipped = False, projectile = False):
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
        if acceleration == None:
            self.acceleration = Vector()
        self.velocity = velocity
        if velocity == None:
            self.velocity = Vector()
        
        self.wallSliding = False
        self.slidingSide = None

        self.projectile = projectile
        self.destroy = False
