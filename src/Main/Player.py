"""

The Player is the Entity that the player controls.

"""

from Entity import Entity
from Main.ObjectType import ObjectType
import Game

class Player(Entity):

    FlyAcceleration = 0.51
    JumpInitialVelocity = 9
    HorizontalMoveSpeed = 1
    MaxHorizontalMoveSpeed = 4
    WallJumpRepelSpeed = 8
    FireDelay = 10

    MaxFlyLength = 64

    MovingLeft, MovingRight, NotMoving = range(3)

    def getNextFrame(self):
        """
        Calculates the current animation.
        """
        if self.blink:
            self.draw = not self.draw
        self.currentAnimation = self.objectType.animations['idle']
        if self.moveState != Player.NotMoving:
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
                projectile = Entity(ObjectType.ObjectTypes['laser'], position = [self.position[0] + (-5 if self.flipped else 5), self.position[1] + 5],velocity = [-15 if self.flipped else 15,0], acceleration = [0,-Game.Game.Gravity], projectile = True)

    def flying(self, isFlying):
        """
        Starts/Stops the player's Jetpack.        
        """

        if (not self.isFlying and isFlying and self.flyCounter <= Player.MaxFlyLength and not self.wallSliding):
            self.isFlying = True
            self.acceleration[1] -= Player.FlyAcceleration
        elif (self.isFlying and not isFlying):
            self.isFlying = False
            self.acceleration[1] += Player.FlyAcceleration
        elif (self.isFlying and isFlying):
            self.flyCounter += 0.5 + abs(min(0, self.velocity[1] / 2))
            if self.flyCounter > Player.MaxFlyLength:
                self.isFlying = False
                self.acceleration[1] += Player.FlyAcceleration

    def jumping(self, isJumping):
        """
        Starts/Stops the player's jump
        """

        if (isJumping and (self.wallSliding or not self.isJumping and self.velocity[1] == 0)):
            self.isJumping = True
            self.velocity[1] = -Player.JumpInitialVelocity
            if self.collidingLeft:
                self.velocity[0] += Player.WallJumpRepelSpeed
            elif self.collidingRight:
                self.velocity[0] -= Player.WallJumpRepelSpeed
        elif (not isJumping and self.isJumping):
            self.isJumping = False
            if (self.velocity[1] < 0 and not self.isFlying):
                self.velocity[1] = 0

    def running(self, toRight, isRunning):
        """
        Starts/Stops the player's horizontal movement.
        """

        if not isRunning:
            # Slow the player down to zero when user is not running
            if self.velocity[0] != 0 and abs(self.velocity[0]) < Player.HorizontalMoveSpeed:
                self.velocity[0] = 0
            elif self.velocity[0] >= Player.HorizontalMoveSpeed:
                self.velocity[0] -= Player.HorizontalMoveSpeed
            elif abs(self.velocity[0]) >= Player.HorizontalMoveSpeed:
                self.velocity[0] += Player.HorizontalMoveSpeed
            self.moveState = Player.NotMoving
            self.collideState = Entity.NotColliding
        else:
            # Speed the player up to Player.MaxHorizonalMoveSpeed in the direction they are moving.
            if toRight:
                self.velocity[0] = min(self.velocity[0] + Player.HorizontalMoveSpeed, Player.MaxHorizontalMoveSpeed)
            else:
                self.velocity[0] = max(self.velocity[0] - Player.HorizontalMoveSpeed, -Player.MaxHorizontalMoveSpeed)
                
            if not self.collidingLeft and not self.collidingRight and (self.collidingTop or self.collidingBottom):
                self.flipped = not toRight
            elif self.collidingLeft or self.collidingRight and (not self.collidingTop and not self.collidingBottom):
                self.flipped = toRight if self.wallSliding else not toRight
            elif not (self.collidingLeft or self.collidingRight or self.collidingTop or self.collidingBottom):
                self.flipped = not toRight
            else:
                self.flipped = not toRight if self.velocity[1] == 0 else toRight
            self.moveState = Player.MovingRight if toRight else Player.MovingLeft

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
        self.blink = False
        self.moveState = Player.NotMoving
        self.isJumping = False
        self.isFlying = False
        self.flyCounter = 0
        self.fireDelay = Player.FireDelay
