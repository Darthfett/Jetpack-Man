"""
An Entity is an Object that moves and can collide

It can have velocity, acceleration, and several other properties
"""

from Object import Object
import math

class Entity(Object):
    Entities = []
    MaxHorizontalMoveSpeed = 4

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
        
    def onObjectCollision2(self,object):
        """
        Finds the side the entity is colliding with
        """
        if self.velocity[0] == 0:
            if self.velocity[1] == 0:
                print "Warning:",self,"is colliding with",object," while not moving."                
                
            else:
                # Player may be wallsliding
                vxDiff = min(abs(object.rect.right - self.rect.left),abs(object.rect.left - self.rect.right))
                if vxDiff <= Entity.MaxHorizontalMoveSpeed:
                    self.wallSliding = True
                    if self.slidingSide == Object.Left:
                        return Object.Left
                    else:
                        return Object.Right
                else:
                    return Object.Top if self.velocity[1] > 0 else Object.Bottom
        else:
            if self.velocity[1] == 0:
                if self.velocity[0] < 0:
                    return Object.Left
                else:   
                    return Object.Right
            else:
                # Find the side the entity would have hit first
                vxDiff = min(abs(object.rect.right - self.rect.left),abs(object.rect.left - self.rect.right))
                vyDiff = min(abs(object.rect.top - self.rect.bottom),abs(object.rect.bottom - self.rect.top))
                if (abs(vyDiff / self.velocity[1]) > abs(vxDiff / self.velocity[0])):
                    return Object.Left if self.velocity[0] > 0 else Object.Right
                else:
                    return Object.Top if self.velocity[1] > 0 else Object.Bottom

    def onObjectCollision(self, object):
        """
        Upon collision with an Object, entities are moved towards the side of the bounding rect that they would have hit first.
        """
        if self.velocity[0] < 0:
            vxDiff = object.rect.right - self.rect.left
        elif self.velocity[0] > 0:
            vxDiff = object.rect.left - self.rect.right
        else:
            if self.wallSliding and self.velocity[0] == 0 and (abs(object.rect.left - self.rect.right) < 5) or (abs(object.rect.right - self.rect.left) < 5):
                return None
                
            print (abs(object.rect.left - self.rect.right) < 5), (abs(object.rect.right - self.rect.left) < 5)
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
                collisionType = self.onObjectCollision2(object)
            
            if collisionType == Object.Left:
                self.rect.right = object.rect.left
                self.collidingLeft = True
            elif collisionType == Object.Right:
                self.rect.right = object.rect.left
                self.collidingRight = True
            elif collisionType == Object.Top:
                self.rect.bottom = object.rect.top
                self.collidingTop = True
            elif collisionType == Object.Bottom:
                self.rect.top = object.rect.bottom
                self.collidingBottom = True
            else:
                print "Warning:",self,"colliding with",object," onObjectCollision returned without releasing collided side"
                pass
                
            if collisionType != Object.Bottom and collisionType != None:
                self.onLand()
                
            if (collisionType == Object.Left or collisionType == Object.Right) and self.trySlide:
                self.wallSliding = True
                self.slidingSide = collisionType
            else:
                self.wallSliding = False
                self.slidingSide = None

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
        self.trySlide = False

        self.projectile = projectile
        self.destroy = False
