"""
An Entity is an Object that moves and can collide

It can have velocity, acceleration, and several other properties
"""

from Object import Object
import math

class Entity(Object):
    Entities = []

    LeftCollision, RightCollision, TopCollision, BottomCollision = range(4)
    CollidingLeft, CollidingRight, NotColliding = range(3)

    def getNextFrame(self):
        """
        Calculates the current animation.
        """
        self.currentAnimation = self.objectType.animations['idle']
        if (self.velocity[0] != 0):
            self.currentAnimation = self.objectType.animations['move']

        return self.currentAnimation.frame[0]

    def onLand(self):
        """
        Called upon landing on an object
        """
        self.acceleration[1] = 0
        pass

    def onObjectCollision(self, object):
        """
        Upon collision with an Object, entities are moved towards the side of the bounding rect that they would have hit first.
        """
        if self.velocity[0] < 0:
            vxDiff = (object.position[0] + object.objectType.width) - self.position[0]
        elif self.velocity[0] > 0:
            vxDiff = object.position[0] - (self.position[0] + self.objectType.width)
        else:
            self.position[1] = (object.position[1] + object.objectType.height) if (self.velocity[1] < 0) else (object.position[1] - self.objectType.height)
            if self.detectCollision(object):
                print "DEBUG",self,"is still colliding with",object,"" + " top" if self.velocity[1] > 0 else " bottom"
                
            return Entity.BottomCollision if self.velocity[1] < 0 else Entity.TopCollision

        if self.velocity[1] > 0:
            vyDiff = object.position[1] - (self.position[1] + self.objectType.height)
        elif self.velocity[1] < 0:
            vyDiff = (object.position[1] + object.objectType.height) - self.position[1]
        else:
            self.position[0] += vxDiff
            if self.detectCollision(object):
                print "DEBUG",self,"is still colliding with",object,"" + " right" if vxDiff > 0 else " left"
            return Entity.LeftCollision if vxDiff > 0 else Entity.RightCollision

        if (abs(vyDiff / self.velocity[1]) > abs(vxDiff / self.velocity[0])):
            self.position[0] += vxDiff
            if self.detectCollision(object):
                print "DEBUG",self,"is still colliding with",object,"" + " right" if vxDiff > 0 else " left"
            return Entity.LeftCollision if vxDiff > 0 else Entity.RightCollision
        else:
            self.position[1] += vyDiff
            if self.detectCollision(object):
                print "DEBUG",self,"is still colliding with",object,"" + " top" if self.velocity[1] > 0 else " bottom"
            return Entity.BottomCollision if vyDiff > 0 else Entity.TopCollision

    def colliding(self, isColliding, object):
        if isColliding:
            collisionType = self.onObjectCollision(object)
            
            if collisionType == Entity.LeftCollision:
                self.collidingLeft = True
            elif collisionType == Entity.RightCollision:
                self.collidingRight = True
            elif collisionType == Entity.TopCollision:
                self.collidingTop = True
            else:
                self.collidingBottom = True
                
            if collisionType == Entity.BottomCollision or collisionType == Entity.TopCollision:
                self.wallSliding = False
            else:
                self.wallSliding = True
            self.onLand()

    def __init__(self, whichType, wallSliding = False, position = [0, 0], velocity = [0, 0], acceleration = [0, 0], flipped = False, collideState = NotColliding):
        """
        Creates a basic Entity of a specific type.
        """
        Object.__init__(self, whichType, position, flipped = flipped)
        Entity.Entities.append(self)
        Object.Objects.pop(-1)

        self.wallSliding = wallSliding
        self.velocity = velocity
        self.acceleration = acceleration

        self.collideState = collideState
        self.collidingLeft,self.collidingRight,self.collidingTop,self.collidingBottom = [False] * 4
        self.collidingRight = False
