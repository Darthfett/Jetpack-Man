"""

The Player is the Entity that the player controls.

"""

from Entity import Entity
from Object import Object
from ObjectType import ObjectType
from Vector import Vector
import Game

class Player(Entity):

    FlyAcceleration = 0.51
    JumpInitialVelocity = 9
    HorizontalMoveSpeed = 1
    MaxHorizontalMoveSpeed = 4
    WallJumpRepelSpeed = 8
    FireDelay = 10

    MaxFlyLength = 64
    
    #Running State
    RunningLeft, RunningRight = range(2)

    def getNextFrame(self):
        """
        Calculates the current animation.
        """
        self.currentAnimation = self.objectType.animations['idle']
        if self.runState != None:
            self.currentAnimation = self.objectType.animations['move']
        if self.isFlying:
            self.currentAnimation = self.objectType.animations['fly']
    
    
    def firing(self,isFiring):
        """
        Starts/Stops the player's weapon.
        """
        self.isFiring = isFiring
        if self.fireDelay > 0:
            self.fireDelay -= 1
        if self.isFiring:
            if self.fireDelay <= 0:
                self.fireDelay = Player.FireDelay
                projectile = Entity(ObjectType.ObjectTypes['laser'], position = Vector(self.position.x + (-5 if self.flipped else 5), self.position.y + 5),velocity = Vector(-15 if self.flipped else 15,0), acceleration = Vector(0, -Game.Game.Gravity), projectile = True)

    def flying(self, isFlying):
        """
        Starts/Stops the player's Jetpack.        
        """
        
        if isFlying:
            if self.isFlying:
                if self.flyCounter > Player.MaxFlyLength:
                    self.isFlying = False
                    self.acceleration.y -= Player.FlyAcceleration
                else:
                    if self.wallSliding:
                        self.isFlying = False
                        self.acceleration.y -= Player.FlyAcceleration
                    else:
                        self.flyCounter += 0.5 + abs(max(0, self.velocity.y / 2))
            else:
                if self.wallSliding:
                    pass
                else:
                    if self.flyCounter <= Player.MaxFlyLength:
                        self.isFlying = True
                        self.acceleration.y += Player.FlyAcceleration
        else:
            if self.isFlying:
                self.isFlying = False
                self. acceleration.y -= Player.FlyAcceleration

    def jumping(self, isJumping):
        """
        Starts/Stops the player's jump
        """
        
        if isJumping:
            if not self.isJumping:
                if self.velocity.y == 0:
                    self.isJumping = True
                    self.velocity.y = Player.JumpInitialVelocity
                elif self.wallSliding:
                    self.wallSliding = False
                    self.isJumping = True
                    self.velocity.y = Player.JumpInitialVelocity
                    self.velocity.x += Player.WallJumpRepelSpeed if self.slidingSide == Object.Left else -Player.WallJumpRepelSpeed
                        
            elif self.wallSliding:
                self.wallSliding = False
                self.isJumping = True
                self.velocity.y = Player.JumpInitialVelocity
                self.velocity.x += Player.WallJumpRepelSpeed if self.slidingSide == Object.Left else -Player.WallJumpRepelSpeed
                
        elif not isJumping and self.isJumping:
            self.isJumping = False
            if self.velocity.y > 0 and not self.isFlying:
                self.velocity.y = 0

    def running(self, toRight, isRunning):
        """
        Starts/Stops the player's horizontal movement.
        """

        if not isRunning:
            if self.velocity.x != 0 and abs(self.velocity.x) < Player.HorizontalMoveSpeed:
                self.velocity.x = 0
            elif self.velocity.x >= Player.HorizontalMoveSpeed:
                self.velocity.x -= Player.HorizontalMoveSpeed
            elif abs(self.velocity.x) >= Player.HorizontalMoveSpeed:
                self.velocity.x += Player.HorizontalMoveSpeed
                
            self.runState = None
            self.wallSliding = False
            self.slidingSide = None
            
        else:
            # Speed the player up to Player.MaxHorizonalMoveSpeed in the direction they are moving.
            if toRight and self.collidingRight or not toRight and self.collidingLeft:
                self.wallSliding = True
                self.slidingSide = Object.Right if self.collidingRight else Object.Left
            elif self.wallSliding:
                pass
            else:
                self.wallSliding = False
                self.slidingSide = None
            
            if not self.wallSliding:
                if toRight:
                    self.velocity.x = min(self.velocity.x + Player.HorizontalMoveSpeed, Player.MaxHorizontalMoveSpeed)
                else:
                    self.velocity.x = max(self.velocity.x - Player.HorizontalMoveSpeed, -Player.MaxHorizontalMoveSpeed)
                    
            if self.collidingTop:
                self.flipped = not toRight
            elif self.wallSliding:
                self.flipped = self.slidingSide == Object.Right
            else:
                self.flipped = not toRight
                
            self.runState = Object.Right if toRight else Object.Left

    def onLand(self):
        """
        Called when the player lands on ground of some sort
        """
        Entity.onLand(self)
        self.isJumping = False
        self.isFlying = False
        self.flyCounter = 0

    def __init__(self, whichType, position = None, flipped = False):
        Entity.__init__(self, whichType, position = position, flipped = flipped)
        
        #Collision
        
        #Controls
        self.isJumping = False
        
        self.isFlying = False
        self.flyCounter = 0
        
        self.runState = None
        
        self.fireDelay = Player.FireDelay
