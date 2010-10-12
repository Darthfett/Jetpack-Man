"""

The Player is the Entity that the player controls.

"""

from Entity import Entity

class Player(Entity):

    FlyAcceleration = 0.53
    JumpInitialVelocity = 10
    HorizontalMoveSpeed = 3

    MaxFlyLength = 16

    def flying(self, isFlying):
        """
        Starts/Stops the player's Jetpack.        
        """
        
        if (not self.isFlying and isFlying and self.flyCounter <= Player.MaxFlyLength):
            self.isFlying = True
            self.isFalling = True
            self.acceleration[1] -= Player.FlyAcceleration
        elif (self.isFlying and not isFlying):
            self.isFlying = False
            self.acceleration[1] += Player.FlyAcceleration
        elif (self.isFlying and isFlying):
            self.flyCounter += 1
            if self.flyCounter > Player.MaxFlyLength:
                self.isFlying = False
                self.acceleration[1] += Player.FlyAcceleration

    def jumping(self, isJumping):
        """
        Starts/Stops the player's jump
        """
        
        if (isJumping and not self.isJumping and not self.isFalling):
            self.isJumping = True
            self.isFalling = True
            self.velocity[1] -= Player.JumpInitialVelocity
        elif (not isJumping and self.isJumping):
            self.isJumping = False
            if (self.velocity[1] < 0 and not self.isFlying):
                self.velocity[1] = 0

    def running(self, toRight, isRunning):
        """
        Starts/Stops the player's horizontal movement.
        """
        
        if not isRunning:
            self.velocity[0] = 0
        else:
            self.velocity[0] = ((Player.HorizontalMoveSpeed) if toRight else (-Player.HorizontalMoveSpeed))
            if (self.velocity[0] > 0):
                self.flipped = False
            elif (self.velocity[0] < 0):
                self.flipped = True

    def onLand(self):
        """
        Called when the player lands on ground of some sort
        """
        Entity.onLand(self)
        self.isJumping = False
        self.isFlying = False
        self.flyCounter = 0

    def __init__(self, whichType):
        Entity.__init__(self, whichType,position=[0,0])
        self.isFalling = True
        self.isJumping = False
        self.isFlying = False
        self.flyCounter = 0
