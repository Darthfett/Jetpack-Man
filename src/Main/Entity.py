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
        try:
            if (self.velocity[0] != 0):
                self.currentAnimation = self.objectType.animations['move']
        except:
            pass

        return self.currentAnimation.frame[0]

    def onLand(self):
        """
        Called upon landing on an object
        """
        self.acceleration[1] = 0
        pass
    
    def getBestPosition(self, position1, position2):
        selfMinX1 = position1[0]
        selfMinY1 = abs(position1[1])
        selfMaxX1 = position1[0] + self.objectType.width
        selfMaxY1 = abs(position1[1] + self.objectType.height)
        
        selfMinX2 = position2[0]
        selfMinY2 = abs(position2[1])
        selfMaxX2 = position2[0] + self.objectType.width
        selfMaxY2 = abs(position2[1] + self.objectType.height)
        
        collision1 = False
        collision2 = False
        for object in Object.Objects:
            objectMinX = object.position[0]
            objectMinY = abs(object.position[1])
            objectMaxX = object.position[0] + object.objectType.width
            objectMaxY = abs(object.position[1] + object.objectType.height)
            collision1 = not (selfMaxX1 <= objectMinX or selfMinX1 >= objectMaxX or selfMaxY1 <= objectMinY or selfMinY1 >= objectMaxY)
            collision2 = not (selfMaxX2 <= objectMinX or selfMinX2 >= objectMaxX or selfMaxY2 <= objectMinY or selfMinY2 >= objectMaxY)
                    
        if not collision1:
            return position1
        
        if collision2:
            return position2
        print "Uh oh, double collisions"
        return None
        
        

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
            Xpoint = [self.position[0] + vxDiff, self.position[1]]
            Ypoint = [self.position[0],self.position[1] + vyDiff]
            newPosition = self.getBestPosition(Xpoint, Ypoint)
            if newPosition != None:
                self.position = newPosition
            else:
                self.position = Xpoint
                
            if self.detectCollision(object):
                print "DEBUG",self,"is still colliding with",object,"" + " right" if vxDiff > 0 else " left"
            return Entity.LeftCollision if vxDiff > 0 else Entity.RightCollision
        else:
            Xpoint = [self.position[0] + vxDiff, self.position[1]]
            Ypoint = [self.position[0],self.position[1] + vyDiff]
            newPosition = self.getBestPosition(Ypoint, Xpoint)
            if newPosition != None:
                self.position = newPosition
            else:
                self.position = Ypoint
                
            if self.detectCollision(object):
                print "DEBUG",self,"is still colliding with",object,"" + " top" if self.velocity[1] > 0 else " bottom"
            return Entity.BottomCollision if vyDiff > 0 else Entity.TopCollision

    def colliding(self, isColliding, object):
        if isColliding:
            if self.projectile:
                # Destroy projectile
                return
            else:
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
            if collisionType != Entity.BottomCollision:
                self.onLand()

    def __init__(self, whichType, wallSliding = False, position = [0, 0], velocity = [0, 0], acceleration = [0, 0], flipped = False, collideState = NotColliding, projectile = False):
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
        self.projectile = projectile
        self.bugTest = False