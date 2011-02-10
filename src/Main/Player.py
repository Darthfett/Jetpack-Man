"""

The Player is the Entity that the player controls.

"""

from Entity import Entity
from Object import Object
from Main.ObjectType import ObjectType
import Game

class Player(Entity):

    FlyAcceleration = 0.51
    JumpInitialVelocity = 9
    HorizontalMoveSpeed = 1
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
                projectile = Entity(ObjectType.ObjectTypes['laser'], position = [self.rect.left + (-5 if self.flipped else 5), self.rect.top + 5],velocity = [-15 if self.flipped else 15,0], acceleration = [0,-Game.Game.Gravity], projectile = True)

    def flying(self, isFlying):
        """
        Starts/Stops the player's Jetpack.        
        """
        
        if isFlying:
            if self.isFlying:
                if self.flyCounter > Player.MaxFlyLength:
                    self.isFlying = False
                    self.acceleration[1] += Player.FlyAcceleration
                else:
                    if self.wallSliding:
                        self.isFlying = False
                        self.acceleration[1] += Player.FlyAcceleration
                    else:
                        self.flyCounter += 0.5 + abs(min(0, self.velocity[1] / 2))
            else:
                if self.wallSliding:
                    pass
                else:
                    if self.flyCounter <= Player.MaxFlyLength:
                        self.isFlying = True
                        self.acceleration[1] -= Player.FlyAcceleration
        else:
            if self.isFlying:
                self.isFlying = False
                self. acceleration[1] += Player.FlyAcceleration

    def jumping(self, isJumping):
        """
        Starts/Stops the player's jump
        """
        
        if isJumping:
            if not self.isJumping:
                if self.velocity[1] == 0:
                    self.isJumping = True
                    self.velocity[1] = -Player.JumpInitialVelocity
                elif self.wallSliding:
                    self.wallSliding = False
                    self.isJumping = True
                    self.velocity[1] = -Player.JumpInitialVelocity
                    self.velocity[0] += Player.WallJumpRepelSpeed if self.slidingSide == Object.Left else -Player.WallJumpRepelSpeed
                        
            elif self.wallSliding:
                self.trySlide = False
                self.wallSliding = False
                self.isJumping = True
                self.velocity[1] = -Player.JumpInitialVelocity
                self.velocity[0] += Player.WallJumpRepelSpeed if self.slidingSide == Object.Left else -Player.WallJumpRepelSpeed
                
        elif not isJumping and self.isJumping:
            self.isJumping = False
            if self.velocity[1] < 0 and not self.isFlying:
                self.velocity[1] = 0

    def running(self, toRight, isRunning):
        """
        Starts/Stops the player's horizontal movement.
        """

        if not isRunning:
            if self.velocity[0] != 0 and abs(self.velocity[0]) < Player.HorizontalMoveSpeed:
                self.velocity[0] = 0
            elif self.velocity[0] >= Player.HorizontalMoveSpeed:
                self.velocity[0] -= Player.HorizontalMoveSpeed
            elif abs(self.velocity[0]) >= Player.HorizontalMoveSpeed:
                self.velocity[0] += Player.HorizontalMoveSpeed
            else:               
                self.trySlide = False
                
            self.runState = None
            self.wallSliding = False
            self.slidingSide = None
            
        else:
            self.trySlide = True
            # Speed the player up to Entity.MaxHorizonalMoveSpeed in the direction they are moving.
            if toRight and self.collidingRight or not toRight and self.collidingLeft:
                pass
            else:
                self.wallSliding = False
                self.slidingSide = None
            
            if not self.wallSliding:
                if toRight:
                    self.velocity[0] = min(self.velocity[0] + Player.HorizontalMoveSpeed, Entity.MaxHorizontalMoveSpeed)
                else:
                    self.velocity[0] = max(self.velocity[0] - Player.HorizontalMoveSpeed, -Entity.MaxHorizontalMoveSpeed)
                    
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

    def __init__(self, whichType, position = [0, 0], flipped = False):
        Entity.__init__(self, whichType, position = position, flipped = flipped)
        
        #Collision
        
        #Controls
        self.isJumping = False
        
        self.isFlying = False
        self.flyCounter = 0
        
        self.runState = None
        
        self.fireDelay = Player.FireDelay
